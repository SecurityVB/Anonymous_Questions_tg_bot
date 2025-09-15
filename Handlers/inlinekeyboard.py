from aiogram import Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, LabeledPrice
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.utils.deep_linking import create_start_link

from DataBase.sqlite_db import sql_select_username
from KeyBoards.inline_keyboards import kb_payment_method_donate, kb_payment_method_check, kb_donate_author, kb_start, \
    kb_partners
from config import PAYMENTS_TOKEN, Data
from createbot import *
from loggers import handlers_logger


inline_kb_router = Router()

value = int()

class Form(StatesGroup):
    price = State()


@inline_kb_router.callback_query(F.data == "make_link")
async def make_link(call: CallbackQuery):
    link = await create_start_link(bot, call.from_user.username, encode=True)
    await bot.send_message(chat_id=call.message.chat.id, text=f"<b>Разместите эту ссылку⬇️</b> в описании своего профиля Telegram, TikTok, Instagram или в канале Telegram.\n\n{link}\n\n<a href='https://t.me/AnonQuestAQBot'>AnonQuestions</a>")


@inline_kb_router.callback_query(F.data == "donate_author_bot")
async def donate_author_bot(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.price)
    await bot.send_message(chat_id=call.message.chat.id, text="🎁 Введите сумму пожертвования <b>без пробелов и спец. знаков</b>\n\n") # ❕Минимальная сумма установленная телеграмом - 10₽")


@inline_kb_router.message(Form.price)
async def process_price(message: types.Message, state: FSMContext):
    global value

    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        value = int(data['price'])
        await donate_send_invoice_stars(message.chat.id)
        # await bot.send_message(chat_id=message.chat.id, text="Выберите удобный для вас способ оплаты", reply_markup=kb_payment_method_donate.as_markup())
    except Exception as err:
        handlers_logger.warning(f"Пользователь ввёл некорректную сумму пожертвования: {err}")
        await message.answer("❌ Вы ввели некорректную сумму пожертвования.")


@inline_kb_router.callback_query(F.data.in_(['pay_rub_donate', 'pay_stars_donate']))
async def process_donate_author_bot(call: CallbackQuery):
    chat_id = call.message.chat.id
    if call.data == 'pay_rub_donate':
        await donate_send_invoice_rub(chat_id)
    if call.data == 'pay_stars_donate':
        await donate_send_invoice_stars(chat_id)



async def donate_send_invoice_rub(chat_id):
    global value

    prices = [LabeledPrice(label="Пожертвовать автору", amount=int(value) * 100)]
    await bot.send_invoice(
        chat_id,
        title="Поддержка автора",
        description="🥺 Поддержите разработчика бота чаевыми",
        provider_token=PAYMENTS_TOKEN,
        currency="rub",
        photo_url="https://images.wallpaperscraft.ru/image/single/dikaia_roza_rozovyj_kust_122926_2560x1080.jpg",
        photo_width=416,
        photo_height=170,
        is_flexible=False,
        prices=prices,
        payload="donate_author"
    )


async def donate_send_invoice_stars(chat_id):
    global value

    # stars = int(value*1.35)
    # if stars % 5 != 0:
    #     while stars % 5 != 0:
    #         stars -= 1

    prices = [LabeledPrice(label="Пожертвовать автору", amount=value)]
    await bot.send_invoice(
        chat_id,
        title="Поддержка автора",
        description="🥺 Поддержите разработчика бота чаевыми",
        provider_token="",
        currency="XTR",
        photo_url="https://images.wallpaperscraft.ru/image/single/dikaia_roza_rozovyj_kust_122926_2560x1080.jpg",
        photo_width=416,
        photo_height=170,
        is_flexible=False,
        prices=prices,
        payload="donate_author"
    )


'''##################################################################################################################'''


@inline_kb_router.callback_query(F.data == "check_author")
async def check_author(call: CallbackQuery):
    await check_author_send_invoice_stars(call.message.chat.id)
    # await bot.send_message(chat_id=call.message.chat.id, text="Выберите удобный для вас способ оплаты", reply_markup=kb_payment_method_check.as_markup())


@inline_kb_router.callback_query(F.data.in_(['pay_rub_check', 'pay_stars_check']))
async def process_check_author(call: CallbackQuery):
    chat_id = call.message.chat.id
    if call.data == 'pay_rub_check':
        await check_author_send_invoice_rub(chat_id)
    if call.data == 'pay_stars_check':
        await check_author_send_invoice_stars(chat_id)


async def check_author_send_invoice_rub(chat_id):
    prices = [LabeledPrice(label="Посмотреть отправителя", amount=50 * 100)]
    await bot.send_invoice(
        chat_id,
        title="Узнать отправителя",
        description="🔍 Вы узнаете человека, который писал это сообщение",
        provider_token=PAYMENTS_TOKEN,
        currency="rub",
        photo_url="https://images.wallpaperscraft.ru/image/single/dikaia_roza_rozovyj_kust_122926_2560x1080.jpg",
        photo_width=416,
        photo_height=170,
        is_flexible=False,
        prices=prices,
        payload="check_sender"
    )


async def check_author_send_invoice_stars(chat_id):
    prices = [LabeledPrice(label="Посмотреть отправителя", amount=65)]
    await bot.send_invoice(
        chat_id,
        title="Узнать отправителя",
        description="🔍 Вы узнаете человека, который писал это сообщение",
        provider_token="",
        currency="XTR",
        photo_url="https://images.wallpaperscraft.ru/image/single/dikaia_roza_rozovyj_kust_122926_2560x1080.jpg",
        photo_width=416,
        photo_height=170,
        is_flexible=False,
        prices=prices,
        payload="check_sender"
    )


'''##################################################################################################################'''

@inline_kb_router.callback_query(F.data == 'donate_author_bot_menu')
async def donate_author_bot_menu(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text="Выберите способ поддержки 👇", reply_markup=kb_donate_author.as_markup())


@inline_kb_router.callback_query(F.data == 'referral_links')
async def donate_author_bot_menu(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text= """
Вы можете пополнить баланс звёзд через этих ботов 👇
Тем самым вы поддержите автора бота

Спасибо за поддержку! 🎉
""", reply_markup=kb_partners.as_markup())


@inline_kb_router.callback_query(F.data == 'back')
async def donate_author_bot_menu(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text="<b>Начните получать анонимные вопросы прямо сейчас!!!</b>\n\nДля этого создайте ссылку нажав на кнопку ниже ⬇️", reply_markup=kb_start.as_markup())