# Use a Python image that includes Chrome
FROM python:3.9-slim
# ... (rest of the Dockerfile remains the same as before)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]
# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy your files
COPY . .



# Install Python requirements
RUN pip install --no-cache-dir selenium webdriver-manager

# Start the script
CMD ["python", "main.py"]
