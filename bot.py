import asyncio
import time
import telebot
import speedtest
from threading import Thread

TOKEN = 'token_bot_telegram'
bot = telebot.TeleBot(TOKEN)
speedtester = speedtest.Speedtest()

# Define owner bot ID
OWNER_ID = "your_owner_id_here"

# Define decorator to restrict access to owner only commands
def owner_only(func):
    async def wrapper(message):
        if str(message.from_user.id) == OWNER_ID:
            await func(message)
        else:
            await bot.reply_to(message, "Maaf, perintah ini hanya dapat diakses oleh pemilik bot.")
    return wrapper

@bot.message_handler(commands=['ping'])
async def ping_command(message):
    start_time = time.time()
    await bot.send_chat_action(message.chat.id, 'typing')
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 2)
    response = f'Pong! {ping_time} ms'
    await bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
async def help_command(message):
    response = 'Berikut adalah daftar perintah yang tersedia:\n'
    response += '/ping - untuk mengetahui kecepatan respon bot dalam ms\n'
    response += '/speed - untuk mengetahui kecepatan server\n'
    response += '/help - untuk menampilkan daftar perintah\n'
    if str(message.from_user.id) == OWNER_ID:
        response += '/secret - perintah rahasia hanya untuk pemilik bot\n'
    await bot.reply_to(message, response)

@bot.message_handler(commands=['speed'])
async def speed_command(message):
    download_speed = round(speedtester.download() / 10**6, 2)
    upload_speed = round(speedtester.upload() / 10**6, 2)
    response = f'Kecepatan unduh: {download_speed} Mbps\n'
    response += f'Kecepatan unggah: {upload_speed} Mbps'
    await bot.reply_to(message, response)

@bot.message_handler(commands=['secret'])
@owner_only
async def secret_command(message):
    await bot.reply_to(message, "Hanya pemilik bot yang dapat mengakses perintah ini.")

async def polling():
    await bot.polling()

def start_polling():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(polling())

if __name__ == '__main__':
    thread = Thread(target=start_polling)
    thread.start()
