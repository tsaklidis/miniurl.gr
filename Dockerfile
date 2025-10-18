# 1. Start from an official Python image
FROM python:3.12-slim

# 2. Set environment variables for Python (e.g. disables .pyc files and enables unbuffered output)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory inside the container
WORKDIR /app

# 4. Install system dependencies (build essentials, pip, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 5. Copy Python dependency files first (enables Docker cache for dependencies)
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the application code
COPY . .

# 8. Expose the port your app runs on (FastAPI default is 8000)
EXPOSE 8000

# 9. Command to run app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]