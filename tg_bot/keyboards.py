from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def services_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='📜Услуги', callback_data='services'),
        ],
    ]
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    return inline_keyboard


def application_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text='🪄Оставить заявку', callback_data='application'
            ),
        ],
    ]
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    return inline_keyboard


def application_services_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text='1️⃣Разработка Telegram-ботов под ключ', callback_data='1'
            ),
        ],
        [
            InlineKeyboardButton(
                text='2️⃣Создание Mini Apps (встроенных приложений в Telegram)',
                callback_data='2'
            ),
        ],
        [
            InlineKeyboardButton(
                text='3️⃣Сопровождение и доработка ботов', callback_data='3'
            ),
        ],
        [
            InlineKeyboardButton(
                text='4️⃣Консультации и проектирование', callback_data='4'
            ),
        ],
    ]
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    return inline_keyboard
