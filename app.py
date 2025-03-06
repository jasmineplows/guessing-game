import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import string

# -----------------------
# SHARED GLOBAL DATA STORE
# -----------------------
@st.cache_resource
def get_global_data():
    """Returns a dictionary {session_id -> guess} shared across all active user sessions."""
    return {}

# -----------------------
# HELPERS
# -----------------------
def get_session_id():
    """Assign a random session ID to each user session (stored in st.session_state)."""
    if "session_id" not in st.session_state:
        # Generate a random 8-character string for this session
        st.session_state.session_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
    return st.session_state.session_id


# -----------------------
# STREAMLIT APP
# -----------------------
st.set_page_config(page_title="Guess the Jar Count", layout="wide")

ACTUAL_COUNT = 735

# Initialize toggle states
if "show_plot" not in st.session_state:
    st.session_state["show_plot"] = False
if "reveal_count" not in st.session_state:
    st.session_state["reveal_count"] = False

# Get or create the shared global data
global_data = get_global_data()

# Each user gets a unique session ID
session_id = get_session_id()

# Create columns
col_left, col_right = st.columns([2, 1])

with col_left:
    st.title("Guess the Number of Items in the Jar!")
    st.markdown(
        """
        <div style='text-align: center;'>
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
        3. Once everyone has guessed, the host clicks **Generate Plot** to show the guesses.
        4. Finally, the host clicks **Reveal Actual Count** to show the real number.
        """
    )

    guess = st.number_input("Enter your guess:", min_value=0, max_value=100000, value=0)

    # SUBMIT GUESS
    if st.button("Submit Guess"):
        global_data[session_id] = guess  # store (or overwrite) this session's guess
        st.success("Your guess has been submitted!")

    # GENERATE PLOT (host action)
    if st.button("Generate Plot"):
        if len(global_data) == 0:
            st.warning("No guesses have been submitted yet!")
        else:
            st.session_state["show_plot"] = True

    # REVEAL ACTUAL COUNT (host action)
    if st.button("Reveal Actual Count"):
        st.session_state["reveal_count"] = True


# DISPLAY THE HISTOGRAM IF "Generate Plot" WAS CLICKED
if st.session_state["show_plot"] and len(global_data) > 0:
    # Collect all guesses
    all_guesses = np.array(list(global_data.values()))
    mean_guess = np.mean(all_guesses)
    median_guess = np.median(all_guesses)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(all_guesses, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)

    # Plot mean and median
    ax.axvline(mean_guess, color='green', linestyle='-', linewidth=2,
               label=f"Mean: {mean_guess:.0f}")
    ax.axvline(median_guess, color='green', linestyle=':',
               linewidth=2, label=f"Median: {median_guess:.0f}")

    # Reveal the actual count if requested
    if st.session_state["reveal_count"]:
        ax.axvline(ACTUAL_COUNT, color='red', linestyle='--', linewidth=2,
                   label=f"Actual: {ACTUAL_COUNT}")

    ax.set_title("Distribution of Guesses")
    ax.set_xlabel("Guesses")
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)
