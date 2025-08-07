import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

# توکن و آیدی ادمین از محیط بیرونی (مثل Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)

# ایجاد بات و دیسپچر
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("سلام! پیامت چیه؟")


@dp.message(Command("reply"))
async def reply_to_user(message: Message):
    args = message.text.split(" ", 2)  # /reply user_id text
    if len(args) < 3:
        await message.reply("فرمت درست: /reply user_id پیام شما")
        return
    try:
        user_id = int(args[1])
        reply_text = args[2]
        await bot.send_message(chat_id=user_id, text=f"📩 جواب ادمین:\n{reply_text}")
        await message.reply("✅ پیغام ارسال شد مهندس")
    except ValueError:
        await message.reply("❌ آیدی کاربر باید عدد باشد.")
    except Exception as e:
        await message.reply(f"❌ مهندس خطا در ارسال پیام داریم! {e}")


@dp.message(F.text)
async def forward_message(message: Message):
    if message.from_user.id == ADMIN_ID:
        return  # اگر پیام از خود ادمین باشد، ارسال نشود

    user = message.from_user
    msg = (
        f"📩 پیام ناشناس:\n"
        f"🧑‍💬 نام: {user.first_name}\n"
        f"🔗 یوزرنیم: @{user.username or 'ندارد'}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"📝 پیام: {message.text}\n\n"
        f"برای پاسخ:\n/reply {user.id} پیام شما"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=msg)


async def main():
    # شروع به دریافت پیام‌ها
    await dp.start_polling(bot, skip_updates=True)
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
#code by jobay v2.1
