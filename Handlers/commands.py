from aiogram import types, Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.payload import decode_payload

from DataBase.sqlite_db import sql_add_id, sql_select_id, sql_add_message
from KeyBoards.inline_keyboards import kb_start, kb_check_author
from createbot import *
from config import Data
from loggers import handlers_logger


commands_router = Router()

data = {}
msg_reply_id = None

class Form(StatesGroup):
    question = State()


@commands_router.message(CommandStart(deep_link=True))
async def command_handler_start_referral(message: types.Message, command: CommandObject, state: FSMContext):
    args = command.args
    recipient = decode_payload(args)
    username = message.from_user.username
    if not recipient == username:
        await sql_add_id(message)
        recipient_id = await sql_select_id(recipient)
        Data.recipient = recipient_id[0]
        await state.set_state(Form.question)
        await message.answer(f"Задайте любой вопрос {recipient}")
    else:
        handlers_logger.warning(f"Пользователь {message.from_user.id}-{username} написал самому себе по ссылке")
        await message.answer("❌ Вы не можете писать самому себе")


@commands_router.message(Form.question)
async def process_question(message: types.Message, state: FSMContext):
    global msg_reply_id

    await state.update_data(question=message.text)
    data = await state.get_data()
    Data.sender = message.from_user.id
    await state.clear()
    await sql_add_message(message, data['question'], Data.recipient)
    await message.answer(f"✉️ Вы успешно задали вопрос, ждите ответа")

    msg = await bot.send_message(chat_id=Data.recipient, text=f"🎉Вам пришло новое сообщение📨:\n\n<b>{data['question']}</b>\n\n↪️ Свайпни для ответа", reply_markup=kb_check_author.as_markup())
    msg_reply_id = msg.message_id


@commands_router.message(F.reply_to_message, F.chat.func(lambda chat: chat.id == Data.recipient))
async def handle_reply(message: types.Message):
    global msg_reply_id

    if message.reply_to_message.message_id == msg_reply_id:
        replied_msg = message.reply_to_message
        if replied_msg.from_user.id == (await message.bot.me()).id:
            await sql_add_message(message, message.text, Data.sender)
            msg = await bot.send_message(text=f"🎉Вам пришло новое сообщение📨:\n\n<b>{message.text}</b>\n\n↪️ Свайпни для ответа", chat_id=Data.sender)
            msg_reply_id = msg.message_id


@commands_router.message(F.reply_to_message, F.chat.func(lambda chat: chat.id == Data.sender))
async def handle_reply(message: types.Message):
    global msg_reply_id

    if message.reply_to_message.message_id == msg_reply_id:
        replied_msg = message.reply_to_message
        if replied_msg.from_user.id == (await message.bot.me()).id:
            await sql_add_message(message, message.text, Data.recipient)
            msg = await bot.send_message(text=f"🎉Вам пришло новое сообщение📨:\n\n<b>{message.text}</b>\n\n↪️ Свайпни для ответа", chat_id=Data.recipient, reply_markup=kb_check_author.as_markup())
            msg_reply_id = msg.message_id


@commands_router.message(CommandStart())
async def command_handler_start(message: types.Message):
    await sql_add_id(message)
    await message.answer(f'🎉 Добро пожаловать в бота для анонимных вопросов - <a href="https://t.me/AnonQuestAQBot">AnonQuestions</a>.\n\n<b>Начните получать анонимные вопросы прямо сейчас!!!</b>\n\nДля этого создайте ссылку нажав на кнопку ниже ⬇️', reply_markup=kb_start.as_markup())