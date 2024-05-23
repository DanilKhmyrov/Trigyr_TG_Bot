from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton as kb,
                           InlineKeyboardMarkup, InlineKeyboardButton)

languages = {
    'ru': 'Русский',
    'en': 'Английский',
    'uk': 'Украинский',
    'de': 'Немецкий',
    'es': 'Испанский',
    'fr': 'Французский',
}

main = ReplyKeyboardMarkup(
    keyboard=[[kb(text='/random_word'), kb(text='/get_word')]],
    resize_keyboard=True,
    input_field_placeholder='Введите команду...')

# lang = ReplyKeyboardMarkup(
#     keyboard=[[]],
#     resize_keyboard=True,
#     input_field_placeholder='Введите язык...')


lang = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Русский', callback_data=languages.get('ru'))],
    [InlineKeyboardButton(text='Английский', callback_data=languages.get('en'))],
    [InlineKeyboardButton(text='Немецкий', callback_data=languages.get('de'))]])
