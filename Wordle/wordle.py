# Used online API sites to find how to make words colored - installed rich using python3 -m install rich
from rich.console import Console
from random import choice
from words import dictionary

# these 3 functions use the rich library to color the letters
def correctLetterAndPosition(letter):
    return f'[black on green]{letter}[/]'

def correctLetterWrongPosition(letter):
    return f'[black on yellow]{letter}[/]'

def wrongLetter(letter):
    return f'[black on red]{letter}[/]'

# function to properly assign colors to letters
def checkWord(answer, word):
    input = []
    # loop through each letter in the answer
    for i, letter in enumerate(answer):
        # letter is in the word and in the correct position
        if letter == word[i]:
            input += correctLetterAndPosition(letter)
        # letter is in the word but in the wrong position
        elif letter in word:
            input += correctLetterWrongPosition(letter)
        # letter is not in the word
        else:
            input += wrongLetter(letter)
    return input

if __name__ == "__main__":
    console = Console()
    # choose a random word from the list
    word = choice(dictionary).upper()
    # print dashes across console
    for i in range(100):
        print('-', end='')
    # start console with message
    console.print("\nWelcome to CS 4710 Wordle")
    for i in range(100):
        print('-', end='')
    # instructions
    console.print("\nINSTRUCTIONS:\nWordle is a game where you have six attempts at guessing the random five letter word. \nEach attempt gives a hint to the user if each letter is used at all and if it is in the correct position.  \nIf the letter is green, it is used and in the corerect position. \nIf the letter is yellow, it is used but not in the correct position. \nIf the letter is red, it is not used at all. \nGood luck!")
    for i in range(100):
        print('-', end='')
    # start game
    console.print("\nTime to play!")
    winner = False
    loser = False
    inputs = []
    guesses = 0
    # upper case every dictionary word
    dictionary = [i.upper() for i in dictionary]
    # loop to print dictionary
    while not winner and not loser:
        # get user input
        answer = input("Guess a five letter word: ")
        answer = answer.upper()
        # check if user input is valid
        while len(answer) != 5 or answer in inputs or answer not in dictionary or not answer.isalpha():
            if len(answer) != 5:
                answer = input("Please enter a five letter word: ")
            elif answer in inputs:
                answer = input("You already guessed that word. Please enter a different word: ")
            elif not answer.isalpha():
                answer = input("Please enter a word with only letters: ")
            elif answer not in dictionary:
                answer = input("That word is not in the dictionary. Please enter a different word: ")
            answer = answer.upper()
        # check if user input has already been guessed
        if answer in inputs:
            console.print("You already guessed that word, try again")
        else:
            inputs.append(answer)
            guesses += 1
            inp = checkWord(answer, word)
            console.print(f"Guesses: {guesses}/6")
            console.print(''.join(inp))
            # check if user input is correct
            if answer == word:
                winner = True
            elif guesses == 6:
                loser = True
    if winner:
        console.print("You won!")
    else:
        console.print("You lost!")