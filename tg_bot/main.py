import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender
from dotenv import load_dotenv

from keyboards import (
    application_keyboard, application_services_keyboard, services_keyboard
)
from text import (
    start_text, menu_text,
)


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


class Form(StatesGroup):
    service = State()
    name = State()
    phone = State()


@dp.message(Command('start'))
async def command_start(message: types.Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.clear()
        await asyncio.sleep(1)
        await message.answer(start_text, reply_markup=services_keyboard())


@router.callback_query(F.data == 'services')
@router.callback_query(F.data == 'application')
async def callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'services':
        await state.clear()
        async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
            await asyncio.sleep(1)
            await call.message.answer(
                text=menu_text, reply_markup=application_keyboard()
                )
            await call.answer()
    elif call.data == 'application':
        await state.clear()
        async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
            await state.set_state(Form.service)
            await call.message.answer(
                text='Выберите услугу',
                reply_markup=application_services_keyboard()
            )
            await call.answer()


@router.callback_query(F.data, Form.service)
async def service(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        if call.data == '1':
            await state.update_data(
                service='услугу по разработке Telegram-ботов под ключ'
            )
            await call.answer()
        elif call.data == '2':
            await state.update_data(
                service='услугу по созданию Mini Apps (встроенных приложений в Telegram)'
            )
            await call.answer()
        elif call.data == '3':
            await state.update_data(
                service='услугу по сопровождению и доработке ботов'
            )
            await call.answer()
        elif call.data == '4':
            await state.update_data(
                service='консультацию и проектирование'
            )
            await call.answer()
        await asyncio.sleep(1)
        await call.message.answer(
            text='Введите ваше имя',
        )
        await state.set_state(Form.name)


@router.message(F.text, Form.name)
async def name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer(
            text='Введите номер телефона'
        )
        await state.set_state(Form.phone)


@router.message(F.text, Form.phone)
async def phone(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    fsm_data = await state.get_data()
    user_service = fsm_data.get('service')
    user_name = fsm_data.get('name')
    user_phone = fsm_data.get('phone')
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer(
            text='Спасибо за предоставленную информацию,'
                 'в ближайшее время мы свяжемся с вами'
                 f'\n Вы выбрали: <b>{user_service}</b>'
                 f'\n Ваше имя: <b>{user_name}</b>'
                 f'\n Ваш телефон: <b>{user_phone}</b>',
            parse_mode='HTML'
        )
        await state.clear()


dp.include_router(router)


async def main() -> None:
    task = asyncio.create_task(dp.start_polling(bot))
    await task

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
