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
INIT_FACE_SWAPED_VIDEO = f"{USER_UPLOAD_DIR}/init_face_swaped.mov"


@app.get("/")
async def home() -> RedirectResponse:
    redirect_url = f"/static/home.html?img_url=/{INIT_IMG}&video_url=/{INIT_VIDEO}"
    return RedirectResponse(url=redirect_url)


@app.post("/upload_img/")
async def create_upload_files(img: UploadFile, img_url: str, video_url: str):
    start = time.time()
    _, file_ext = os.path.split(img.filename)   # 获取上传文件的扩展名，例如  .jpg
    # 使用uuid作为文件名，避免冲突
    new_file_path = f"{USER_UPLOAD_DIR}/{uuid.uuid1()}{file_ext}"
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
    _, file_ext = os.path.splitext(video.filename)   # 获取上传文件的扩展名 .jpg
    # 使用uuid作为文件名，避免冲突
    new_file_path = f"{USER_UPLOAD_DIR}/{uuid.uuid1()}{file_ext}"
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
    # roop 在执行换脸过程中会生成一个和视频同名的目录，避免有2个用户同时使用同一个视频进行换脸。 调用系统命令cp，拷贝多一份用uuid命名的视频文件，避免冲突
    # /static/user_upload/init_girl.mp4  中的 init_girl.mp4
    video_file_basename = os.path.basename(video_url)
    _, video_ext = os.path.splitext(video_url)   # 获取上传文件的扩展名，例如  .mp4
    tmp_video_file = f"{USER_UPLOAD_DIR}/{uuid.uuid1()}_tmp{video_ext}"
    output_video_file = f"{USER_UPLOAD_DIR}/{uuid.uuid1()}_output{video_ext}"
    os.system(f"cp {USER_UPLOAD_DIR}/{video_file_basename} {tmp_video_file}")

    roop_run_command = f"python ../roop/run.py -f .{img_url} -t ./{tmp_video_file} -o ./{output_video_file} --gpu-vendor nvidia --gpu-threads 2"
    subprocess.call(roop_run_command.split(" "))
    print("**"*20, "\n", roop_run_command)


    redirect_url = f"/static/home.html?img_url={img_url}&video_url={video_url}&face_swaped_video=/{output_video_file}"
    print("**"*20, "\n", redirect_url)

    return RedirectResponse(url=redirect_url)


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="172.16.14.2", port=8000, reload=True)
