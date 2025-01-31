# Dockerfile
FROM python:3.10-slim

# Logların anında görünmesi için
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Gerekli sistem paketlerini yükle ve apt cache'ini temizle
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
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome'u indir ve kur
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y /tmp/chrome.deb && \
    rm /tmp/chrome.deb

# ChromeDriver'ı dinamik olarak indir:
# 1. Yüklü Chrome sürümünün ana versiyonunu al (örneğin: 132)
# 2. Bu versiyona uygun ChromeDriver sürümünü çekmeye çalış.
# 3. Eğer çekilemezse fallback olarak "132.0.7240.71" sürümü kullan.
RUN CHROME_VERSION=$(google-chrome --version | sed -E 's/[^0-9]*([0-9]+).*/\1/') && \
    echo "Chrome version: $CHROME_VERSION" && \
    CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION || true) && \
    if [ -z "$CHROMEDRIVER_VERSION" ]; then \
         echo "ChromeDriver version for Chrome $CHROME_VERSION not found, using default version 132.0.7240.71"; \
         CHROMEDRIVER_VERSION="132.0.7240.71"; \
    fi && \
    echo "ChromeDriver version: $CHROMEDRIVER_VERSION" && \
    wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Python paketlerini yükle
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Railway ortamında eğer HTTP port kullanıyorsanız (örn: web endpoint) bu satırları aktifleştirin
# ENV PORT=8000
# EXPOSE 8000

# Telegram botunuz long polling ile çalıştığından, doğrudan bot.py'yi çalıştırıyoruz.
CMD ["python", "bot.py"]