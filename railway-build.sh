#!/bin/bash
# Make Chrome executable available
apt-get update
apt-get install -y chromium chromium-chromedriver
ln -s /usr/lib/chromium/chromedriver /usr/bin/chromedriver
ln -s /usr/bin/chromium /usr/bin/google-chrome
chmod +x /usr/bin/chromedriver
# Install other dependencies