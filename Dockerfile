FROM python:3.7

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN mkdir bot
WORKDIR /bot
COPY ./bot /bot

CMD ["python3", "bot.py"]
