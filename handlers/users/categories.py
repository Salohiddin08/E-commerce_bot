from handlers.users.start import start_bot
from keyboards.inline.buttons import start_button
from loader import bot, db, dp
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, F
from aiogram.types import InputFile  # Ensure you import InputFile
import os
from aiogram.fsm.context import FSMContext
from states.my_states import OrderState
from handlers.users import orders

@dp.message(F.text == 'Erkaklar uchun 🧑')
async def get_and_create_button_male(message: types.Message):
    btn = InlineKeyboardBuilder()
    category = db.get_category_gender(gender=True)
    [btn.button(text=i[1], callback_data=f"male_{i[0]}") for i in category]
    btn.button(text="Orqaga 🔙", callback_data="back_to_gender")
    await message.answer(text="Barcha kategoriyalar erkaklar uchun", reply_markup=btn.as_markup())

@dp.message(F.text == 'Ayollar uchun 👩')
async def get_and_create_button_female(message: types.Message):
    btn = InlineKeyboardBuilder()
    category = db.get_category_gender(gender=False)
    [btn.button(text=i[1], callback_data=f"female_{i[0]}") for i in category]
    btn.button(text="Orqaga 🔙", callback_data="back_to_gender")
    await message.answer(text="Barcha kategoriyalar ayollar uchun", reply_markup=btn.as_markup())

@dp.callback_query(F.data == 'back_to_gender')
async def back_to_gender(callback: types.CallbackQuery):
    await callback.message.delete()  # Oldingi xabarni o'chirish
    await callback.message.answer("Tanlang:", reply_markup=start_button())






@dp.callback_query(lambda query: query.data.startswith('male_'))
async def get_category(call: types.CallbackQuery):
    category_id = call.data.split('_')[1]
    products = db.get_product_id(category=category_id)

    if products:
        product_buttons = InlineKeyboardBuilder()
        for product in products:
            product_buttons.button(text=f"{product[1]} - {product[3]}000 so'm", callback_data=f"product_{product[0]}")

        await call.message.answer(text="Select a product:", reply_markup=product_buttons.as_markup())
    else:
        await call.message.answer(text="No products found in this category.")
    await call.answer()

@dp.callback_query(lambda query: query.data.startswith('female_'))
async def get_female_category(call: types.CallbackQuery):
    category_id = call.data.split('_')[1]
    products = db.get_product_id(category=category_id)

    if products:
        product_buttons = InlineKeyboardBuilder()
        for product in products:
            product_buttons.button(text=f"{product[1]} - {product[3]}000 so'm", callback_data=f"product_{product[0]}")

        await call.message.answer(text="Select a product:", reply_markup=product_buttons.as_markup())
    else:
        await call.message.answer(text="No products found in this category.")
    await call.answer()


from aiogram import types

@dp.callback_query(lambda query: query.data.startswith('add_to_cart_'))
async def add_to_cart(call: types.CallbackQuery):
    product_id = call.data.split('_')[-1]
    user_id = call.from_user.id
    try:
        existing_items = db.get_basket_items(user_id)
        print(existing_items)  # Check the structure of existing_item

        # Find the item with the matching product_id
        existing_item = next((item for item in existing_items if item[2] == int(product_id)), None)

        if existing_item:
            quantity = existing_item[3]  # Extract the quantity
            new_quantity = quantity + 1  # Update the quantity
            db.update_basket_item(user_id, product_id, new_quantity)
            await call.answer("Mahsulot savatda yangilandi!")
        else:
            quantity = 1
            db.add_to_basket(user_id, product_id, quantity)
            await call.answer("Mahsulot savatga qo'shildi!")
    except Exception as e:
        await call.answer("Savatga qo'shishda xato yuz berdi.")
        print(f"Error: {e}")






# Mahsulot tafsilotlari va tugmalarni ko'rsatish
@dp.callback_query(lambda query: query.data.startswith('product_'))
async def get_product_details(call: types.CallbackQuery):
    product_id = call.data.split('_')[1]
    product = db.get_product_details(product_id=product_id)

    if product:
        product_name = product[1]
        description = product[2]
        price = product[3]
        qty = product[4]
        category_id = product[5]
        image_path = product[6]

        text = (f"Name: {product_name}\n"
                f"Description: {description}\n"
                f"Price: {price} so'm\n"
                f"Quantity: {qty}\n"
                f"Category ID: {category_id}")

        # Tugmalarni yaratamiz
        order_button = InlineKeyboardBuilder()
        order_button.button(text="Buyurtma berish", callback_data=f"order_{product_id}_{price}_{qty}")
        order_button.button(text="Savatga qo'shish", callback_data=f"add_to_cart_{product_id}")

        # Mahsulot ma'lumotlari va rasm bilan tugmalarni yuborish
        await call.message.answer_photo(
            caption=text,
            reply_markup=order_button.as_markup(),
            photo=types.input_file.FSInputFile(path=image_path)
        )


    else:
        await call.message.answer(text="Product not found.")

    await call.answer()


@dp.callback_query(lambda query: query.data.startswith('order_'))
async def start_order(call: types.CallbackQuery, state: FSMContext):
    # Callback data format: order_{product_id}_{price}_{qty}
    data = call.data.split('_')
    product_id = data[1]
    price = data[2]
    qty = data[3]

    # Buyurtma holatini boshlash uchun foydalanuvchidan mahsulot nomini so'raymiz
    await call.message.answer(
        text=f"Buyurtma bermoqchi bo'lgan mahsulot ID: {product_id}, narxi: {price}000 so'm. Mahsulot nomini kiriting:")

    # Davlat mashinasi (FSM) uchun kerakli holatni o'rnatamiz
    await state.set_state(OrderState.waiting_for_product)

    # Foydalanuvchiga javob beramiz
    await call.answer()

# @dp.callback_query(lambda query: query.data.startswith('order_'))
# async def order_product(call: types.CallbackQuery):
#     # Ma'lumotlarni callback_data dan olish
#     _, product_id, price, qty = call.data.split('_')
#
#     # Bu yerda buyurtma berish jarayonini davom ettirish
#     await call.message.answer(text=f"Siz {product_id} mahsulotini buyurtma qildingiz.\n"
#                                    f"Narxi: {price}000 so'm\n"
#                                    f"Miqdori: {qty}.")
#
#     await call.answer()


