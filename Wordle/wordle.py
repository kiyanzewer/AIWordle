# Used online API sites to find how to make words colored - installed rich using python3 -m install rich
from rich.console import Console
from random import choice

# function to properly assign colors to letters
def checkWord(answer, word):
    input = []
    # loop through each letter in the answer
    for i, letter in enumerate(answer):
        # letter is in the word and in the correct position
        if letter == word[i]:
            # uses rich to color the letter green
            input += f'[black on green]{letter}[/]'
        # letter is in the word but in the wrong position
        elif letter in word:
            # uses rich to color the letter yellow
            input += f'[black on yellow]{letter}[/]'
        # letter is not in the word
        else:
            # uses rich to color the letter red
            input += f'[black on red]{letter}[/]'
    return input

if __name__ == "__main__":
    console = Console()
    words = []
    # put words in words.txt into a list
    # list was found online at https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/ca9018b32e963292473841fb55fd5a62176769b5/valid-wordle-words.txt
    with open('words.txt') as f:
        # add words uppercase to list
        words = [word.upper() for word in f.read().splitlines()]
    word = choice(words)
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
    dictionary = [i.upper() for i in words]
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
        console.print("You lost! The word was " + word)