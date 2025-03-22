from fastapi import FastAPI, Response, responses, staticfiles
# from fastapi.responses import HTMLResponse, Response
import uvicorn
import logging
import sys
import os
from typing import Optional
import mariadb
from abc import ABC

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from const import HOST, PORT, PROJECT_DIR
from getValidWords import CMU_ENGLISH, IPA_US, fetchValidWords
from utils import fetchAccountInfo

''' ------------------------------------------------------ PRECONFIG ------------------------------------------------------ '''

app = FastAPI()

app.mount("/static", staticfiles.StaticFiles(directory="../static"), name="static")

VALID_WORDS: dict[int, list[str]] = fetchValidWords()

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
    def __init__(self, _word, _phonemes, _vowels, _consonants):
        self.word: str = _word
        self.phonemes: str = _phonemes
        self.vowels: str = _vowels
        self.consonants: str = _consonants
    def __repr__(self):
        return f"Word(word='{self.word}', phonemes='{self.phonemes}', vowels='{self.vowels}', consonants='{self.consonants}')"

class AbstractRhymeFinder(ABC):
    def __init__(self):
        self.keyDict: dict[str:int] = {}  # key: words value: pos
        self.rhymeDict: list[Word] = [] # word object with rhymes consonants etc
        self.buildDictionnaries()

    def buildDictionnaries(self):
        cursor.execute('''SELECT word, vowels, phonemes, consonants FROM dict ORDER BY vowels, phonemes''')
        rows = cursor.fetchall()
        pos: int = 0
        for row in rows:
            self.keyDict[row[0]] = pos
            phonemes = row[2]
            consonants = row[3]
            self.rhymeDict.append(Word(row[0], phonemes, row[1], consonants))
            pos += 1
        # logging.info(self.keyDict)
        logging.info(self.rhymeDict)

    def getRhymeDictKey(self, word:str):
        vowels = self.keyDict[word]
        key = vowels + " | " + word
        return key

class RhymeFinder(AbstractRhymeFinder):
    def __init__(self):
        super().__init__()
    
    def findRhymes(self, word:str):
        pass

rhyme_finder = RhymeFinder()

''' ------------------------------------------------------  FUNCTIONS  ------------------------------------------------------ '''

async def buildSearchResultsPage(word:str):
    cursor.execute('''  ''')
    cursor.execute(f" SELECT phonemes FROM dict WHERE word='{word}' ")
    phonemes = cursor.fetchall()
    print(phonemes)
    logging.info("search word found phonemes: ", phonemes)

''' ------------------------------------------------------  ENDPOINTS  ------------------------------------------------------ '''

@app.get("/")
async def home():
    index_path = os.path.join(PROJECT_DIR, "static/html/index.html")
    with open(index_path, "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)
''',dict_name: str, *phenomes:Optional[str]'''

@app.get("/search/{word}")
async def search(word:str):
    word = word.upper()
    print(f"received string: {word}")
    logging.info(f"received string: {word}")
    if word not in VALID_WORDS[CMU_ENGLISH]:
        return Response(content="Error: word not found in database", status_code=400)
    search_path = os.path.join(PROJECT_DIR, "static/html/search.html")
    with open(search_path, "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)
