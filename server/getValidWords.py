from enum import Enum

from const import PROJECT_DIR

PATH = PROJECT_DIR + "server/wordLists/"

class DictionaryName(Enum):
    CMU_ENGLISH = 1
    IPA_US = 2

CMU_ENGLISH, IPA_US = (DictionaryName.CMU_ENGLISH, DictionaryName.IPA_US)

WORD_LISTS_FILES = {CMU_ENGLISH: "CMU_english.txt", IPA_US: "ipa_us.txt"}

def fetchValidWords():
    validWords:dict[int, list[str]] = {}
    for key, filename in WORD_LISTS_FILES.items():
        with open(PATH + filename, "r") as file:
            words = file.read().split()
            validWords[key] = words
    return validWords

fetchValidWords()
