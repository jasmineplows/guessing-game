import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import string

# ----------------------------------------
# 1) SHARED (GLOBAL) STATE, CACHED
# ----------------------------------------
@st.cache_resource
def get_store():
    """
    Returns a single global dictionary shared by all active user sessions.
    Structure:
      store["guesses"] -> { session_id: guess_value, ... }
      store["public_show_plot"] -> bool
      store["reveal_count"] -> bool
    """
    return {
        "guesses": {},
        "public_show_plot": False,  # controls if *everyone* sees the histogram
        "reveal_count": False,      # controls if *everyone* sees the actual count line
    }

# ----------------------------------------
# 2) HELPER: GET UNIQUE SESSION ID
# ----------------------------------------
def get_session_id():
    """Assign a random session ID to each new user session."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
    return st.session_state.session_id

# ----------------------------------------
# 3) STREAMLIT APP SETUP
# ----------------------------------------
st.set_page_config(page_title="Guess the Jar Count", layout="wide")

ACTUAL_COUNT = 735

# Pull the global store (shared among all sessions)
store = get_store()

# Each user gets a session ID
session_id = get_session_id()

# ----------------------------------------
# 4) IS THIS USER THE HOST?
# ----------------------------------------
# We'll keep it simple: a password field. If correct, this session becomes "host."
if "is_host" not in st.session_state:
    st.session_state["is_host"] = False

def attempt_host_login():
    pwd = st.session_state.get("host_password_input", "")
    if pwd == "secret123":  # <--- Change this to whatever password you like
        st.session_state["is_host"] = True
        st.success("You are now the Host!")
    else:
        st.error("Wrong password!")

# ----------------------------------------
# 5) HOST-ONLY (PRIVATE) PLOT PREVIEW TOGGLE
# ----------------------------------------
# The host can generate a PRIVATE preview of the plot that only they see.  
# This is stored in the host's st.session_state, *not* in the global store.
if "private_plot_host" not in st.session_state:
    st.session_state["private_plot_host"] = False

# ----------------------------------------
# 6) LAYOUT: TWO COLUMNS
# ----------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.title("Guess the Number of Items in the Jar!")

    # A smaller, centered image
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src="image.jpg" width="300" />
            <p><em>How many items do you think are in this jar?</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.subheader("Instructions for Everyone:")
    st.markdown(
        """
        1. Enter your guess below.
        2. Click **Submit Guess**.
        3. Wait until the host decides to show the results!
        """
    )

    guess = st.number_input("Enter your guess:", min_value=0, max_value=100000, value=0)
    if st.button("Submit Guess"):
        # Store guess in the global dictionary, keyed by session_id
        store["guesses"][session_id] = guess
        st.success("Your guess has been submitted!")

    st.write("---")
    st.subheader("Host Login (optional)")
    st.text_input("Enter Host Password:", key="host_password_input", type="password")
    if st.button("Login as Host"):
        attempt_host_login()

# ----------------------------------------
# 7) IF YOU ARE THE HOST
