# bot.py
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from scraper import scrape_links, run_data_mining

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "<BOT_TOKENINIZ>")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /start komutu """
    await update.message.reply_text(
        "Merhaba, ben sizin web scraping botunuzum!\n"
        "/scrape <LINK> <ADET> komutuyla linkleri çekebilirim.\n"
        "Örnek: /scrape https://example.com?page=1 10"
    )

async def scrape_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /scrape <url> <adet>
    Ör: /scrape https://example.com?page=1 10
    """
    try:
        args = update.message.text.split()
        if len(args) < 3:
            await update.message.reply_text(
                "Lütfen link ve çekilecek link sayısını giriniz. Örnek: /scrape <URL> <ADET>"
            )
            return

        link = args[1]
        link_count = int(args[2])

        # 1) Linkleri CSV'ye çek
        await update.message.reply_text(
            f"Linkler çekiliyor... Link: {link}, Adet: {link_count}"
        )
        scrape_links(link, link_count, output_csv="links.csv")

        # 2) Veri kazma
        await update.message.reply_text("Veri kazma işlemi başlıyor...")
        basarili_islem = run_data_mining(links_csv="links.csv", excel_file="list.xlsx")
        await update.message.reply_text(
            f"Veri kazma tamamlandı! Başarılı işlem sayısı: {basarili_islem}"
        )

        # 3) Ortaya çıkan dosyaları Telegram'dan gönder
        if os.path.exists("links.csv"):
            await update.message.reply_document(document=open("links.csv", "rb"))
        if os.path.exists("list.xlsx"):
            await update.message.reply_document(document=open("list.xlsx", "rb"))

        await update.message.reply_text("İşlem bitti, dosyalar gönderildi.")
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

def main():
    if BOT_TOKEN.startswith("<"):
        raise ValueError("Lütfen geçerli bir BOT_TOKEN ortam değişkeni ayarlayınız.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("scrape", scrape_command))

    print("Bot çalışmaya başladı...")
    app.run_polling()

if __name__ == "__main__":
    main()