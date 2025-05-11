# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Install dependencies for Chromium and other libraries
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to not generate .pyc files and to buffer output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Set environment variables for Chrome binary location
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_PATH=/usr/bin/chromium

# Expose the port your app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]
