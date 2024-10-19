from aiogram.fsm.state import State, StatesGroup


class ProductAdd(StatesGroup):
    name = State()
    description = State()
    price = State()
    qty = State()
    gender = State()
    discount = State()
    image = State()

class CategoryAdd(StatesGroup):
    gender = State()
    name = State()

class OrderState(StatesGroup):
    waiting_for_product = State()
    waiting_for_quantity = State()
    waiting_for_confirmation = State()


