import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import string

# -----------------------------------------------------
# 1. SHARED GLOBAL DATA STORE (in-memory for all users)
# -----------------------------------------------------
@st.cache_resource
def get_global_data():
    """A dictionary mapping user session_ids -> their submitted guess."""
    return {}

# -----------------------------------------------------
# 2. GENERATE/RETRIEVE A UNIQUE SESSION ID FOR EACH USER
# -----------------------------------------------------
def get_session_id():
    """Creates a unique ID and stores it in st.session_state (one per user)."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
    return st.session_state.session_id

# -----------------------------------------------------
# 3. STREAMLIT APP SETUP
# -----------------------------------------------------
st.set_page_config(page_title="Guess the Jar Count", layout="wide")

ACTUAL_COUNT = 735  # The real number in the jar

# Initialize toggles
if "show_plot" not in st.session_state:
    st.session_state["show_plot"] = False
if "reveal_count" not in st.session_state:
    st.session_state["reveal_count"] = False

# Retrieve the shared data store and a user-specific session_id
global_data = get_global_data()
session_id = get_session_id()

# -----------------------------------------------------
# 4. TWO-COLUMN LAYOUT
# -----------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    # Title and image
    st.title("Guess the Number of Items in the Jar!")
    st.markdown(
        """
        <div style='text-align: center;'>
            <!-- Make sure "image.jpg" is actually in the same folder as app.py -->
            <img src="image.jpg" width="300"/>
            <p><em>How many items do you think are in this 1/2 gallon jar?</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.subheader("Instructions:")
    st.markdown(
        """
        1. Enter your guess below.
        2. Click **Submit Guess**.
        3. Once everyone has guessed, the host clicks **Generate Plot**.
        4. Finally, the host clicks **Reveal Actual Count** to show the real number.
        """
    )

    # Input box for the guess
    guess = st.number_input("Enter your guess:", min_value=0, max_value=100000, value=0)

    # Buttons for actions
    if st.button("Submit Guess"):
        # Store this user's guess in the global dictionary
        global_data[session_id] = guess
        st.success("Your guess has been submitted!")

    if st.button("Generate Plot"):
        if len(global_data) == 0:
            st.warning("No guesses have been submitted yet!")
        else:
            st.session_state["show_plot"] = True

    if st.button("Reveal Actual Count"):
        st.session_state["reveal_count"] = True

# -----------------------------------------------------
# 5. SHOW THE HISTOGRAM (ONLY AFTER 'Generate Plot')
# -----------------------------------------------------
if st.session_state["show_plot"] and len(global_data) > 0:
    # Collect all guesses
    all_guesses = np.array(list(global_data.values()))
    mean_guess = np.mean(all_guesses)
    median_guess = np.median(all_guesses)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(all_guesses, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)

    # Mean & median lines
    ax.axvline(mean_guess, color='green', linestyle='-', linewidth=2,
               label=f"Mean: {mean_guess:.0f}")
    ax.axvline(median_guess, color='green', linestyle=':',
               linewidth=2, label=f"Median: {median_guess:.0f}")

    # The actual number is revealed ONLY if st.session_state["reveal_count"] is True
    if st.session_state["reveal_count"]:
        ax.axvline(ACTUAL_COUNT, color='red', linestyle='--', linewidth=2,
                   label=f"Actual: {ACTUAL_COUNT}")

    ax.set_title("Distribution of Guesses")
    ax.set_xlabel("Guesses")
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)
