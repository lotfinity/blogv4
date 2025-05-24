# Use official Python 3.11 base image
FROM python:3.13.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libdbus-1-3 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv or pip-tools for managing dependencies (PEP compliant)
RUN pip install --upgrade pip setuptools wheel

# Copy project files
COPY . /app
i 
# Install Python dependencies
RUN pip install -r requirements.txt

# Default command (can be overridden)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]