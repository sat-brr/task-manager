FROM python:3.8

WORKDIR /app/
ENV PYTHONUNBUFFERED=1 
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
