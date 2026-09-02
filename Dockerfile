FROM python:3.12-slim

# ... después de FROM python:3.11-slim ...
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Prevent Python from writing .pyc files and enable unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container.
WORKDIR /app

# Install dependencies first so Docker can cache them better.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.

COPY . .

# Create the directory used by SQLite.
RUN mkdir -p /app/data

# Expose the port used by FastAPI.
EXPOSE 8000

# Start the app with Uvicorn.
CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]