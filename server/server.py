from fastapi import FastAPI, Response, responses, staticfiles
import uvicorn
import logging
import sys
import os
from typing import Optional
import mariadb
from abc import ABC

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import cursor
from const import HOST, PORT, PROJECT_DIR
from getValidWords import fetchValidWords
from htmlResponse import HtmlResponse

''' ------------------------------------------------------ PRECONFIG ------------------------------------------------------ '''

app = FastAPI()

app.mount("/static", staticfiles.StaticFiles(directory="../static"), name="static")

VALID_WORDS = fetchValidWords()

with open(os.path.join(PROJECT_DIR, "server/logging/server.log"), "w") as file:
    file.write("")

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler(os.path.join(PROJECT_DIR, "server/logging/server.log"), mode='a')],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logging.debug("This is a debug message")
logging.info("This is an info message")

''' Cached Dictionnaries '''

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

rhyme_finder = RhymeFinder()

''' ------------------------------------------------------  ENDPOINTS ------------------------------------------------------ '''

@app.get("/")
async def home():
    index_path = os.path.join(PROJECT_DIR, "static/html/index.html")
    with open(index_path, "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)

@app.get("/search/{word}")
async def search(word:str):
    word = word.upper()
    logging.info(f"received string: {word}")
    if word not in VALID_WORDS:
        return Response(content="Error: word not found in database", status_code=400)
    search_path = PROJECT_DIR + "static/html/search.html"
    resp = await rhyme_finder.findRhymes(word)
    html_content = "<ul>" + "".join([f"<li>{rhyme.word}</li>" for rhyme in resp]) + "</ul>"
    return responses.HTMLResponse(content=html_content)

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)
