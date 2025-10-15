# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies (if any)
# RUN pip install -r requirements.txt

# Default command to run the calculator
CMD ["python", "calculator.py"]
