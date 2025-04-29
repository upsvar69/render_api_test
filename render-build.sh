#!/usr/bin/env bash
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