from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, responses, staticfiles
import uvicorn
import logging
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from const import HOST, PORT, PROJECT_DIR
from getValidWords import fetchValidWords
from htmlResponse import HtmlResponse
from dictionnary import RhymeFinder, Word

''' ------------------------------------------------------ Cache ------------------------------------------------------ '''

class Cached():
    cached_times:dict[str, float] = {}
    rhymes:dict[str, list[Word]] = {}
    @staticmethod
    async def cacheCleaner():
        while True:
            time.sleep(6)
            await Cached.deleteRhymesLists()
    @staticmethod
    async def deleteRhymesLists():
        now = time.time()
        for word, cached_time in Cached.cached_times.items():
            if now - cached_time > 5:
                Cached.rhymes.pop(word)
    @staticmethod
    async def dictifyWord(rhymes_list: list[Word]) -> list[dict]:
        ret: list[dict] = []
        for wordObj in rhymes_list:
            ret.append(await wordObj.toDict())
        return ret
    @staticmethod
    async def getWord(word: str) -> dict:
        wordObj, pos, small = await rhyme_finder.findWord(word)
        return await wordObj.toDict()
    @staticmethod
    async def getRhymesList(word: str) -> list[dict]:
        try:
            rhyme_list = Cached.rhymes[word]
            logging.info(f"found cached rhymes list")
            return await Cached.dictifyWord(rhyme_list)
        except:
            logging.info(f"rhymes list wss not cached")
            logging.info(f"!!!word: {word}")
            rhyme_list = await rhyme_finder.findRhymes(word)
            return await Cached.dictifyWord(rhyme_list)

''' ------------------------------------------------------ PRECONFIG ------------------------------------------------------ '''

with open(os.path.join(PROJECT_DIR, "server/logging/server.log"), "w") as file:
    file.write("")
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler(os.path.join(PROJECT_DIR, "server/logging/server.log"), mode='a')],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

VALID_WORDS = fetchValidWords()
rhyme_finder = RhymeFinder()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     global VALID_WORDS, rhyme_finder
#     asyncio.create_task(Cached.cacheCleaner())
#     yield

''' ------------------------------------------------------ FASTAPI ------------------------------------------------------ '''

# lifespan=lifespan
app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="../static"), name="static")

''' ENDPOINTS '''

@app.get("/")
async def home():
    index_path = os.path.join(PROJECT_DIR, "static/html/index.html")
    with open(index_path, "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)

@app.get("/getword/{word}")
async def getWord(word:str):
    ret = await Cached.getWord(word)
    return ret

@app.get("/getrhymeslist/{word}")
async def getRhymesList(word:str):
    ret = await Cached.getRhymesList(word)
    return ret

@app.get("/search/{word}")
async def search(word:str):
    word = word.upper()
    logging.info(f"received string: {word}")
    if word not in VALID_WORDS:
        return Response(content="Error: word not found in database", status_code=400)
    rhymes, wordObj = await rhyme_finder.findRhymesWord(word)
    html_content =  await HtmlResponse.buildSearchResultsPage(wordObj=wordObj, rhymes=rhymes)
    return responses.HTMLResponse(content=html_content)

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)
