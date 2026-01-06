from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post('/upload')
async def file_upload(file:UploadFile = File(...)):
    content = await file.read()

    return JSONResponse(content ={
        'file_name' : file.filename,
        'content_type': file.content_type,
        'size_bytes': len(content)
    })