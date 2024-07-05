import random

# List of words
words = ["python", "java", "javascript", "ruby"]

# Function to select a random word
def select_word():
    return random.choice(words)

# Function to display the current game state
def display_state(guessed_word, guessed_letters, lives):
    print(f"Lives: {lives}")
    print(f"Guessed word: {' '.join(guessed_word)}")
    print(f"Guessed letters: {', '.join(guessed_letters)}")

# Function to check if the word is guessed
def is_word_guessed(guessed_word):
    return '_' not in guessed_word

# Main game function
def play_game():
    word = select_word()
    guessed_word = ['_' for _ in word]
    guessed_letters = []
    lives = 6

    while lives > 0 and not is_word_guessed(guessed_word):
        display_state(guessed_word, guessed_letters, lives)
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            lives -= 1
            print("Incorrect guess!")

    if is_word_guessed(guessed_word):
        print(f"Congratulations! You guessed the word: {word}")
    else:
        print(f"Sorry, you lost! The word was: {word}")

# Run the game
if __name__ == "__main__":
    play_game()