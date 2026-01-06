from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

logging.basicConfig(
    level = logging.INFO,
    format="[%(asctime)s] (line %(lineno)d) - %(levelname)s - %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S"
)

@app.exception_handler(Exception)
def handle(req:Request,ex:Exception):
    return JSONResponse(content ={
        'status_code' : 500,
        'status_message' : str(ex)
    })


@app.get('/')
async def debug():
    logging.info('---')
    return 1/0