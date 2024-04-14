FROM python:3.9

ARG PORT

EXPOSE $PORT

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG MONGODB_URL
ARG DB_NAME

RUN python3 scripts/init.py

CMD ["python3", "app.py"]
