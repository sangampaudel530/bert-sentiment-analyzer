# Use official Python slim image
FROM python:3.11-slim

# Install base system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libx11-xcb1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libxss1 \
    libappindicator3-1 \
    xdg-utils \
    ca-certificates \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Chromium (version 136)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver version 136 (to match Chromium 136)
RUN CHROMEDRIVER_VERSION=`curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])"` && \
    echo "Using ChromeDriver version: $CHROMEDRIVER_VERSION" && \
    wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# Set environment variables
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
