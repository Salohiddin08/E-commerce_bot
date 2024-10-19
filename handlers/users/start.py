from aiogram.filters import CommandStart
from loader import dp, db, bot
from aiogram import types, html, F
import random
from keyboards.default.buttons import start_button, gender_button
@dp.message(CommandStart())
async def start_bot(message:types.Message):
    if not db.select_user(telegram_id=message.from_user.id):
        user = message.from_user
        db.add_user(id=random.randint(1,100000), fullname=user.full_name, telegram_id=user.id, language=user.language_code)
    else:
        pass
    await bot.send_message(chat_id=message.from_user.id,
                           text="Assalamu Aleykum  " + html.link(value="" + message.from_user.full_name + '',
                                                                 link=f'tg://user?id={message.from_user.id}'),
                           disable_web_page_preview=True, reply_markup=start_button())


@dp.message(F.text == 'Categories 🎛')
async def get_gender(message: types.Message):
    await message.answer(text="Tanlang", reply_markup=gender_button())
