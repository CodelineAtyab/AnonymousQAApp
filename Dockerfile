FROM python:3.11-alpine

WORKDIR /app

COPY ./ /app

RUN pip install fastapi[all]

EXPOSE 8080

CMD ["python", "main.py"]
