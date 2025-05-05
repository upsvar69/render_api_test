#!/usr/bin/env bash
#"""
#We couldnt hook up chrome to the render.com
#we solved this problem through cordel22 but was useless
#cause google wont let u scrape with selenium anyway
#next step is modigy the working beautiful soup scraper on google
#to duckduck go and see if we can get the data
#"""

set -o errexit

echo "📦 Installing Chrome and Chromedriver..."

mkdir -p .render/chrome

# Download prebuilt Chromium + Chromedriver bundle
curl -SL https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.114/linux64/chrome-linux64.zip -o .render/chrome/chrome-linux64.zip
curl -SL https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.114/linux64/chromedriver-linux64.zip -o .render/chrome/chromedriver-linux64.zip

# Unzip the downloaded files
unzip .render/chrome/chrome-linux64.zip -d .render/chrome/
unzip .render/chrome/chromedriver-linux64.zip -d .render/chrome/

# Make Chrome binary executable
chmod +x .render/chrome/chrome-linux64/chrome

# Print structure for verification
echo "📂 Installed files:"
ls -lR .render/chrome

echo "📦 Installing Python requirements..."
pip install -r requirements.txt