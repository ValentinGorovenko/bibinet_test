FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY bibinet_app/ .

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8008", "main:bibinet_app", "-k", "uvicorn.workers.UvicornWorker"]