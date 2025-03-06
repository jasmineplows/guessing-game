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
    Returns a single global dictionary shared by all active users.
    Structure:
      store["guesses"] -> { session_id: guess_value, ... }
      store["show_plot"] -> bool
      store["reveal_count"] -> bool
    """
    return {
        "guesses": {},
        "show_plot": False,
        "reveal_count": False,
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
# 4) HOST MODE / PASSWORD
# ----------------------------------------
# We'll keep it very simple: if you type the correct password, you're "the host."
# That lets you control "Generate Plot" and "Reveal Count."
if "is_host" not in st.session_state:
    st.session_state["is_host"] = False

def host_login():
    """Set is_host = True if the password is correct."""
    pwd = st.session_state.get("host_password_input", "")
    if pwd == "secret123":  # <--- You can change this!
        st.session_state["is_host"] = True
        st.success("You are now in Host mode!")
    else:
        st.error("Incorrect password!")

# ----------------------------------------
# 5) TWO-COLUMN LAYOUT
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
        3. Wait until the host reveals the results!
        """
    )

    # Submit guess
    guess = st.number_input("Enter your guess:", min_value=0, max_value=100000, value=0)
    if st.button("Submit Guess"):
        store["guesses"][session_id] = guess  # store/overwrite the guess for this user
        st.success("Guess submitted!")

    st.write("---")

    # Host login form
    st.subheader("Host Login (optional)")
    st.text_input("Enter Host Password:", key="host_password_input", type="password")
    if st.button("Login as Host"):
        host_login()

# ----------------------------------------
# 6) IF HOST: SHOW HOST-ONLY CONTROLS
# ----------------------------------------
if st.session_state["is_host"]:
    st.write("---")
    st.subheader("Host Controls")
    st.markdown(
        """
        As the host, you can generate the plot (histogram of guesses)
        and reveal the actual count line.
        """
    )
    if st.button("Generate Plot"):
        if len(store["guesses"]) == 0:
            st.warning("No guesses submitted yet!")
        else:
            store["show_plot"] = True

    if st.button("Hide Plot"):
        store["show_plot"] = False

    if st.button("Reveal Actual Count"):
        store["reveal_count"] = True

    if st.button("Hide Actual Count"):
        store["reveal_count"] = False

# ----------------------------------------
# 7) DISPLAY THE HISTOGRAM (IF ENABLED)
# ----------------------------------------
if store["show_plot"] and len(store["guesses"]) > 0:
    all_guesses = np.array(list(store["guesses"].values()))
    mean_guess = np.mean(all_guesses)
    median_guess = np.median(all_guesses)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(all_guesses, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)

    # Show mean & median
    ax.axvline(mean_guess, color='green', linestyle='-', linewidth=2,
               label=f"Mean: {mean_guess:.0f}")
    ax.axvline(median_guess, color='green', linestyle=':', linewidth=2,
               label=f"Median: {median_guess:.0f}")

    # Show actual line only if reveal_count == True
    if store["reveal_count"]:
        ax.axvline(ACTUAL_COUNT, color='red', linestyle='--', linewidth=2,
                   label=f"Actual: {ACTUAL_COUNT}")

    ax.set_title("Distribution of Guesses")
    ax.set_xlabel("Guess")
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)
