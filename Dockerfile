# Start from an official Python slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    chromium \
    chromium-driver

# Link chromium browser properly
RUN ln -s /usr/bin/chromium /usr/bin/google-chrome

# Print versions for debugging
RUN echo "✅ Installed Chrome binary at: $(which google-chrome)" && \
    google-chrome --version || true && \
    chromium --version || true

# Set display port to avoid crash
ENV DISPLAY=:99

# Set workdir
WORKDIR /app

# Copy source files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose port
EXPOSE 8000

# Start the server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]