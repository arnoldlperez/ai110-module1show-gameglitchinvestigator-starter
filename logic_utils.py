def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Refactored from app.py using Claude Code agent mode.
    # Hard was 1-50, which made it easier than Normal; it is now 1-200
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Refactored from app.py using Claude Code agent mode.
    # Decimals like "3.7" used to be cut down to 3 without warning, and out-of-range
    # guesses were accepted; both are now rejected with a message
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Hint messages were swapped; a guess that is too high now says "Go LOWER!"
    # Claude Code found the swap after I marked it with a FIXME; verified with pytest.
    # The string-comparison fallback was removed because app.py no longer passes the secret as a string
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Refactored from app.py using Claude Code agent mode.
    # A first-try win now scores 100 (it was off by one attempt), and a "Too High"
    # guess no longer earns +5 on even attempts; every wrong guess costs 5
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
