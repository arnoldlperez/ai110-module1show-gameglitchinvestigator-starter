# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Purpose:** A Streamlit number guessing game. The player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–200), then guesses the secret number within a limited number of attempts. After each guess the game says "Go HIGHER!" or "Go LOWER!", and the score goes down 5 for each wrong guess and up for a win (more points for fewer attempts).

**Bugs found and fixes applied:**

| Bug | Fix |
|---|---|
| Hints were backwards ("Too High" said "Go HIGHER!") | Swapped the hint messages in `check_guess` |
| On even attempts the secret was turned into a string, so a correct guess couldn't win and hints compared text | Always compare the secret as a number |
| New Game didn't reset status, score, or history, so the game stayed on "Game over"; the new secret was always 1–100 | New `start_new_game()` resets everything and uses the difficulty's range |
| Attempts started at 1, so a fresh game had one attempt too few | Attempts start at 0 |
| Invalid input like "abc" used up an attempt | Only valid guesses count |
| Banner always said "between 1 and 100" and "Attempts left" lagged one guess behind | Banner uses the real range and updates after the guess |
| Hard (1–50) was easier than Normal (1–100) | Hard is now 1–200 |
| Win score was off by one attempt; "Too High" gave +5 on even attempts | First-try win scores 100; every wrong guess costs 5 |
| "3.7" became 3 without warning; out-of-range guesses were accepted | Both are rejected with a message |
| Changing difficulty kept the old secret | Changing difficulty starts a new game |
| Buttons lagged or missed the first click; Debug Info showed the previous turn | Guess input is in a `st.form`; Debug Info updates after the guess |

All game logic was moved from `app.py` into `logic_utils.py` so it can be tested with pytest.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the game on Normal. The banner says "Guess a number between 1 and 100. Attempts left: 8" (the secret in this example is 63).
2. Enter a guess of 40 → "Go HIGHER!", score -5, attempts left 7.
3. Enter a guess of 80 → "Go LOWER!", score -10, attempts left 6.
4. Enter "abc" → "Enter a whole number." The attempt isn't counted, so attempts left stays at 6.
5. Enter 63 → "Correct!", balloons, and "You won! The secret was 63. Final score: 70" (80 points for winning on attempt 3, minus 10).
6. Click New Game → score 0, history cleared, "Attempts left: 8", and a new secret.

## 🧪 Test Results

```
$ python -m pytest -v
collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 28%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 35%]
tests/test_game_logic.py::test_single_digit_secret_compares_as_number PASSED [ 42%]
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED    [ 50%]
tests/test_game_logic.py::test_parse_guess_rejects_decimal PASSED        [ 57%]
tests/test_game_logic.py::test_parse_guess_rejects_out_of_range PASSED   [ 64%]
tests/test_game_logic.py::test_parse_guess_accepts_valid_number PASSED   [ 71%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_and_text PASSED [ 78%]
tests/test_game_logic.py::test_first_try_win_scores_100 PASSED           [ 85%]
tests/test_game_logic.py::test_win_points_never_below_10 PASSED          [ 92%]
tests/test_game_logic.py::test_too_high_never_adds_points PASSED         [100%]

============================= 14 passed in 0.03s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
