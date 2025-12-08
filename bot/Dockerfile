FROM python:3-alpine

ENV SERVER_URL=http://keen-radiance.railway.internal:8080

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install flask

COPY . .

EXPOSE 5000

CMD [ "python", "./bot_api.py" ]
