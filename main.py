import logging
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# گرفتن توکن و آیدی ادمین از متغیرهای محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# تنظیم سطح لاگ
logging.basicConfig(level=logging.INFO)

# ایجاد نمونه بات و دیسپچر
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    """پیام خوشامدگویی وقتی کاربر /start بزنه"""
    await message.answer("سلام! پیامت چیه؟")


@dp.message(Command("reply"))
async def reply_to_user(message: Message):
    """ادمین با این دستور می‌تونه به کاربر پاسخ بده"""
    args = message.text.split(" ", 2)  # /reply user_id پیام
    if len(args) < 3:
        await message.answer("فرمت درست: /reply user_id پیام شما")
        return
    try:
        user_id = int(args[1])
        reply_text = args[2]
        await bot.send_message(chat_id=user_id, text=f"📩 جواب ادمین:\n{reply_text}")
        await message.answer("✅ پیغام ارسال شد مهندس")
    except ValueError:
        await message.answer("❌ آیدی کاربر باید عدد باشد.")
    except Exception as e:
        await message.answer(f"❌ مهندس خطا در ارسال پیام داریم! {e}")


@dp.message()
async def forward_message(message: Message):
    """همه پیام‌های متنی از کاربران به ادمین فوروارد میشن (ناشناس)"""
    if message.from_user.id == ADMIN_ID:
        return  # اگر پیام از خود ادمین باشه، فوروارد نشه

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
    """شروع polling و دریافت پیام‌ها"""
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

#jobay v2.2
