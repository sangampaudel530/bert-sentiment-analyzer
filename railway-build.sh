#!/bin/bash

# Chromium installation paths for Railway
echo "Installing Chrome & Chromedriver"
apt-get update
apt-get install -y chromium-browser chromium-chromedriver
which chromium-browser
which chromedriver

# Set environment variables
export GOOGLE_CHROME_BIN=/usr/bin/chromium-browser
export CHROMEDRIVER_PATH=/usr/bin/chromedriver
