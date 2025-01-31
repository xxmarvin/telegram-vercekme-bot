FROM python:3.10-slim

WORKDIR /app

# Sistem paketleri (Chrome + Chromedriver kurulumu için)
# Bu kısım Selenium + Chrome için özelleştirilebilir
RUN apt-get update && apt-get install -y wget gnupg unzip
RUN pip install --upgrade pip setuptools wheel

# Google Chrome yüklenmesi
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Chromedriver yüklenmesi
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]


