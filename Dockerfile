FROM python:3.11-slim

#navigate to the app directory
WORKDIR /app 

# Install system dependencies
#yes automatically install gcc
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*  #**remove the apt lists***

# Copy requirements first for better caching (dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project first dot=origin(computer),second dot=destination(docker)
COPY . .

# Expose port not open port only listen to the port
EXPOSE 8000

# Run the application (start script)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]