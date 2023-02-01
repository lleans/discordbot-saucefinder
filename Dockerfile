FROM python:3.8-slim

COPY . /app
WORKDIR /app
RUN apt update && apt -y install ffmpeg && apt -y install git && pip3 install -Ur requirements.txt

CMD ["python3", "bot.py"]