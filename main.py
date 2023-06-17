import os
import time
import uvicorn
import subprocess
import uuid


from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

USER_UPLOAD_DIR = "static/user_upload"
INIT_IMG = f"{USER_UPLOAD_DIR}/init_girl.jpg"
INIT_VIDEO = f"{USER_UPLOAD_DIR}/init_ww.mp4"
INIT_FACE_SWAPED_VIDEO=f"{USER_UPLOAD_DIR}/init_face_swaped.mov"


@app.get("/")
async def home() -> RedirectResponse:
    redirect_url = f"/static/home.html?img_url=/{INIT_IMG}&video_url=/{INIT_VIDEO}"
    return RedirectResponse(url=redirect_url)


@app.post("/upload_img/")
async def create_upload_files(img: UploadFile, img_url: str, video_url: str):
    start = time.time()
    _, file_ext = os.path.split(img.filename)   # 获取上传文件的扩展名 .jpg
    new_file_path = f"{USER_UPLOAD_DIR}/{uuid.uuid1()}{file_ext}"  # 使用uuid作为文件名，避免冲突
    try:
        content = await img.read()
        with open(new_file_path, "wb") as f:
            f.write(content)
        msg = {"✅": new_file_path, '耗时(秒)': time.time() - start}
    except Exception as e:
        msg = {"❌": str(e), '耗时(秒)': time.time() - start, '文件': new_file_path}
    redirect_url = f"/static/home.html?img_url=/{new_file_path}&video_url={video_url}"
    print(msg, "**"*20, "\n", redirect_url)
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/upload_video/")
async def create_upload_files(video: UploadFile, img_url: str, video_url: str) -> RedirectResponse:
    start = time.time()
    _, file_ext = os.path.split(video.filename)   # 获取上传文件的扩展名 .jpg
    new_file_path = f"{USER_UPLOAD_DIR}/{uuid.uuid1()}{file_ext}" # 使用uuid作为文件名，避免冲突
    try:
        content = await video.read()
        with open(new_file_path, "wb") as f:
            f.write(content)
        msg = {"✅": new_file_path, '耗时(秒)': time.time() - start}
    except Exception as e:
        msg = {"❌": str(e), '耗时(秒)': time.time() - start, '文件': new_file_path}
    redirect_url = f"/static/home.html?img_url={img_url}&video_url=/{new_file_path}"
    print(msg, "**"*20, "\n", redirect_url)
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/swapface/")
async def video_swapface(img_url: str, video_url: str) -> RedirectResponse:
    redirect_url = f"/static/home.html?img_url={img_url}&video_url={video_url}&face_swaped_video=/{INIT_FACE_SWAPED_VIDEO}"
    print( "**"*20, "\n", redirect_url)

    return RedirectResponse(url=redirect_url)


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="172.16.14.2", port=8000, reload=True)
