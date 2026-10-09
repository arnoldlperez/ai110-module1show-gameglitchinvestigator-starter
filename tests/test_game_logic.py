from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# FIX: check_guess returns (outcome, message), so the starter tests unpack the outcome.
# Claude Code suggested the unpacking and generated the two hint-message tests below

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug fix: a guess of 60 against a secret of 50 used to say "Go HIGHER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug fix: a guess of 40 against a secret of 50 used to say "Go LOWER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

# Tests below were generated with Claude Code for the remaining bug fixes

def test_single_digit_secret_compares_as_number():
    # Bug fix: on even attempts the secret was a string, so 50 vs "9" compared as text
    outcome, message = check_guess(50, 9)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_hard_range_is_wider_than_normal():
    # Bug fix: Hard was 1-50, smaller (easier) than Normal's 1-100
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high

def test_parse_guess_rejects_decimal():
    # Bug fix: "3.7" used to be cut down to 3 without warning
    ok, value, err = parse_guess("3.7")
    assert not ok
    assert value is None
    assert err

def test_parse_guess_rejects_out_of_range():
    ok, _, err = parse_guess("150", 1, 100)
    assert not ok
    assert "1" in err and "100" in err

def test_parse_guess_accepts_valid_number():
    assert parse_guess(" 42 ", 1, 100) == (True, 42, None)

def test_parse_guess_rejects_empty_and_text():
    assert parse_guess("")[0] is False
    assert parse_guess("abc")[0] is False

def test_first_try_win_scores_100():
    # Bug fix: win points were off by one attempt, so a first-try win scored 80
    assert update_score(0, "Win", 1) == 100

def test_win_points_never_below_10():
    assert update_score(0, "Win", 20) == 10

def test_too_high_never_adds_points():
    # Bug fix: "Too High" gave +5 on even attempts
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5
