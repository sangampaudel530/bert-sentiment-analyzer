FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libx11-xcb1 \
    fonts-liberation \
    xdg-utils \
    libpci3 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome (latest stable version)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Install matching ChromeDriver (v136)
RUN DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])") && \
    wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64*

# Set environment variables for Chrome and Chromedriver
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMIUM_PATH=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/bin/chromedriver

# Set workdir and copy app files
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose Streamlit port
EXPOSE 8501

# Start the app with Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
