from aiogram.utils.keyboard import ReplyKeyboardBuilder
from loader import dp, db
from aiogram import types, F




def start_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="Categories 🎛")
    btn.button(text="Buyurtmalarim 🚚")
    btn.button(text="Chegirmalar 💯")
    btn.button(text="Savat 🛒")
    btn.button(text="Yoqtirganlarim ❤️")
    btn.button(text="Aloqa ☎️")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)


def gender_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text="Erkaklar uchun 🧑")
    btn.button(text="Ayollar uchun 👩")
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)



@dp.message(F.text == "Aloqa ☎️")
async def send_contact_info(message: types.Message):
    phone_number = "+998337974707"
    phone_username = ("\n"
                      ""
                      "@salohiddin_urinboev\n"
                      "@codersdepartament")
    await message.answer(f"📞 Aloqa uchun telefon raqam: {phone_number}\n"
                         f"📞 Aloqa uchun telegram user: {phone_username}")
