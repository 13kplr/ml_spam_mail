FROM python:3.11-slim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY /app/finalized_model.sav /app/finalized_model.sav
COPY /app/app.py /app/app.py
COPY /app/transform.py /app/transform.py
COPY /app/vectorizer2.sav /app/vectorizer2.sav
COPY /nltk_data /usr/local/nltk_data

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]