import random
import streamlit as st

# FIX: Refactored all game logic into logic_utils.py using Claude Code agent mode
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_new_game():
    # FIX: New Game only reset attempts and the secret, so status stayed "won"/"lost"
    # and the game was stuck. Claude Code moved the reset into one helper that clears
    # everything and picks the secret from the current difficulty's range (was always 1-100)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty


# FIX: Attempts started at 1 (but New Game reset them to 0), so a fresh game had one
# attempt too few. Every game now starts through start_new_game() with attempts = 0
if "secret" not in st.session_state:
    start_new_game()

# FIX: Switching difficulty kept the old secret, which could be outside the new range
if st.session_state.get("difficulty") != difficulty:
    start_new_game()

st.subheader("Make a guess")

# FIX: The banner was drawn before the guess was counted, so "Attempts left" lagged
# one guess behind. It is now a placeholder filled in after the guess is handled
info_box = st.empty()


def show_attempts_left():
    # FIX: The banner always said "between 1 and 100"; it now uses the difficulty's range
    info_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )


with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game()
    st.rerun()

if st.session_state.status != "playing":
    show_attempts_left()
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: Invalid input used to count as an attempt; it now only shows the error
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: On even attempts the secret was turned into a string, so a correct guess
        # couldn't win and hints compared text ("50" < "9"). It is always an int now
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

show_attempts_left()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
