FROM python:3.11.6

RUN mkdir /linwex_vseobot

WORKDIR /linwex_vseobot

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .   

RUN chmod a+x /linwex_vseobot/docker/*.sh

RUN alembic upgrade head

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]




