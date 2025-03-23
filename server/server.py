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
from dictionnary import RhymeFinder

''' ------------------------------------------------------ PRECONFIG ------------------------------------------------------ '''

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="../static"), name="static")

VALID_WORDS = fetchValidWords()
rhyme_finder = RhymeFinder()

with open(os.path.join(PROJECT_DIR, "server/logging/server.log"), "w") as file:
    file.write("")
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler(os.path.join(PROJECT_DIR, "server/logging/server.log"), mode='a')],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

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
    rhymes, wordObj = await rhyme_finder.findRhymes(word)
    html_content =  await HtmlResponse.buildSearchResultsPage(wordObj=wordObj, rhymes=rhymes)
    return responses.HTMLResponse(content=html_content)

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)
