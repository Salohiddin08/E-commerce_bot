from loader import bot, db, dp
from aiogram.utils.keyboard import  InlineKeyboardBuilder
from aiogram import types, F

@dp.message(F.text == 'barcha categorylar')
async def product_all(message: types.Message):
    btn = InlineKeyboardBuilder()
    product = db.select_all_products()
    [btn.button(text=i[1], callback_data=f"male_{i[0]}") for i in product]
    await message.answer(text="barcha productlar", reply_markup=btn.as_markup())

@dp.message(F.text == 'barcha categorylar')
async def product_all(message: types.Message):
    btn = InlineKeyboardBuilder()
    product = db.select_all_products()
    [btn.button(text=i[1], callback_data=f"female_{i[0]}") for i in product]
    await message.answer(text="barcha categorylar", reply_markup=btn.as_markup())


