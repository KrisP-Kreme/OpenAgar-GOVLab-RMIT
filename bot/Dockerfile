FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install flask

COPY . .

EXPOSE 8080

CMD ["python", "bot_api.py"]
