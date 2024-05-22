from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
from utils import fetch_random_russian_word

router = Router()


@router.message(CommandStart())
async def on_message(message: Message) -> None:
    await message.answer(f'Привет, {message.from_user.full_name}!\nЭтот бот умеет выдавать случайные русские слова, попробуй!', reply_markup=kb.main)


@router.message(Command('random_word'))
async def random_word(message: Message) -> None:
    await message.answer(fetch_random_russian_word(), parse_mode="HTML", reply_markup=kb.main)
