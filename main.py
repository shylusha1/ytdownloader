import asyncio
from aiogram import *
from aiogram.filters.command import Command
import os
import yt_dlp

bot = Bot(token="tok")

dp = Dispatcher()


@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply("Отправьте ссылку на ваше видео")


@dp.message()
async def echo(message: types.Message):
    try:
        with yt_dlp.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'format': 'best'}) as ydl:
            infoid = ydl.extract_info(message.text, download=True)['id']
            infoex = ydl.extract_info(message.text, download=False)['ext']
            print(infoex)
        msg = await message.reply_document(
            document=types.FSInputFile(
                path=f'{infoid}.{infoex}',
            ),
        )
        await bot.send_message(message.chat.id, "Ваше видео", reply_to_message_id=msg.message_id)
        os.remove(f'{infoid}.{infoex}')
    except:
        await bot.send_message(message.chat.id, "error")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
