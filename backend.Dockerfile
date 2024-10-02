FROM python:3.12-alpine AS base

# Copy the requirements file and install the dependencies
WORKDIR /app

COPY requirements.txt .

RUN set -xe; pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app/ .

EXPOSE 8090

COPY .env .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]

