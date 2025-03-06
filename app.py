import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import string

# -------------------------------------------------
# 1. SHARED GLOBAL DICTIONARY (CACHED)
# -------------------------------------------------
@st.cache_resource
def get_global_store():
    """
    Shared by all sessions:
      store["guesses"]: {session_id -> guess}
      store["show_plot"]: bool - whether the histogram is public
      store["reveal_count"]: bool - whether to show the actual count
    """
    return {
        "guesses": {},
        "show_plot": False,
        "reveal_count": False,
    }

# -------------------------------------------------
# 2. ASSIGN A UNIQUE SESSION ID TO EACH USER
# -------------------------------------------------
def get_session_id():
    if "session_id" not in st.session_state:
        # create a random 8-char string
        st.session_state.session_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
    return st.session_state.session_id

# -------------------------------------------------
# 3. STREAMLIT SETUP
# -------------------------------------------------
st.set_page_config(page_title="Guess the Jar Count", layout="wide")

ACTUAL_COUNT = 735

store = get_global_store()
session_id = get_session_id()

# Are we the host?
if "is_host" not in st.session_state:
    st.session_state["is_host"] = False

def login_as_host():
    """Check password and set is_host = True if correct."""
    pwd = st.session_state.get("host_password_input", "")
    if pwd == "secret123":  # <-- Change this to your chosen password
        st.session_state["is_host"] = True
        st.success("You are now in Host mode!")
    else:
        st.error("Incorrect password!")

# -------------------------------------------------
# 4. LAYOUT
# -------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.title("Guess the Number of Items in the Jar!")
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src="image.jpg" width="250" />
            <p><em>How many items do you think are in this jar?</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.subheader("Instructions (Everyone):")
    st.write(
        """
        1. Enter your guess below.
        2. Click **Submit Guess**.
        3. Wait until the host shares the results!
        """
    )
    
    guess = st.number_input("Enter your guess:", min_value=0, max_value=100000, value=0)
    
    if st.button("Submit Guess"):
        store["guesses"][session_id] = guess
        st.success("Your guess has been submitted!")

    st.write("---")
    # Host login
    st.subheader("Host Login")
    st.text_input("Host Password:", key="host_password_input", type="password")
    if st.button("Login as Host"):
        login_as_host()

# -------------------------------------------------
# 5. HOST CONTROLS
# -------------------------------------------------
if st.session_state["is_host"]:
    st.write("---")
    st.subheader("Host Controls")
    st.markdown(
        """
        You alone can share or hide the histogram for all participants,
        and reveal or hide the actual count (red line).
        """
    )

    # Show/hide public plot
    if st.button("Show Plot to Everyone"):
        if len(store["guesses"]) == 0:
            st.warning("No guesses submitted yet.")
        else:
            store["show_plot"] = True

    if st.button("Hide Plot from Everyone"):
        store["show_plot"] = False

    # Reveal/hide the actual count (735)
    if st.button("Reveal Actual Count to Everyone"):
        store["reveal_count"] = True

    if st.button("Hide Actual Count from Everyone"):
        store["reveal_count"] = False

# -------------------------------------------------
# 6. PUBLIC PLOT (VISIBLE ONLY IF show_plot = True)
# -------------------------------------------------
if store["show_plot"] and len(store["guesses"]) > 0:
    all_guesses = np.array(list(store["guesses"].values()))
    mean_guess = np.mean(all_guesses)
    median_guess = np.median(all_guesses)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(all_guesses, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)

    # Mean & median lines
    ax.axvline(mean_guess, color='green', linestyle='-', linewidth=2,
               label=f"Mean: {mean_guess:.0f}")
    ax.axvli
