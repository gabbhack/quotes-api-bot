from contextlib import suppress

from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_query_result import (
    InlineQueryResultArticle,
)
from aiogram.types.input_message_content import InputTextMessageContent
from aiogram.utils.markdown import hcode, hlink, quote_html
from pydantic.error_wrappers import ValidationError

from app.core import api


async def cmd_start(msg: types.Message) -> None:
    with suppress(ValidationError):
        await api.create_user(msg.from_user.full_name, msg.from_user.id)

    text = """
Это бот для цитат.\n
Документация к API: https://quotes.apps.xakep.ga/docs/
GitHub Repo: https://github.com/gabbhack/quotes-api-bot
Получить токен: /key
Перевыпустить токен: /revoke
Обновить аккаунт (если поменяли имя): /update
Удалить аккаунт (и цитаты): /delete

Добавить цитату: /add ваша-цитата

Для просмотра цитат нажмите на кнопку Цитаты
"""
    await msg.answer(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Цитаты", switch_inline_query_current_chat=""
                    )
                ]
            ]
        ),
    )


async def cmd_key(msg: types.Message) -> None:
    try:
        user = await api.create_user(msg.from_user.full_name, msg.from_user.id)
    except ValidationError:
        user = await api.get_user(msg.from_user.id)

    await msg.answer(f"Ваш ключ: {hcode(user.api_key)}")


async def cmd_update(msg: types.Message) -> None:
    await api.update_user(msg.from_user.full_name, msg.from_user.id)
    await msg.answer("Данные аккаунта обновлены")


async def cmd_revoke(msg: types.Message) -> None:
    user = await api.revoke_api_key(msg.from_user.id)
    await msg.answer(f"Ваш новый ключ: {hcode(user.api_key)}")


async def cmd_delete(msg: types.Message) -> None:
    await api.delete_user(msg.from_user.id)
    await msg.answer("Ваш аккаунт удален")


async def cmd_add(msg: types.Message) -> None:
    text = msg.get_args()
    if not text:
        await msg.answer("Используйте так: /add ваша-цитата")
        return

    try:
        user = await api.create_user(msg.from_user.full_name, msg.from_user.id)
    except ValidationError:
        user = await api.get_user(msg.from_user.id)

    quote = await api.add_quote(text, user.api_key)

    await msg.answer(f"Цитата {hlink('добавлена', api.make_url(f'quotes/{quote.id}/'))}")


async def inline_quotes(query: types.InlineQuery) -> None:
    offset = int(query.offset) if query.offset else 0
    quotes = await api.quotes(offset)
    await query.answer(
        [
            InlineQueryResultArticle(
                id=i.id,
                title=f"{i.author.name}:",
                description=i.text,
                input_message_content=InputTextMessageContent(
                    message_text=f"{quote_html(i.text)} (C) {quote_html(i.author.name)}\n\n{hlink('Посмотреть через API', api.make_url(f'quotes/{i.id}/'))}"
                ),
            )
            for i in quotes
        ],
        next_offset=offset + 10,
        cache_time=0,
    )
