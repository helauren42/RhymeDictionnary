from fastapi import FastAPI, Response, responses, staticfiles
import uvicorn
import logging
import sys
import os
from typing import Optional
import mariadb
from abc import ABC

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from const import HOST, PORT, PROJECT_DIR
from getValidWords import fetchValidWords
from utils import fetchAccountInfo

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

''' MARIADB '''

try:
    conn_params = {
        'user' : f"{fetchAccountInfo('DB_USER')}",
        'password' : f"{fetchAccountInfo('DB_PASSWORD')}",
        'host' : "127.0.0.1",
        'port' : 3306,
        'database' : "rd"
    }

    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
except Exception as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

''' Cached Dictionnaries '''

class Word():
    def __init__(self, _word:str, _phonemes:str, _vowels:str, _consonants:str):
        self.word: list[str] = _word.split()
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

    def rhymeDictPos(self, word:str) -> int:
        pos = self.keyDict[word]
        logging.info("still here")
        logging.info(f"pos: {pos}")
        return pos

    def getBasicRhymes(self, word:str):
        logging.debug("get basic rhymes called")
        posmin = self.rhymeDictPos(word)
        posmax = posmin
        end_vowel = self.rhymeDict[posmin].vowels[0]
        logging.info(f"end_vowel:  {end_vowel}")
        while posmin > 0 and self.rhymeDict[posmin-1].vowels[0] == end_vowel:
            posmin -= 1
        logging.info(f"next word: {self.rhymeDict[posmax+1]}")
        logging.info(f"{self.maxPos}")
        while posmax < self.maxPos and self.rhymeDict[posmax+1].vowels[0] == end_vowel:
            posmax += 1
        logging.info(f"posmin:  {posmin}")
        logging.info(f"posmax:  {posmax}")
        return self.rhymeDict[posmin:posmax]

class RhymeFinder(AbstractRhymeFinder):
    def __init__(self):
        super().__init__()

    def findRhymes(self, word:str, phonemes: Optional[list[str]]=None):
        logging.debug("here")
        rhymes = self.getBasicRhymes(word)
        logging.info(rhymes)
        return rhymes

rhyme_finder = RhymeFinder()

''' ------------------------------------------------------  ENDPOINTS  ------------------------------------------------------ '''

@app.get("/")
async def home():
    index_path = os.path.join(PROJECT_DIR, "static/html/index.html")
    with open(index_path, "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)

@app.get("/search/{word}")
async def search(word:str):
    word = word.upper()
    print(f"received string: {word}")
    logging.info(f"received string: {word}")
    if word not in VALID_WORDS:
        return Response(content="Error: word not found in database", status_code=400)
    search_path = os.path.join(PROJECT_DIR, "static/html/search.html")
    resp = rhyme_finder.findRhymes(word)
    html_content = "<ul>" + "".join([f"<li>{rhyme}</li>" for rhyme in resp]) + "</ul>"
    return responses.HTMLResponse(content=html_content)

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)
