import os
import uvicorn

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/upload_file/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = os.path.join("./data", file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "path": file_path}


@app.get("/")
async def main():
    content = """
    <html>
        <body>
            <h1>Upload File</h1>
            <form action="/upload_file/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=23333)
