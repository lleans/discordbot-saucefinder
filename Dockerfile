FROM python:3.8

COPY . /app
WORKDIR /app
RUN apt-get -y update && apt-get install -y ffmpeg && pip3 install -Ur requirements.txt

CMD ["python3", "bot.py"]