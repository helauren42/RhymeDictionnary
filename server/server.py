from click import Option
from fastapi import FastAPI, Response, responses
# from fastapi.responses import HTMLResponse, Response
import uvicorn
import logging
import sys
import os
from typing import Optional
import mariadb

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from const import HOST, PORT, PROJECT_DIR
from getValidWords import CMU_ENGLISH, IPA_US, fetchValidWords
from utils import fetchAccountInfo

''' ------------------------------------------------------ PRECONFIG ------------------------------------------------------ '''

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler(os.path.join(PROJECT_DIR, "server/logging/server.log"))],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
app = FastAPI()

VALID_WORDS = fetchValidWords()

''' MARIADB '''

try:
    # connection parameters
    conn_params = {
        'user' : f"{fetchAccountInfo('DB_USER')}",
        'password' : f"{fetchAccountInfo('DB_PASSWORD')}",
        'host' : "127.0.0.1",
        'port' : 3306,
        'database' : "rd"
    }

    # establish a connection
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

''' ------------------------------------------------------------------------------------------------------------------------ '''

@app.get("/")
async def home():
    index_path = os.path.join(PROJECT_DIR, "static/html/index.html")
    with open(index_path, "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)

''',dict_name: str, *phenomes:Optional[str]'''
@app.get("/search")
async def search(word:str): 
    # empty string handled client side
    if word not in VALID_WORDS:
        return Response(content="Error: word not found in database", status_code=400)
    return

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)

