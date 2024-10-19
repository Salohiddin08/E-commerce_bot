from aiogram import types
from aiogram.fsm.context import FSMContext
from states.my_states import OrderState
from loader import dp, db  # Importing db from loader
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.types import InputFile, FSInputFile



# Product ID input state
@dp.message(F.text, OrderState.waiting_for_product)
async def set_product(message: types.Message, state: FSMContext):
    product_id = message.text
    product = db.get_product_details(product_id=product_id)  # Fetch product details from the database

    if product:
        await state.update_data({
            'product_id': product_id,
            'product_name': product[1],  # Product name
            'price': product[3]  # Product price
        })
        await message.answer(f"{product[1]} tanlandi. Mahsulot miqdorini kiriting:")
        await state.set_state(OrderState.waiting_for_quantity)
    else:
        await message.answer("Mahsulot topilmadi, iltimos to'g'ri ID kiriting.")


# Setting quantity
@dp.message(F.text, OrderState.waiting_for_quantity)
async def set_quantity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        quantity = int(message.text)
        data = await state.get_data()
        product_name = data['product_name']
        price = data['price']

        await state.update_data({'quantity': quantity})
        total_price = price * quantity  # Calculate total price

        await display_order_summary(message, product_name, quantity, total_price)  # Send summary with buttons
        await state.set_state(OrderState.waiting_for_confirmation)
    else:
        await message.answer("Iltimos, miqdorni to'g'ri kiriting.")


# Function to display order summary
async def display_order_summary(message: types.Message, product_name: str, quantity: int, total_price: int):
    # Create +/- buttons and confirm order button
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="➕", callback_data="increase_quantity")
    keyboard.button(text="➖", callback_data="decrease_quantity")
    keyboard.button(text="Buyurtma berish", callback_data="confirm_order")
    keyboard.adjust(2, 1)

    await message.answer(f"{product_name} uchun miqdor: {quantity} ta\nUmumiy summa: {total_price} so'm",
                         reply_markup=keyboard.as_markup())


# Quantity modification and order confirmation
@dp.callback_query(F.data.in_({"increase_quantity", "decrease_quantity", "confirm_order"}))
async def confirm_or_update_quantity(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quantity = data['quantity']
    price = data['price']

    # Modify quantity based on the button pressed
    if call.data == "increase_quantity":
        quantity += 1
    elif call.data == "decrease_quantity" and quantity > 1:
        quantity -= 1
    elif call.data == "confirm_order":
        product_id = data['product_id']
        total_price = price * quantity  # Calculate total price
        user_id = call.from_user.id
        db.save_order(user_id=user_id, product_id=product_id, quantity=quantity,
                      total_price=total_price)  # Save the order

        await call.message.answer(
            f"Buyurtma tasdiqlandi:\n"
            f"Mahsulot: {data['product_name']}\n"
            f"Miqdor: {quantity} ta\n"
            f"Umumiy summa: {total_price} so'm"
        )

        # Create a new inline keyboard for placing another order
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Yana buyurtma berish", callback_data="new_order")  # Button for a new order
        keyboard.adjust(1)

        # Prompt the user to place a new order
        await call.message.answer("Yana buyurtma berish uchun tugmani bosing:", reply_markup=keyboard.as_markup())

        await state.clear()  # Clear the state
        await call.answer()
        return

    # Update and display the new quantity
    await state.update_data({'quantity': quantity})
    total_price = price * quantity  # Recalculate total price
    await call.message.edit_text(
        f"Yangi miqdor: {quantity} ta\nUmumiy summa: {total_price} so'm\nBuyurtma berish uchun 'Buyurtma berish' tugmasini bosing.")

    # Re-display buttons
    await display_order_summary(call.message, data['product_name'], quantity, total_price)
    await call.answer()


# Handle the new order request
@dp.callback_query(F.data == "new_order")
async def handle_new_order(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Iltimos, mahsulot ID sini kiriting:")  # Prompt the user to enter the product ID
    await state.set_state(OrderState.waiting_for_product)  # Set state to waiting for product
    await call.answer()


from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import dp, db
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import dp, db
import os
from aiogram import types
from aiogram.types import InputFile



@dp.message(F.text == "Buyurtmalarim 🚚")
async def show_orders(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    orders = db.get_user_orders(user_id)  # Get user's orders

    if orders:
        for order in orders:
            # Handle cases where image might be missing
            if len(order) == 3:
                product_id, quantity, total_price = order
                image = None  # Default value if image is missing
            else:
                product_id, quantity, total_price, image = order

            # Prepare the photo path and retrieve product details
            product = db.select_product(id=product_id)
            image_path = product[-1] if len(product) > 1 else None

            # Check if the file exists before sending
            if image_path and os.path.exists(image_path):
                # Use FSInputFile to send the photo
                await message.answer_photo(
                    photo=types.input_file.FSInputFile(path=image_path),
                    caption=f"📦 Mahsulot ID: {product_id}\nMiqdor: {quantity} ta\nUmumiy summa: {total_price} so'm"
                )
            else:
                await message.answer(f"❌ Mahsulot ID: {product_id} uchun rasm topilmadi.")
    else:
        await message.answer("❌ Sizda hech qanday buyurtma mavjud emas.")






