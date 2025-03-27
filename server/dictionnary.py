import logging
from abc import ABC
from db import cursor
from typing import Optional
import json

class Word():
    def __init__(self, _word:str, _phonemes:str, _vowels:str, _consonants:str):
        self.word: str = _word
        self.phonemes: list[str] = _phonemes.split()
        self.vowels: list[str] = _vowels.split()
        self.consonants: list[str] = _consonants.split()
    def __repr__(self):
        return f"Word(word='{self.word}', phonemes='{self.phonemes}', vowels='{self.vowels}', consonants='{self.consonants}')"
    async def toDict(self) -> dict:
        return {
            "word": self.word,
            "phonemes": self.phonemes,
            "vowels": self.vowels,
            "consonants": self.consonants
        }

class AbstractRhymeFinder(ABC):
    def __init__(self):
        self.keyDict: dict[str,int] = {}  # key: words, value: pos in rhymeDict
        self.rhymeDict: list[Word] = []
        self.keyDictBig: dict[str,int] = {}
        self.rhymeDictBig: list[Word] = []
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
        cursor.execute('''SELECT word, vowels, phonemes, consonants FROM bigDict ORDER BY vowels, phonemes''')
        rows = cursor.fetchall()
        pos: int = 0
        for row in rows:
            self.keyDictBig[row[0]] = pos
            phonemes = row[2]
            consonants = row[3]
            self.rhymeDictBig.append(Word(row[0], phonemes, row[1], consonants))
            pos += 1

    async def rhymeDictPos(self, word:str) -> int:
        pos = self.keyDict[word]
        return pos

    async def getBasicRhymes(self, word:str, pos: int) -> tuple[list[Word], int]:
        posmin = pos -1
        posmax = pos +1
        end_vowel = self.rhymeDict[posmin].vowels[0]
        while posmin > 0 and self.rhymeDict[posmin-1].vowels[0] == end_vowel:
            posmin -= 1
        while posmax < self.maxPos and self.rhymeDict[posmax+1].vowels[0] == end_vowel:
            posmax += 1
        logging.info(f"posmin: {posmin}")
        logging.info(f"posmax: {posmax}")
        return (self.rhymeDict[posmin:posmax], pos - posmin)

    async def orderRhymesList(self, rhymes: list[Word], wordObj:Word, pos:int) -> list[Word]:
        posmin = pos -1
        posmax = pos +1
        minList = rhymes[0:posmin+1]
        maxList = rhymes[:posmax-1:-1]
        matchPhonemes = (wordObj.phonemes[0], wordObj.phonemes[1])
        matchConsonant = wordObj.consonants[0]
        refined: list[Word] = []
        # c++ remove phonemes if size < 2
        while (minList[-1].phonemes[0], minList[-1].phonemes[1]) == matchPhonemes:
            refined.append(minList.pop())
        while (maxList[-1].phonemes[0], maxList[-1].phonemes[1]) == matchPhonemes:
            refined.append(maxList.pop())
        while len(minList) != 0 or len(maxList) != 0:
            if len(minList) != 0:
                refined.append(minList.pop())
            if len(maxList) != 0:
                refined.append(maxList.pop())
        logging.info(f"len: {len(refined)}")
        return refined

class RhymeFinder(AbstractRhymeFinder):
    def __init__(self):
        super().__init__()

    async def findWord(self, word:str) -> Word:
        pos = await self.rhymeDictPos(word)
        return self.rhymeDict[pos]
    
    async def findRhymesWord(self, word:str):
        pos = self.keyDict[word]
        wordObj = self.rhymeDict[pos]
        rhymes, pos = await self.getBasicRhymes(word, pos)
        if len(wordObj.phonemes) >= 2:
            rhymes = await  self.orderRhymesList(rhymes, wordObj, pos)
        return rhymes, wordObj

    async def findRhymes(self, word:str):
        pos = self.keyDict[word]
        wordObj = self.rhymeDict[pos]
        rhymes, pos = await self.getBasicRhymes(word, pos)
        if len(wordObj.phonemes) >= 2:
            rhymes = await  self.orderRhymesList(rhymes, wordObj, pos)
        return rhymes
