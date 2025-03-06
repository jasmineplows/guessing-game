import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -- Page config --
st.set_page_config(page_title="Guess the Jar Count", layout="wide")

# -- Initialize session state variables --
if "guesses" not in st.session_state:
    st.session_state["guesses"] = []
if "show_plot" not in st.session_state:
    st.session_state["show_plot"] = False
if "reveal_count" not in st.session_state:
    st.session_state["reveal_count"] = False

ACTUAL_COUNT = 735  # The actual number of items in the jar

# Create two columns: one for the image (col1) and one for the instructions & inputs (col2)
col1, col2 = st.columns([2, 1])  # Adjust ratios [2, 1] as desired

with col1:
    # -- App Title --
    st.title("Guess the Number of Items in the Jar!")

    # -- Display your image/slide --
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src="image.jpg" width="400" />
            <p><em>How many items do you think are in this 1/2 gallon jar?</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        **Instructions**:
        1. Enter your guess in the box below.
        2. Click **Submit Guess**.
        3. Once everyone has guessed, click **Generate Plot** to see the guesses.
        4. Click **Reveal Actual Count** when you're ready to show the real number.
        """
    )

    # -- Input for user guess --
    guess = st.number_input("Enter your guess:", min_value=0, max_value=10000, value=0)

    # -- Button to submit a guess --
    if st.button("Submit Guess"):
        st.session_state["guesses"].append(guess)
        st.success("Your guess has been submitted!")

    # -- Button to show the histogram (without revealing actual count) --
    if st.button("Generate Plot"):
        if len(st.session_state["guesses"]) == 0:
            st.warning("No guesses have been submitted yet!")
        else:
            st.session_state["show_plot"] = True

    # -- Button to reveal the actual count --
    if st.button("Reveal Actual Count"):
        st.session_state["reveal_count"] = True

# -- Show the plot if requested --
if st.session_state["show_plot"] and len(st.session_state["guesses"]) > 0:
    all_guesses = np.array(st.session_state["guesses"])
    mean_guess = np.mean(all_guesses)
    median_guess = np.median(all_guesses)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(all_guesses, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)

    # Mean and median lines (always shown)
    ax.axvline(mean_guess, color='green', linestyle='-', linewidth=2, label=f"Mean: {mean_guess:.0f}")
    ax.axvline(median_guess, color='green', linestyle=':', linewidth=2, label=f"Median: {median_guess:.0f}")

    # Reveal actual count if user clicked "Reveal Actual Count"
    if st.session_state["reveal_count"]:
        ax.axvline(ACTUAL_COUNT, color='red', linestyle='--', linewidth=2, label=f"Actual: {ACTUAL_COUNT}")

    ax.set_title("Distribution of Guesses")
    ax.set_xlabel("Guesses")
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)
