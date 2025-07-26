FROM python:3.11-alpine

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./sample-data ./sample-data

COPY ./app ./app

WORKDIR /app

RUN cd database && python init_db.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]