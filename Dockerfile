FROM python:3.10

WORKDIR /bot_f

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /bot_f/docker/app.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]