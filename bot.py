import os
import tempfile
import telebot
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m, "Salom! Instagram havolasini yuboring 📥")

@bot.message_handler(func=lambda m: True)
def download(m):
    url = (m.text or "").strip()

    if "instagram.com/" not in url:
        return bot.reply_to(m, "Instagram havolasini yuboring!")

    msg = bot.reply_to(m, "⏳ Yuklanmoqda...")

    try:
        with tempfile.TemporaryDirectory() as folder:
            opts = {
                "outtmpl": folder + "/video.%(ext)s",
                "format": "best[ext=mp4]/best",
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = ydl.prepare_filename(info)

            with open(path, "rb") as f:
                bot.send_video(m.chat.id, f)

    except Exception as e:
        bot.reply_to(m, "❌ Yuklab bo'lmadi!")
        print(e)

    finally:
        try:
            bot.delete_message(m.chat.id, msg.message_id)
        except Exception:
            pass

bot.infinity_polling()