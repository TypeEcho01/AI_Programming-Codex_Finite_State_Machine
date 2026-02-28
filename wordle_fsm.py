"""Console Wordle simulator controlled by a finite state machine (FSM).

Run:
    python3 wordle_fsm.py
"""

from __future__ import annotations

from enum import Enum, auto


class RoundState(Enum):
    """All round-level FSM states for one Wordle round."""

    WORD_ENTRY = auto()
    CONFIRM = auto()
    SCORE = auto()
    IS_WINNER = auto()
    REVIEW = auto()
    CONFIRM_AFTER_REVIEW = auto()
    DISPLAY = auto()


class Wordle:
    """A simple console Wordle game using an explicit finite state machine."""

    MAX_ATTEMPTS = 6

    def __init__(self, secret_word: str = "crane") -> None:
        if len(secret_word) != 5 or not secret_word.isalpha():
            raise ValueError("secret_word must be exactly 5 alphabetic letters")

        self.secret_word = secret_word.lower()
        self.attempt_count = 0
        self.has_won = False
        self.attempts: list[str] = []

    def PlayRound(self) -> None:
        """Controls one round via FSM states and transitions."""

        state = RoundState.WORD_ENTRY
        current_guess = ""

        while True:
            if state == RoundState.WORD_ENTRY:
                current_guess = input("Enter a 5-letter guess: ").strip().lower()
                if len(current_guess) == 5 and current_guess.isalpha():
                    state = RoundState.CONFIRM
                else:
                    print("Invalid input. Please enter exactly five letters.")

            elif state == RoundState.CONFIRM:
                proceed = input(f"Use '{current_guess}'? (y/n): ").strip().lower()
                if proceed == "y":
                    state = RoundState.SCORE
                elif proceed == "n":
                    state = RoundState.WORD_ENTRY
                else:
                    print("Please enter 'y' or 'n'.")

            elif state == RoundState.SCORE:
                self.Score(current_guess)
                state = RoundState.IS_WINNER

            elif state == RoundState.IS_WINNER:
                self.has_won = self.IsWinner(current_guess)
                if self.has_won:
                    state = RoundState.DISPLAY
                else:
                    if self.attempt_count >= self.MAX_ATTEMPTS:
                        state = RoundState.DISPLAY
                    else:
                        state = RoundState.REVIEW

            elif state == RoundState.REVIEW:
                present_letters, correct_position_letters = self._review_guess(current_guess)
                print(f"Letters present in secret word: {present_letters}")
                print(
                    "Letters present and in correct position: "
                    f"{correct_position_letters}"
                )
                state = RoundState.CONFIRM_AFTER_REVIEW

            elif state == RoundState.CONFIRM_AFTER_REVIEW:
                input("Press Enter to continue to your next guess...")
                state = RoundState.WORD_ENTRY

            elif state == RoundState.DISPLAY:
                self.Display()
                return

    def Score(self, guess: str) -> None:
        """Updates the attempt count and stores the guess."""

        self.attempt_count += 1
        self.attempts.append(guess)

    def IsWinner(self, guess: str) -> bool:
        """Checks if the guess matches the secret word."""

        return guess == self.secret_word

    def Display(self) -> None:
        """Shows all attempts and final result of the round."""

        print("\n--- Round Results ---")
        print(f"Secret word: {self.secret_word}")
        print("Attempts:")
        if self.attempts:
            for i, attempt in enumerate(self.attempts, start=1):
                print(f"  {i}. {attempt}")
        else:
            print("  (none)")

        print(f"Attempt count: {self.attempt_count}")
        if self.has_won:
            print("You Won.")
        else:
            print("You Lost.")

        input("Press Enter to return to the main menu...")

    def _review_guess(self, guess: str) -> tuple[str, str]:
        """Returns letters present and letters in correct positions for feedback."""

        present = sorted({letter for letter in guess if letter in self.secret_word})
        correct_positions = [
            guess[i] for i in range(5) if guess[i] == self.secret_word[i]
        ]

        present_display = " ".join(present) if present else "(none)"
        correct_display = (
            " ".join(correct_positions) if correct_positions else "(none)"
        )
        return present_display, correct_display


def main() -> None:
    """Main menu loop for playing multiple rounds."""

    while True:
        print("\n=== Wordle Menu ===")
        print("1. Play a round of Wordle")
        print("2. Leave")
        choice = input("Choose an option (1/2): ").strip()

        if choice == "1":
            game = Wordle()
            game.PlayRound()
        elif choice == "2":
            print("Thanks for Playing and come back another time!")
            break
        else:
            print("Invalid menu choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
