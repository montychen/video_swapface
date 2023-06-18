```bash
pip install fastapi uvicorn

pip install python-multipart

```
开发运行
```bash
uvicorn main:app  --reload
```

# uvicorn后台运行 nohup
nohup是一种Unix命令，用于在后台运行进程，并将其输出重定向到指定的文件中，从而使进程在用户退出终端后仍能继续运行。
当我们使用nohup命令来运行uvicorn时，我们可以将uvicorn进程转换为守护进程并将输出写入到指定的文件中。

```bash
nohup uvicorn myapp:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
```


