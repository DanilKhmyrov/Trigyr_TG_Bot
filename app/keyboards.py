from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton as kb,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(
    keyboard=[[kb(text='/random_word')]],
    resize_keyboard=True,
    input_field_placeholder='Введите команду...')


# catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='qwe')]])
