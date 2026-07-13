FROM python:3.12-slim
WORKDIR /app
COPY ./* /app/
RUN pip3 install -r requirements.txt

