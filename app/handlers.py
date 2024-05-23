from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from .utils import fetch_random_russian_word, get_word_search

router = Router()


class GetWord(StatesGroup):
    lang = State()
    word = State()


@router.message(CommandStart())
async def on_message(message: Message) -> None:
    await message.answer(
        f'Привет, {message.from_user.full_name}!\n '
        'Этот бот умеет выдавать случайные русские слова, попробуй!',
        reply_markup=kb.main)


@router.message(Command('get_word'))
async def cmd_get_word(message: Message, state: FSMContext):
    await state.set_state(GetWord.lang)
    await message.answer('Выберите язык', parse_mode="HTML",  reply_markup=kb.lang)


# @router.message(GetWord.lang)
# async def state_get_lang(message: Message, state: FSMContext):
#     await state.update_data(lang=message.text)
#     await state.set_state(GetWord.word)
#     await message.answer('Введите слово')

@router.callback_query()
async def select_lang(query: CallbackQuery, state: FSMContext):
    lang_code = query.data
    await state.update_data(lang=lang_code)
    await query.answer(f'Выбран язык {lang_code}')
    await state.set_state(GetWord.word)
    await query.message.answer('Введите слово')


@router.message(GetWord.word)
async def state_get_word(message: Message, state: FSMContext):
    await state.update_data(word=message.text)
    data = await state.get_data()
    await message.answer(get_word_search(data.get('word'), data.get('lang')), parse_mode="HTML", reply_markup=kb.main)
    await state.clear()


@router.message(Command('random_word'))
async def cmd_random_word(message: Message) -> None:
    await message.answer(fetch_random_russian_word(), parse_mode="HTML", reply_markup=kb.main)
