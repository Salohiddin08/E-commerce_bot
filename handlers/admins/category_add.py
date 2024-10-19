from loader import dp, db
from states.my_states import CategoryAdd
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import random
from keyboards.inline.buttons import CheckCategoryGender, categories_gender_button

@dp.message(Command('category_add'))
async def category_add(message: types.Message, state: FSMContext):
    await message.answer(text="Category tanlang:",reply_markup=categories_gender_button())
    await state.set_state(CategoryAdd.gender)

@dp.callback_query(CheckCategoryGender.filter(), CategoryAdd.gender)
async def get_gender(call: types.CallbackQuery, callback_data: CheckCategoryGender, state: FSMContext):
    check = callback_data.check
    await call.answer(cache_time=60)
    if check:
        await call.message.answer(text="Category Nomini kiritin")
        await state.update_data({
            'gender':True
        })
        await state.set_state(CategoryAdd.name)
    else:
        await call.message.answer(text="Category Nomini kiriting")
        await state.update_data({
            'gender': False
        })
        await state.set_state(CategoryAdd.name)
@dp.message(F.text, CategoryAdd.name)
async def final(message: types.Message, state: FSMContext):
    category_name = message.text
    category_id = random.randint(1, 100)
    data = await state.get_data()
    db.add_category(id=category_id, name=category_name, gender=data['gender'])
    await message.answer(text=f"Category muvaffaqiyatli qoshildi\n"
                                f"ID:{category_id}\n"
                                f"Name:{category_name}\n")

    await state.clear()