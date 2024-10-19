from loader import bot, db, dp
from aiogram import types, F
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

@dp.message(F.text == "Savat 🛒")
async def show_basket(message: types.Message):
    user_id = message.from_user.id  # Foydalanuvchining ID sini olish
    basket_items = db.get_basket_items(user_id)  # Savatcha elementlarini olish
    print(basket_items, 'Savatchadagi mahsulotlar', user_id)  # Terminalda chop etish

    if basket_items:
        for item in basket_items:
            product_id = item[1]  # 2-ustun - product_id
            quantity = item[3]    # 4-ustun - quantity
            total_price = item[4]  # 5-ustun - total_price

            # Mahsulot tafsilotlarini olish
            product_details = db.get_product_details(product_id)
            if product_details:
                product_name = product_details[1]  # Mahsulot nomi
                price = product_details[3]  # Mahsulot narxi
                image_path = product_details[6]  # Mahsulot rasmi

                # Mahsulot haqida matn tayyorlash
                message_text = (
                    f"📦 Mahsulot: {product_name}\n"
                    f"Narxi: {price}000 so'm\n"
                    f"Miqdor: {quantity} ta\n"
                    f"Umumiy narx: {total_price} so'm\n\n"
                )

                # Tugmalarni yaratish
                button_builder = InlineKeyboardBuilder()
                button_builder.button(text="Buyurtma berish", callback_data=f"order_{product_id}_{total_price}_{quantity}")
                button_builder.button(text="Savatdan o'chirish", callback_data=f"remove_{product_id}")

                # Mahsulot rasmi va tugmalar bilan javob jo'natish
                await message.answer_photo(
                    caption=message_text,
                    reply_markup=button_builder.as_markup(),
                    photo=types.input_file.FSInputFile(path=image_path)
                )
            else:
                await message.answer(f"Mahsulot ID {product_id} uchun tafsilotlar topilmadi.")
    else:
        await message.answer("❌ Savatda hech qanday mahsulot yo'q.")  # Savatcha bo'sh bo'lsa
