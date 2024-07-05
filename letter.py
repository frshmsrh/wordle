# letter.py

class Letter:
    def __init__(self, char):
        self.char = char
        self.guessed = False

    def display(self):
        if self.guessed:
            return self.char
        else:
            return "_"

    def check(self, guess):
        if guess == self.char:
            self.guessed = True
            return True
        return False
