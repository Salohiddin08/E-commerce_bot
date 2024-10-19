from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class CheckCategoryGender(CallbackData, prefix='ikb16'):
    check: bool


def categories_gender_button():
    btn = InlineKeyboardBuilder()
    btn.button(text='🧑🏻Erkak', callback_data=CheckCategoryGender(check=True))
    btn.button(text='👩🏻 Ayol', callback_data=CheckCategoryGender(check=False))
    btn.adjust(2)
    return btn.as_markup()

from aiogram.utils.keyboard import ReplyKeyboardBuilder




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






