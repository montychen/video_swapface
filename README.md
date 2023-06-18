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

# 监听 8000端口
gunicorn fastapi_db.main:app -c ./gunicorn.py  
```
gunicorn的配置文件**gunicorn.py**内容
```python
daemon=True #是守护进程

bind='0.0.0.0:8000'#绑定

pidfile='gunicorn.pid'#pid文件地址
chdir='.' # 项目地址
worker_class='uvicorn.workers.UvicornWorker'
workers=1   # 推荐 CPU数 * 2  + 1
threads=2
loglevel='debug' # 日志级别
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "gunicorn_access.log"
errorlog = "gunicorn_error.log"
```
