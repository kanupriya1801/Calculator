FROM python:3.9-slim

WORKDIR /app

COPY calculator.py .

RUN pip install --no-cache-dir tk
CMD ["python", "calculator.py"]
