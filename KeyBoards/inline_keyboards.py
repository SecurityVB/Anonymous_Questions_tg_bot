from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


kb_start = InlineKeyboardBuilder()
buttons = [
    InlineKeyboardButton(text=f"🔗 Ссылка для анонимных вопросов", callback_data="make_link"),
    InlineKeyboardButton(text=f"💫 Поддержка автора бота", callback_data="donate_author_bot_menu"),
]
for b in buttons:
    kb_start.add(b)
kb_start.adjust(1)

kb_check_author = InlineKeyboardBuilder()
kb_check_author.add(InlineKeyboardButton(text=f"Посмотреть автора сообщения", callback_data="check_author"))


kb_donate_author = InlineKeyboardBuilder()
buttons = [
    InlineKeyboardButton(text=f"Поддержать автора донатом ⭐", callback_data="donate_author_bot"),
    InlineKeyboardButton(text=f"Поддержать через партнёров 👥", callback_data="referral_links"),
    InlineKeyboardButton(text=f"🔙 Назад", callback_data="back"),
]
for b in buttons:
    kb_donate_author.add(b)
kb_donate_author.adjust(1)


kb_check_author = InlineKeyboardBuilder()
kb_check_author.add(InlineKeyboardButton(text=f"Посмотреть автора сообщения", callback_data="check_author"))


kb_payment_method_check = InlineKeyboardBuilder()
buttons = [
    InlineKeyboardButton(text=f"Оплатить по карте 💳", callback_data="pay_rub_check"),
    InlineKeyboardButton(text=f"Оплатить звёздами ⭐", callback_data="pay_stars_check"),
]
for b in buttons:
    kb_payment_method_check.add(b)
kb_payment_method_check.adjust(1)


kb_payment_method_donate = InlineKeyboardBuilder()
buttons = [
    InlineKeyboardButton(text=f"Оплатить по карте 💳", callback_data="pay_rub_donate"),
    InlineKeyboardButton(text=f"Оплатить звёздами ⭐", callback_data="pay_stars_donate"),
]
for b in buttons:
    kb_payment_method_donate.add(b)
kb_payment_method_donate.adjust(1)


kb_partners = InlineKeyboardBuilder()
buttons = [
    InlineKeyboardButton(text=f"ЗДЁЗДНЫЙ КЛИКЕР", url="https://t.me/rulisturbot?start=_tgr_kIedlkM0NjFi"),
    InlineKeyboardButton(text=f"ЗДЁЗДНЫЙ ПОДАРОК", url="https://t.me/rzvezdatutbot?start=_tgr_y0VXX5o1Y2Zi"),
    InlineKeyboardButton(text=f"ЗВЁЗДНЫЕ БОКСЫ", url="https://t.me/zvezdnyeboksy_bot?start=_tgr_g-tZUjBjZWRi"),
    InlineKeyboardButton(text=f"Easy Gift", url="https://t.me/EasyGiftDropbot?start=_tgr_Q7gzxVlkNDgy"),
    InlineKeyboardButton(text=f"Автопокупка подарков #3", url="https://t.me/AutoThreeRobot?start=_tgr_bIZJFzUyMmFi"),
]
for b in buttons:
    kb_partners.add(b)
kb_partners.adjust(1)