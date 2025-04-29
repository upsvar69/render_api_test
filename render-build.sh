#!/usr/bin/env bash
set -o errexit

echo "📦 Installing Chrome..."

mkdir -p .render/chrome
cd .render/chrome

# Download and unzip Chrome
curl -SL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
ar x chrome.deb
tar -xf data.tar.xz

# Move Chrome to Render-compatible path
mkdir -p opt/google/chrome
mv opt/google/chrome/* ./opt/google/chrome/
chmod +x ./opt/google/chrome/google-chrome

# Move chromedriver (Render automatically provides the matching one)
mkdir -p usr/bin
cp /usr/bin/chromedriver usr/bin/ || echo "⚠️ No chromedriver found globally — skipping copy."

cd ../../