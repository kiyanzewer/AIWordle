# Used online API sites to find how to make words colored - installed rich using python3 -m install rich
from rich.console import Console
from random import choice
from collections import defaultdict
import pandas as pd
from enum import Enum

class Information(Enum):
    GREEN = 0
    YELLOW = 1
    RED = 2
def calcLetterFrequencies(dictionary):
    counts = defaultdict(int)
    for word in dictionary:
        for char in word:
            counts[char] += 1

    return {char : counts[char] / (len(dictionary) * 5) for char in counts}

def calcLetterFrequenciesByPosition(dictionary):
    counts = defaultdict(lambda : [0,0,0,0,0])
    for word in dictionary:
        for i, char in enumerate(word):
            counts[char][i] += 1

    return {char : [count / (len(dictionary) * 5) for count in counts[char]] for char in counts}

def buildDF(dictionary):
    dictionary = [[char for char in word]+[word] for word in dictionary]
    return pd.DataFrame(dictionary).rename(columns={5:"word"})


# function to properly assign colors to letters
def checkWord(answer, word):
    input = [""] * 5
    counts = defaultdict(int)
    # loop through each letter in the answer
    for i, letter in enumerate(answer):
        # letter is in the word and in the correct position
        if letter == word[i]:
            # uses rich to color the letter green
            counts[letter] += 1
            input[i] = f'[black on green]{letter}[/]'
        # letter is in the word but in the wrong position
    
    for i, letter in enumerate(answer):
        if letter in word and input[i] == "":
            # uses rich to color the letter yellow
            counts[letter] += 1
            if counts[letter] <= word.count(letter):
                input[i] = f'[black on yellow]{letter}[/]'
            else:
                input[i] = f'[black on red]{letter}[/]'
        # letter is not in the word
        elif input[i] == "":
            # uses rich to color the letter red
            input[i] = f'[black on red]{letter}[/]'

    return "".join(input)

def evaluateInformation(answer, word):
    information = [""] * 5
    counts = defaultdict(int)
    # loop through each letter in the answer
    for i, letter in enumerate(answer):
        # letter is in the word and in the correct position
        if letter == word[i]:
            counts[letter] += 1
            information[i] = (letter, Information.GREEN)

    for i, letter in enumerate(answer):
        # letter is in the word but in the wrong position
        if letter in word and information[i] == "":
            if counts[letter] < word.count(letter):
                counts[letter] += 1
                information[i] = (letter, Information.YELLOW)
            else:
                information[i] = (letter, Information.RED)
        # letter is not in the word
        elif information[i] == "":
            information[i] = (letter, Information.RED)
    information.append(counts)
    return information

def getRemainingFromInformation(df, information, current_guess):
    counts = information.pop()
    for letter in counts:
        df = df[(df["word"].str.count(letter)) >= counts[letter]]
        if current_guess.count(letter) > counts[letter]:
            df = df[(df["word"].str.count(letter)) < current_guess.count(letter)]

    for i, info in enumerate(information):
        letter = info[0]
        confidence = info[1]
        if confidence == Information.GREEN:
            df = df[df[i] == letter]
        elif confidence == Information.YELLOW:
            df = df[(df["word"].str.contains(letter)) & (df[i] != letter)]
        elif confidence == Information.RED:
            if letter not in counts:
                df = df[~df["word"].str.contains(letter)]
    return df

def scoreWordsFromDF(df):
    words = list(df["word"])
    scores = []
    value_counts = [df[i].value_counts() for i in range(5)]
    for word in words:
        curr_score = 0
        for i, letter in enumerate(word):
            curr_score += value_counts[i][letter]
        scores.append((curr_score, word))
    scores.sort(reverse=True)
    return scores
        


if __name__ == "__main__":
    console = Console()
    words = []
    # put words in words.txt into a list
    # list was found online at https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/ca9018b32e963292473841fb55fd5a62176769b5/valid-wordle-words.txt
    # with open('words.txt') as f:
    # list was found online at https://www.wordunscrambler.net/word-list/wordle-word-list
    with open('wordleList.txt') as f:
        # add words uppercase to list
        words = [word.upper() for word in f.read().splitlines()]

    freqs = calcLetterFrequencies(words)
    freqs_by_pos = calcLetterFrequenciesByPosition(words)

    df = buildDF(words)
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

    scored_words = scoreWordsFromDF(df)
    print(f"Recommended guess: {scored_words[0][1]}")

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
        inputs.append(answer)
        guesses += 1
        inp = checkWord(answer, word)
        df = getRemainingFromInformation(df, evaluateInformation(answer, word), answer)
        print(df.head(100))
        scored_words = scoreWordsFromDF(df)
        print(f"Recommended guess: {scored_words[-1][1]}")
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