# bot.py
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# scraper.py içindeki fonksiyonları içe aktar
from scraper import scrape_links, run_data_mining

# Loglama ayarı
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ortam değişkeninden TOKEN'i alalım (Railway'de ayarlayacaksınız)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7380181516:AAGAzBZInwCKYSdhwqNnIGl-0Q7IXBkyk9c")  
# BOT_TOKEN'ı bir .env dosyasında saklayıp python-dotenv ile de okuyabilirsiniz.

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start komutunu yakalar.
    """
    await update.message.reply_text(
        "Merhaba, ben sizin web scraping botunuzum!\n"
        "/scrape <LINK> <ADET> komutuyla linkleri çekebilirim.\n"
        "Örnek: /scrape https://example.com?page=1 10"
    )

async def scrape_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /scrape <link> <link_sayisi>
    Kullanıcıdan link ve çekilecek link sayısını alarak scraping başlatır.
    """
    try:
        # Komutun içeriğini parçalayalım
        # Örnek: "/scrape https://example.com?page=1 10"
        message_parts = update.message.text.split()
        if len(message_parts) < 3:
            await update.message.reply_text("Lütfen link ve çekilecek link sayısını giriniz. Ör: /scrape <url> <adet>")
            return

        link = message_parts[1]
        link_count = int(message_parts[2])

        # 1) Links.csv oluşturma (scrape_links fonksiyonu)
        await update.message.reply_text(f"Linkler çekiliyor... Link: {link}, Adet: {link_count}")
        scrape_links(link, link_count, output_csv="links.csv")

        await update.message.reply_text("Linkler çekildi! Şimdi veri kazma işlemi başlıyor...")
        # 2) Veri kazma (run_data_mining)
        basarili_islem = run_data_mining(links_csv="links.csv", excel_file="list.xlsx")
        await update.message.reply_text(f"Veri kazma tamamlandı! Toplam Başarılı İşlem: {basarili_islem}")

        # 3) Ortaya çıkan dosyaları kullanıcıya gönderme
        if os.path.exists("links.csv"):
            await update.message.reply_document(document=open("links.csv", "rb"))
        if os.path.exists("list.xlsx"):
            await update.message.reply_document(document=open("list.xlsx", "rb"))

        await update.message.reply_text("İşlem tamam! Dosyalar gönderildi.")

    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

def main():
    """
    Botu başlatan ana fonksiyon.
    """
    if BOT_TOKEN is None or BOT_TOKEN.startswith("<"):
        raise ValueError("Lütfen geçerli bir BOT_TOKEN ortam değişkeni ayarlayın.")

    # Uygulama oluştur
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Komutları ekle
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("scrape", scrape_command))

    # Botu çalıştır
    print("Bot çalışıyor...")
    application.run_polling()

if __name__ == "__main__":
    main()