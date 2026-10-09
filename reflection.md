# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, it looked like a normal number guessing game, with a difficulty setting in the sidebar, a box to enter guesses, and a "Developer Debug Info" panel that showed the secret number. Once I started playing, it was clear something was off. The hints were backwards: guessing 60 when the secret was 50 told me to go higher. When the game ended, clicking "New Game" didn't let me play again. It still said "Game over" and my guess history stayed, even though the secret number changed. The attempt counter was also off by one, showing 7 attempts left on Normal before I had made a single guess.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `60` (secret `50`) | "Go LOWER!" | "Go HIGHER!" | Hint is giving the incorrect answer |
| Click "New Game" after game ends | Fresh game starts | Still says "Game over" | History does not clear but secret updates|
| Start the game | "Attempts left: 8" | "Attempts left: 7" | Attemps: 1 |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code in VS Code as my AI teammate. One correct suggestion was the hint fix: after I marked `check_guess` with a FIXME, Claude pointed out that the "Go HIGHER!" and "Go LOWER!" messages were swapped, moved `check_guess` into `logic_utils.py`, and swapped them back. I verified it by reviewing the diff and running pytest, and a guess of 60 against a secret of 50 now returns "Too High" with "Go LOWER!". One misleading result was Claude's first check of the live app. It drove the game headlessly, and a guess of 17 against a secret of 16 showed the right hint, which made it look like the hints were fully fixed. But that guess landed on an even attempt, where the app turns the secret into a string, so it only worked because both numbers have two digits. A secret of 9 and a guess of 50 would still compare as text and give the wrong hint, so I treated the hint fix as only partly done. Later, Claude removed the string conversion in `app.py`, and I verified it with a new test that checks a guess of 50 against a secret of 9 returns "Too High".

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I counted a bug as fixed only when a pytest test covering it passed and the game showed the right behavior. After moving `check_guess`, all 3 starter tests failed with errors like `assert ('Too High', '📉 Go LOWER!') == 'Too High'`. That showed the function returns an (outcome, message) pair while the tests expected only the outcome, so the problem was in the tests, not the logic. Claude suggested unpacking the result with `outcome, _ = check_guess(...)` and generated two new tests that check the hint message itself (60 vs. 50 must say "LOWER", 40 vs. 50 must say "HIGHER"). After that, pytest showed `5 passed`. For the rest of the fixes (New Game reset, attempt counter, scoring, difficulty ranges, and input checking), Claude moved all the logic into `logic_utils.py` and generated a test for each logic fix, such as a first-try win scoring 100 and "3.7" being rejected, which brought pytest to `14 passed`. Since New Game and the attempt counter live in the Streamlit UI, Claude also played through the game headlessly: a fresh Normal game showed "Attempts left: 8", "abc" didn't use an attempt, and New Game after a win or loss reset the status, score, and history.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
