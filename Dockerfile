# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Sistem paketlerini yükle (Chrome, Chromedriver vs.)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libx11-dev \
    libxss1 \
    libxext6 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release

# Google Chrome yükle
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

# ChromeDriver yükle (latest)
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]