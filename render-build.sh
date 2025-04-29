#!/usr/bin/env bash
set -o errexit

echo "📦 Installing Chrome and Chromedriver..."

mkdir -p .render/chrome

# Download prebuilt Chromium + Chromedriver bundle
curl -SL https://github.com/BugzTheBunny/chrome-on-render/releases/latest/download/chrome-on-render.tar.gz | tar -xzC .render/chrome

# Make Chrome binary executable
chmod +x .render/chrome/opt/google/chrome/google-chrome

# Print structure for verification
echo "📂 Installed files:"
ls -lR .render/chrome

echo "📦 Installing Python requirements..."
pip install -r requirements.txt