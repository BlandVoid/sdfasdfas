FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED true
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r ./requirements.txt
COPY ./ ./
EXPOSE 8000
