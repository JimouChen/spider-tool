import io
import zipfile
import os

import uvicorn
from fastapi import FastAPI, Response

app = FastAPI()

files = ["./data/output.xlsx", "./data/output1.xlsx"]


@app.get("/download_zip")
async def download_zip():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zipf:
        for file in files:
            if os.path.isfile(file):
                zipf.write(file)

    zip_buffer.seek(0)

    headers = {
        "Content-Disposition": "attachment; filename=files.zip",
        "Content-Type": "application/zip"
    }
    return Response(zip_buffer.read(), headers=headers, media_type="application/zip")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
