from fastapi import FastAPI, responses
# from fastapi.responses import HTMLResponse, Response
import uvicorn
import logging
import os

from const import HOST, PORT, PROJECT_DIR

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler(os.path.join(PROJECT_DIR, "server/logging/server.log"))],
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

app = FastAPI()

@app.get("/")
async def home():
    with open(os.path.join(PROJECT_DIR, "static/index.html"), "r") as file:
        content = file.read()
    return responses.HTMLResponse(content=content)

if __name__ == "__main__":
    print(f"host: {HOST}, port: {PORT}")
    uvicorn.run(app="server:app", host=HOST, port=PORT, reload=True)
