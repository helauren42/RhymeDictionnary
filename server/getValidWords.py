from enum import Enum

from const import PROJECT_DIR

PATH = PROJECT_DIR + "server/wordLists/CMU_english.txt"

def fetchValidWords():
    with open(PATH, "r") as file:
        words = file.read().split()
        return words

fetchValidWords()
