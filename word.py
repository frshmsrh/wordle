from letter import Letter  # Assuming Letter is a class defined in letter.py

class Word:
    def __init__(self, word):
        self.word_solved = []

        # Initialize list of Letter objects for each character in the word
        for char in word:
            new_letter = Letter(char)
            self.word_solved.append(new_letter)

    # Display the current solved state of the word as a string (e.g., "F o _ _ _ u _ d")
    def word_current(self):
        word_string = ""
        for letter in self.word_solved:
            word_string += letter.display() + " "
        return word_string.strip()

    # Check the user's guessed letter against the word
    def word_check(self, guess):
        for letter in self.word_solved:
            if letter.check(guess):
                return True
        return False
