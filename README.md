# Wordle FSM Assignment

This project is a console-based Wordle simulator in Python where round flow is controlled by a Finite State Machine (FSM).

## How to run

```bash
python3 wordle_fsm.py
```

## FSM design used in `PlayRound()`

The round state is represented by an `Enum` (`RoundState`) with these states:
- `WORD_ENTRY`
- `CONFIRM`
- `SCORE`
- `IS_WINNER`
- `REVIEW`
- `CONFIRM_AFTER_REVIEW`
- `DISPLAY`

No boolean variable is used to represent FSM state.

## Manual tests performed

1. **Invalid word length and non-letter input**
   - Entered values such as `ab`, `abcdef`, `12abc`
   - Verified game stays in word-entry state and asks again.

2. **Confirm No path**
   - Entered valid guess `crate`, answered `n` at confirmation.
   - Verified transition back to word-entry to re-enter guess.

3. **Winning path**
   - Entered secret word `crane`, answered `y`.
   - Verified attempt count increments, winner is detected, and `Display()` shows `You Won.`

4. **Losing path (6 attempts)**
   - Entered six incorrect guesses and confirmed each.
   - Verified round ends after attempt 6 and `Display()` shows `You Lost.`

5. **Review feedback path**
   - Entered a non-winning guess and confirmed.
   - Verified review prints letters present in secret and correct-position letters, then continues to next guess.
