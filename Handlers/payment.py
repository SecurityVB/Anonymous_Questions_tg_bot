from aiogram import types, Router, F
from aiogram.enums import ContentType

from DataBase.sqlite_db import sql_select_username, sql_add_payment
from config import Data
from createbot import *
from loggers import handlers_logger


payment_router = Router()
author = str()


@payment_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    payload = pre_checkout_q.invoice_payload
    if payload == "check_sender":
        global author
        author = await sql_select_username(Data.sender)
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@payment_router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    global author
    payload = message.successful_payment.invoice_payload
    payment_info = message.successful_payment
    user_id = message.from_user.id
    currency = payment_info.currency
    amount = payment_info.total_amount

    handlers_logger.info(f"Пользователь {user_id}-{message.from_user.username} успешная оплата: currency='{currency}' total_amount='{amount}' invoice_payload='{payment_info.invoice_payload}' telegram_payment_charge_id='{payment_info.telegram_payment_charge_id}' provider_payment_charge_id='{payment_info.provider_payment_charge_id}'")
    await sql_add_payment(user_id, currency, amount)
    if payload == "check_sender":
        await bot.send_message(chat_id=message.chat.id, text=f"@{author[0]} - вот кто вам написал данное сообщение 🔍👁")
    else:
        await bot.send_message(chat_id=message.chat.id, text="<b>🎉 Большое спасибо за поддержку автора бота\!</b>\n\nВаш вклад помогает проекту развиваться и становиться лучше 💙\n")
