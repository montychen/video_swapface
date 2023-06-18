```bash
pip install fastapi uvicorn

pip install python-multipart

```
开发运行
```bash
uvicorn main:app  --reload
```

# uvicorn后台运行，需要依靠uvicorn
```bash
pip install gunicorn

gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &
```

gunicorn main:app --worker-connections=1000 --workers=2  -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
