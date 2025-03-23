import logging
from abc import ABC
from db import cursor
from typing import Optional

class Word():
    def __init__(self, _word:str, _phonemes:str, _vowels:str, _consonants:str):
        self.word: str = _word
        self.phonemes: list[str] = _phonemes.split()
        self.vowels: list[str] = _vowels.split()
        self.consonants: list[str] = _consonants.split()
    def __repr__(self):
        return f"Word(word='{self.word}', phonemes='{self.phonemes}', vowels='{self.vowels}', consonants='{self.consonants}')"

class AbstractRhymeFinder(ABC):
    def __init__(self):
        self.keyDict: dict[str,int] = {}  # key: words value: pos
        self.rhymeDict: list[Word] = [] # word object with rhymes consonants etc
        self.buildDictionnaries()
        self.maxPos:int = len(self.rhymeDict)-1

    def buildDictionnaries(self):
        cursor.execute('''SELECT word, vowels, phonemes, consonants FROM smallDict ORDER BY vowels, phonemes''')
        rows = cursor.fetchall()
        pos: int = 0
        for row in rows:
            self.keyDict[row[0]] = pos
            phonemes = row[2]
            consonants = row[3]
            self.rhymeDict.append(Word(row[0], phonemes, row[1], consonants))
            pos += 1

    async def rhymeDictPos(self, word:str) -> int:
        pos = self.keyDict[word]
        logging.info("still here")
        logging.info(f"pos: {pos}")
        return pos

    async def getBasicRhymes(self, word:str, pos: int):
        posmin = pos -1
        posmax = pos +1
        end_vowel = self.rhymeDict[posmin].vowels[0]
        while posmin > 0 and self.rhymeDict[posmin-1].vowels[0] == end_vowel:
            posmin -= 1
        while posmax < self.maxPos and self.rhymeDict[posmax+1].vowels[0] == end_vowel:
            posmax += 1
        return (self.rhymeDict[posmin:posmax], pos - posmin)

    async def orderRhymesList(self, rhymes: list[Word], wordObj:Word, pos:int):
        posmin = pos -1
        posmax = pos +1
        maxpos = len(rhymes) -1
        refined: list[Word] = []
        matchPhonemes = (wordObj.phonemes[0], wordObj.phonemes[1])
        while posmin > 0 and (rhymes[posmin].phonemes[0], rhymes[posmin].phonemes[1]) == matchPhonemes:
            refined.append(rhymes[posmin])
            posmin -= 1
        while posmax < maxpos and (rhymes[posmax].phonemes[0], rhymes[posmax].phonemes[1]) == matchPhonemes:
            refined.append(rhymes[posmax])
            posmax += 1
        while True:
            if posmin < 0 and posmax > maxpos:
                break
            if posmin >= 0:
                refined.append(rhymes[posmin])
                posmin -= 1
            if posmax <= maxpos:
                refined.append(rhymes[posmax])
                posmax += 1
        logging.info("!!! RHYMES REFINED !!!")
        logging.info(f"len: {len(refined)}")
        return refined

class RhymeFinder(AbstractRhymeFinder):
    def __init__(self):
        super().__init__()

    async def findPhonemes(self, word:str, phonemes: Optional[list[str]]=None):
        pass

    async def findRhymes(self, word:str, phonemes: Optional[list[str]]=None):
        pos = self.keyDict[word]
        wordObj = self.rhymeDict[pos]
        rhymes, pos = await self.getBasicRhymes(word, pos)
        if len(wordObj.phonemes) >= 2:
            rhymes = await  self.orderRhymesList(rhymes, wordObj, pos)
        logging.info(rhymes)
        return rhymes
