import os
import time
import uvicorn

from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

USER_UPLOAD_DIR = "static/user_upload"
INIT_IMG=f"{USER_UPLOAD_DIR}/init_girl.jpg"
INIT_VIDEO=f"{USER_UPLOAD_DIR}/init_ww.mp4"


@app.get("/")
async def home() -> RedirectResponse:
    redirect_url = f"/static/home.html?img_url=/{INIT_IMG}&video_url=/{INIT_VIDEO}"
    return RedirectResponse(url=redirect_url)


@app.post("/upload_img/")
async def create_upload_files(img: UploadFile, img_url:str, video_url:str):
    print(img_url, "**"*20, video_url)
    start = time.time()
    new_file_path = f"{USER_UPLOAD_DIR}/{img.filename}"
    try:
        content = await img.read()
        with open(new_file_path, "wb") as f:
            f.write(content)
        msg = {"✅": new_file_path, '耗时(秒)': time.time() - start}
    except Exception as e:
        msg = {"❌": str(e), '耗时(秒)': time.time() - start, '文件': new_file_path}
    redirect_url = f"/static/home.html?img_url=/{new_file_path}&video_url={video_url}"
    print(redirect_url)
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/upload_video/")
async def create_upload_files(video: UploadFile, img_url:str, video_url:str) -> RedirectResponse:
    start = time.time()
    new_file_path = f"{USER_UPLOAD_DIR}/{video.filename}"
    try:
        content = await video.read()
        with open(new_file_path, "wb") as f:
            f.write(content)
        msg = {"✅": new_file_path, '耗时(秒)': time.time() - start}
    except Exception as e:
        msg = {"❌": str(e), '耗时(秒)': time.time() - start, '文件': new_file_path}
    redirect_url = f"/static/home.html?img_url={img_url}&video_url=/{new_file_path}"
    print(redirect_url)
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)





if __name__ == '__main__':
    # uvicorn.run(app=app,host="127.0.0.1", port=8000, reload=True)
    uvicorn.run(app="test:app", host="172.16.14.2", port=8000, reload=True)
