import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase

from rich.console import Console
from rich.theme import Theme

console = Console(width=100, theme=Theme({"warning": "red on yellow"}))

NUM_LETTERS = 5
NUM_GUESSES = 6
WORDS_PATH = pathlib.Path(__file__).parent / "wordlist.txt"

def main():
    words_path = pathlib.Path(__file__).parent / "wordlist.txt"
    word = get_random_word(words_path.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * NUM_LETTERS] * NUM_GUESSES

    with contextlib.suppress(KeyboardInterrupt):
        for idx in range(6):
            refresh_page(headline=f"Guess {idx + 1}")
            show_guesses(guesses, word)
            guesses[idx] = guess_word(previous_guesses=guesses[:idx])
            if guesses[idx] == word:
                break
    game_over(guesses, word, guessed_correctly=guesses[idx] == word)

def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")

def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ").upper()
    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.", style="warning")
        return guess_word(previous_guesses)

    if len(guess) != 5:
        console.print("Your guess must be 5 letters.", style="warning")
        return guess_word(previous_guesses)

    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(
            f"Invalid letter: '{invalid}'. Please use English letters.",
            style="warning",
        )
        return guess_word(previous_guesses)

    return guess

def get_random_word(word_list):
    if words := [
        word.upper()
        for word in word_list
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    else:
        console.print("No words of length 5 in the word list", style="warning")
        raise SystemExit()

def show_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print("".join(styled_guess), justify="center")
    console.print("\n" + "".join(letter_status.values()), justify="center")

def game_over(guesses, word, guessed_correctly):
    refresh_page(headline="Game Over")
    show_guesses(guesses, word)

    if guessed_correctly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")

if __name__ == "__main__":
    main()
