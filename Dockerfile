# Firstly, python image (base layer)
FROM python:3.11-slim

# Put the working directory inside the container
WORKDIR /app

# Install sqlite3 CLI
RUN apt-get update && apt-get install -y sqlite3

# Requirements for server 
COPY requirements.txt .

# Installation of python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the project files to this container
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]