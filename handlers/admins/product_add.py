from loader import bot, db, dp
from aiogram.filters import Command
from aiogram import types, F
from states.my_states import ProductAdd
from aiogram.fsm.context import FSMContext
import random
import os

MEDIA_FOLDER = "media"  # Media folder path

# Ensure the media directory exists
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)


@dp.message(Command('product_add'))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(text="Product nomoni kiriting:")
    await state.set_state(ProductAdd.name)


@dp.message(F.text, ProductAdd.name)
async def get_description(message: types.Message, state: FSMContext):
    await message.answer(text="Product description kiriting:")
    await state.update_data({'name': message.text})
    await state.set_state(ProductAdd.description)


@dp.message(F.text, ProductAdd.description)
async def get_price(message: types.Message, state: FSMContext):
    await message.answer(text='Product price kiriting:')
    await state.update_data({'description': message.text})
    await state.set_state(ProductAdd.price)


@dp.message(F.text, ProductAdd.price)
async def get_qty(message: types.Message, state: FSMContext):
    await message.answer(text='Product qty kiriting:')
    await state.update_data({'price': message.text})
    await state.set_state(ProductAdd.qty)


@dp.message(F.text, ProductAdd.qty)
async def get_gender(message: types.Message, state: FSMContext):
    await message.answer(text='Product category idsini kiriting:')
    await state.update_data({'qty': message.text})
    await state.set_state(ProductAdd.gender)


@dp.message(F.text, ProductAdd.gender)
async def get_discount(message: types.Message, state: FSMContext):
    await state.update_data({"category": message.text})
    await message.answer(text="Product discountini kirting:")
    await state.set_state(ProductAdd.discount)


@dp.message(F.text, ProductAdd.discount)
async def get_image(message: types.Message, state: FSMContext):
    await state.update_data({"discount": message.text})
    await message.answer(text="Iltimos, product rasmni yuboring:")
    await state.set_state(ProductAdd.image)


@dp.message(F.photo, ProductAdd.image)  # Handle image input
async def final(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # Get the file ID and download the photo
    photo_file_id = message.photo[-1].file_id
    photo_file = await bot.get_file(photo_file_id)

    # Download the image
    photo_bytes = await bot.download_file(photo_file.file_path)

    # Define the file path and save the image
    file_extension = ".jpg"  # or ".png" based on your needs
    file_name = f"{random.randint(1, 100000)}{file_extension}"
    file_path = os.path.join(MEDIA_FOLDER, file_name)

    # Save the image to the media folder
    with open(file_path, 'wb') as f:
        f.write(photo_bytes.getvalue())

    # Create the URL for the database
    image_url = f"{file_path.replace('\\', '/')}"  # Convert backslashes to forward slashes for URL format

    # Add product to the database with the image URL
    try:
        db.add_product(
            id=random.randint(1, 100000),
            name=data['name'],
            description=data['description'],
            price=data['price'],
            qty=data['qty'],
            category=data['category'],
            discount=data['discount'],
            image=image_url
        )
        await message.answer(text="Product added successfully!")
    except Exception as e:
        await message.answer(text=f"Failed to add product: {e}")

    await message.answer(text="Product added successfully!")
    await state.clear()

