FROM python:3.8.5

COPY requirements.txt ./

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

ENV PYTHONPATH /app

COPY . .

CMD python run.py