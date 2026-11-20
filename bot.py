import asyncio

import shutil

import logging

import random

import sqlite3

import time

from datetime import datetime, timezone, timedelta

from urllib.parse import quote

from quiz import ANIME_EMOJI_QUIZ

from rp_list import RP_TECHNIQUES

from aiogram import Bot, Dispatcher, F, types

from aiogram.filters import Command

from aiogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton,

    ReplyKeyboardMarkup,

    KeyboardButton,

    LabeledPrice,

    PreCheckoutQuery,

    BotCommand,

    InputMediaPhoto,

    FSInputFile,

)

 

logging.basicConfig(level=logging.INFO)

 

BOT_TOKEN = "9059209753:AAFaj8EcKY-I8dvfEqxswjWdyujylqHO4rA"

ADMIN_ID = 6921885296

BOT_USERNAME = "AnimeEnergNFTBot"

COOLDOWN = 3 * 3600

 

BANNERS = {

    "welcome": "",

    "shop": "",

    "levels": "",

    "top": "",

}

 

LEVELS = {

    1: {"name": "Наруто (Генин на минималках)", "need": 250, "reward": "Мишка (15 ⭐)", "photo": "AgACAgIAAxkBAAMxavmpcpkyR321bXlTcO03f0kLewYAAjweaxuKkshLF3b_juZ9rVIBAAMCAAN4AAM9BA"},

    2: {"name": "Танджиро (Угольный барон)", "need": 1000, "reward": "Кольцо (100 ⭐)", "photo": "AgACAgIAAxkBAAMzavmpev7gL0gD-vQSk67j96d0wv0AAj0eaxuKkshL00Zu3USVDb8BAAMCAAN5AAM9BA"},

    3: {"name": "Годжо Сатору (Без повязки)", "need": 3000, "reward": "NFT Pet Snake", "photo": "AgACAgIAAxkBAAM1avmpfkYMtA3verNLxRV7Tzo7liwAAj4eaxuKkshLL-zRwHyaDIgBAAMCAAN5AAM9BA"},

    4: {"name": "Итачи Учиха (Мастер яичницы)", "need": 5000, "reward": "NFT Input Key", "photo": "AgACAgIAAxkBAAM3avmpg_3ZLkv5F-4cuC3KuHTe794AAj8eaxuKkshLnTXQ_6BWI3oBAAMCAAN5AAM9BA"},

    5: {"name": "Сейлор Мун (В поисках обеда)", "need": 7500, "reward": "NFT Moon Pendant", "photo": "AgACAgIAAxkBAAM5avmpiJYXaFcLGINflYIF8kJk4kAAAkAeaxuKkshLXfUwICm8tfQBAAMCAAN5AAM9BA"},

    6: {"name": "Аня Форджер (Агент Сумрак-младший)", "need": 11000, "reward": "NFT Spy Agaric", "photo": "AgACAgIAAxkBAAM7avmpi2Kb1l36v_sHCfmFpXno8kkAAkEeaxuKkshLp4-8UNuOrlABAAMCAAN5AAM9BA"},

    7: {"name": "Саске Учиха (Мститель на диете)", "need": 15000, "reward": "NFT Easter Egg", "photo": ""},

    8: {"name": "Зеницу (Спящий гром)", "need": 19000, "reward": "NFT Whip Cupcake", "photo": ""},

    9: {"name": "Иноске (Кабан без тормозов)", "need": 23000, "reward": "NFT Snoop Cigar", "photo": ""},

    10: {"name": "Какаши (Читатель 18+)", "need": 27500, "reward": "NFT Lunar Snake", "photo": ""},

    11: {"name": "Луффи (Резиновый обжора)", "need": 32500, "reward": "NFT Jolly Chimp", "photo": ""},

    12: {"name": "Зоро (Потерялся в меню)", "need": 37500, "reward": "NFT Homemade Cake", "photo": ""},

    13: {"name": "Санджи (Шеф-повар Конохи)", "need": 43000, "reward": "NFT Spicy Scroll", "photo": ""},

    14: {"name": "Ичиго (Рыжий жнец)", "need": 49000, "reward": "NFT Jingle Bells", "photo": ""},

    15: {"name": "Сайтама (Лысый со скидкой)", "need": 55000, "reward": "NFT Party Sparkler", "photo": ""},

    16: {"name": "Генос (Киборг-пылесос)", "need": 62500, "reward": "NFT Santa Hat", "photo": ""},

    17: {"name": "Леви Аккерман (Мистер Пропер)", "need": 70000, "reward": "NFT Ginger Cookie", "photo": ""},

    18: {"name": "Эрен Йегер (Любитель свободы)", "need": 77500, "reward": "NFT Candy Cane", "photo": ""},

    19: {"name": "Микаса (Хранительница шарфа)", "need": 85000, "reward": "NFT Berry Box", "photo": ""},

    20: {"name": "Кен Канеки (Любитель кофе)", "need": 95000, "reward": "NFT Vintage Cigar", "photo": ""},

    21: {"name": "Денджи (Бензопила за еду)", "need": 105000, "reward": "NFT Eternal Rose", "photo": ""},

    22: {"name": "Пауэр (Президент мира)", "need": 115000, "reward": "NFT Love Potion", "photo": ""},

    23: {"name": "Макима (Контроль бюджета)", "need": 127500, "reward": "NFT Crystal Ball", "photo": ""},

    24: {"name": "Мегуми (Призыватель теней)", "need": 140000, "reward": "NFT Witch Hat", "photo": ""},

    25: {"name": "Юджи Итадори (Сосуд Сукуны)", "need": 152500, "reward": "NFT Skull Flower", "photo": ""},

    26: {"name": "Сукуна (Король проклятий)", "need": 167500, "reward": "NFT Trapped Heart", "photo": ""},

    27: {"name": "Киллуа (Молния на скейте)", "need": 182500, "reward": "NFT Electric Skull", "photo": ""},

    28: {"name": "Гон Фрикс (Камень-ножницы)", "need": 197500, "reward": "NFT Star Notepad", "photo": ""},

    29: {"name": "Хисока (Фокусник с картами)", "need": 215000, "reward": "NFT Magic Potion", "photo": ""},

    30: {"name": "Эдвард Элрик (Не называй коротышкой)", "need": 232500, "reward": "NFT Signet Ring", "photo": ""},

    31: {"name": "Альфонс (Доспех с котиками)", "need": 250000, "reward": "NFT Toy Bear", "photo": ""},

    32: {"name": "Лайт Ягами (Писатель в тетради)", "need": 270000, "reward": "NFT Desk Calendar", "photo": ""},

    33: {"name": "L (Детектив на сладком)", "need": 290000, "reward": "NFT Lol Pop", "photo": ""},

    34: {"name": "Рюк (Яблочный маньяк)", "need": 310000, "reward": "NFT Evil Eye", "photo": ""},

    35: {"name": "Джотаро Куджо (Ярэ-ярэ дазэ)", "need": 332500, "reward": "NFT B-Day Candle", "photo": ""},

    36: {"name": "Дио Брандо (Остановил время)", "need": 355000, "reward": "NFT Swiss Watch", "photo": ""},

    37: {"name": "Джорно Джованна (У меня есть мечта)", "need": 380000, "reward": "NFT Perfume Bottle", "photo": ""},

    38: {"name": "Моб (100% спокойствия)", "need": 405000, "reward": "NFT Hypno Lollipop", "photo": ""},

    39: {"name": "Рейген (Великий экстрасенс)", "need": 430000, "reward": "NFT Top Hat", "photo": ""},

    40: {"name": "Сон Джин-Ву (Поднимитесь!)", "need": 460000, "reward": "NFT Astral Shard", "photo": ""},

    41: {"name": "Гатс (Чёрный мечник)", "need": 490000, "reward": "NFT Ion Gem", "photo": ""},

    42: {"name": "Спайк Шпигель (Космический ковбой)", "need": 520000, "reward": "NFT Loot Bag", "photo": ""},

    43: {"name": "Алукард (Ночной прогульщик)", "need": 550000, "reward": "NFT Scared Cat", "photo": ""},

    44: {"name": "Кирито (Чёрный мечник Айнкрада)", "need": 585000, "reward": "NFT Sharp Tongue", "photo": ""},

    45: {"name": "Асуна (Молния на кухне)", "need": 620000, "reward": "NFT Sakuras", "photo": ""},

    46: {"name": "Рем (Лучшая горничная)", "need": 655000, "reward": "NFT Snow Globe", "photo": ""},

    47: {"name": "Субару (Возвращение из смерти)", "need": 695000, "reward": "NFT Skull", "photo": ""},

    48: {"name": "Аинз Оал Гоун (Владыка склепа)", "need": 735000, "reward": "NFT Necromancer", "photo": ""},

    49: {"name": "Римуру Темпест (Слизь-император)", "need": 780000, "reward": "NFT Jelly Bunny", "photo": ""},

    50: {"name": "Вельдора (Дракон-отаку)", "need": 825000, "reward": "NFT Dragon", "photo": ""},

    51: {"name": "Итачи (Режим Сусаноо)", "need": 875000, "reward": "NFT Durov's Cap", "photo": ""},

    52: {"name": "Мадара Учиха (Танцор шиноби)", "need": 930000, "reward": "NFT Plush Pepe", "photo": ""},

    53: {"name": "Наруто (Режим Бариона)", "need": 990000, "reward": "NFT Precious Peach", "photo": ""},

    54: {"name": "Гоку (Ультра Инстинкт)", "need": 1060000, "reward": "NFT Heart Locket", "photo": ""},

    55: {"name": "Веджета (Принц саян)", "need": 1150000, "reward": "NFT Heroic Helmet", "photo": ""},

    56: {"name": "Бог Аниме (Абсолютный Сенсей)", "need": 1250000, "reward": "NFT Legendary Crown", "photo": ""},

}

 

FARM_TEXTS = [

    "🍜 Герой плотно поел рамена в Ичираку и выдал +{gain}⚡!",

    "🧘‍♂️ Час медитации под водопадом (правда, он проспал) принесли +{gain}⚡!",

    "🔥 Сенсей наорал так громко, что чакра подскочила на +{gain}⚡!",

    "🍙 Нашёл в кармане вчерашний онигири и зарядился на +{gain}⚡!",

    "⚡ Вспомнил грустный флешбэк из детства и превозмог на +{gain}⚡!",

    "🐱 Погладил уличного кота и словил дзен на +{gain}⚡!",

    "💪 Сделал 100 отжиманий (ладно, 3 отжимания и 97 приседаний на диван): +{gain}⚡!"

]

 

WAIT_TEXTS = [

    "😴 Герой дрыхнет без задних ног! Потерпи ещё {h}ч {m}м.",

    "🍜 Он сейчас на обеде в Ичираку, не мешай! Возвращайся через {h}ч {m}м.",

    "🪫 Чакра на нуле, батарейка села. Зарядка закончится через {h}ч {m}м.",

    "🚽 Герой отошёл по важным делам шиноби. Будет через {h}ч {m}м.",

    "🎮 Он залип в приставку и отказывается тренироваться! Жди {h}ч {m}м."

]

 

NOTIFY_TEXTS = [

    "🔔 <b>Твой герой выспался и доел рамен!</b>\nШкала чакры готова к новой тренировке. Залетай в качалку! ⚡",

    "🔥 <b>Перекур окончен, сенсей!</b>\nГерой бьёт копытом и требует влить в него новую порцию энергии! ⚡",

    "🍜 <b>Ау, сенсей!</b>\nПрошло 3 часа — пора снова отправлять подопечного на тренировку! ⚡"

]

 

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

admin_waiting_broadcast = set()

admin_waiting_group_broadcast = set()

admin_waiting_promo = set()

 

db = sqlite3.connect("game_v2.db")

cur = db.cursor()

cur.execute("PRAGMA journal_mode=WAL;")

cur.execute("PRAGMA synchronous=FULL;")

 

def init_db():

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY,

        username TEXT,

        level INTEGER DEFAULT 1,

        energy INTEGER DEFAULT 0,

        last_farm INTEGER DEFAULT 0,

        amulet_until INTEGER DEFAULT 0,

        stars_spent INTEGER DEFAULT 0,

        notified INTEGER DEFAULT 1

    )

    """)

    try:

        cur.execute("ALTER TABLE users ADD COLUMN notified INTEGER DEFAULT 1")

    except sqlite3.OperationalError:

        pass

    cur.execute("CREATE TABLE IF NOT EXISTS claims (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, level INTEGER, reward TEXT, status TEXT DEFAULT 'pending')")

    cur.execute("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, item TEXT, amount INTEGER, created_at INTEGER)")

    cur.execute("CREATE TABLE IF NOT EXISTS referrals (referred_id INTEGER PRIMARY KEY, referrer_id INTEGER, rewarded INTEGER DEFAULT 0)")
    
    try:

        cur.execute("ALTER TABLE referrals ADD COLUMN rewarded INTEGER DEFAULT 0")

    except sqlite3.OperationalError:

        pass

    cur.execute("CREATE TABLE IF NOT EXISTS promocodes (code TEXT PRIMARY KEY, reward INTEGER, uses_left INTEGER)")

    cur.execute("CREATE TABLE IF NOT EXISTS promo_used (user_id INTEGER, code TEXT, PRIMARY KEY (user_id, code))")

    cur.execute("""

    CREATE TABLE IF NOT EXISTS groups (

        chat_id INTEGER PRIMARY KEY,

        title TEXT,

        members_count INTEGER DEFAULT 0,

        actions_count INTEGER DEFAULT 0,

        last_active INTEGER DEFAULT 0

    )

    """)

    for col_sql in [

        "ALTER TABLE groups ADD COLUMN members_count INTEGER DEFAULT 0",

        "ALTER TABLE groups ADD COLUMN actions_count INTEGER DEFAULT 0",

        "ALTER TABLE groups ADD COLUMN last_active INTEGER DEFAULT 0",

    ]:

        try:

            cur.execute(col_sql)

        except sqlite3.OperationalError:

            pass

    cur.execute("CREATE TABLE IF NOT EXISTS ramen_gift (sender_id INTEGER PRIMARY KEY, last_sent INTEGER)")

    db.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")

    cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance', '0')")

    cur.execute("""

    CREATE TABLE IF NOT EXISTS chat_punishments (

        chat_id INTEGER,

        user_id INTEGER,

        user_name TEXT,

        p_type TEXT,

        until_ts INTEGER,

        PRIMARY KEY (chat_id, user_id, p_type)

    )

    """)
    
    cur.execute("""

    CREATE TABLE IF NOT EXISTS chat_members (

        chat_id INTEGER,

        user_id INTEGER,

        user_name TEXT,

        msg_total INTEGER DEFAULT 0,

        msg_today INTEGER DEFAULT 0,

        last_msg_ts INTEGER DEFAULT 0,

        PRIMARY KEY (chat_id, user_id)

    )

    """)


    for col_sql in [

        "ALTER TABLE chat_members ADD COLUMN quiz_wins INTEGER DEFAULT 0",

        "ALTER TABLE chat_members ADD COLUMN first_seen_ts INTEGER DEFAULT 0",

        "ALTER TABLE chat_members ADD COLUMN title TEXT DEFAULT ''",

    ]:

        try:

            cur.execute(col_sql)

        except sqlite3.OperationalError:

            pass
    
    db.commit()




 

init_db()

 

 

def is_maintenance() -> bool:

    cur.execute("SELECT value FROM settings WHERE key = 'maintenance'")

    row = cur.fetchone()

    if not row:

        return False

    (val,) = row

    return val == "1"

 

 

async def check_maint_block(event) -> bool:

    user = getattr(event, "from_user", None)

    if not user or user.id == ADMIN_ID or not is_maintenance():

        return False

 

    text = (

        "🛠 <b>АНИМЕ-КАЧАЛКА НА ТЕХ. ОБСЛУЖИВАНИИ!</b>\n\n"

        "Сенсей прямо сейчас настраивает чакру, обновляет героев и полирует сервера. "

        "Весь твой прогресс надёжно сохранён!\n\n"

        "⏳ <i>Загляни чуть позже — как только закончим, мы сразу пришлём уведомление!</i>"

    )

    try:

        if isinstance(event, types.CallbackQuery):

            await event.answer("🛠 Бот на тех. обслуживании! Скоро вернёмся!", show_alert=True)

        elif isinstance(event, types.Message) and event.chat.type == "private":

            await event.answer(text, parse_mode="HTML")

    except Exception:

        pass

    return True

 

 
@dp.message.outer_middleware()

async def track_groups_middleware(handler, event: types.Message, data: dict):

    if await check_maint_block(event):

        return

    if event.chat and event.chat.type in ("group", "supergroup"):

        cid = event.chat.id

        title = event.chat.title or "Группа без названия"

        now = int(time.time())

        cur.execute("SELECT 1 FROM groups WHERE chat_id = ?", (cid,))

        is_new = cur.fetchone() is None

 

        if is_new:

            try:

                m_count = await bot.get_chat_member_count(cid)

            except Exception:

                m_count = 0

            cur.execute(

                "INSERT INTO groups (chat_id, title, members_count, actions_count, last_active) VALUES (?, ?, ?, 1, ?)",

                (cid, title, m_count, now)

            )

            db.commit()

            try:

                await bot.send_message(

                    ADMIN_ID,

                    f"➕ <b>Бота добавили в новый чат!</b>\n"

                    f"💬 Название: <b>{title}</b>\n"

                    f"👥 Участников: <b>{m_count} чел.</b>\n"

                    f"🆔 ID: <code>{cid}</code>",

                    parse_mode="HTML"

                )

            except Exception:

                pass

        else:

            cur.execute(

                "UPDATE groups SET title = ?, actions_count = actions_count + 1, last_active = ? WHERE chat_id = ?",

                (title, now, cid)

            )

            db.commit()

    if event.chat and event.chat.type in ("group", "supergroup") and event.from_user and not event.from_user.is_bot:

        uid = event.from_user.id

        uname = (event.from_user.full_name or event.from_user.username or "Шиноби").replace("<", "").replace(">", "")

        cid = event.chat.id

        now = int(time.time())

        cur.execute("""

            INSERT INTO chat_members (chat_id, user_id, user_name, msg_total, msg_today, last_msg_ts)

            VALUES (?, ?, ?, 1, 1, ?)

            ON CONFLICT(chat_id, user_id) DO UPDATE SET

                user_name = excluded.user_name,

                msg_total = msg_total + 1,

                msg_today = msg_today + 1,

                last_msg_ts = excluded.last_msg_ts

        """, (cid, uid, uname, now))

        db.commit()

      
    if event.chat and event.chat.type in ("group", "supergroup") and event.text and event.from_user and not event.from_user.is_bot and not event.reply_to_message:

        await try_execute_rp_technique(event)

    return await handler(event, data)
 

 

@dp.my_chat_member()

async def on_bot_added_to_group(event: types.ChatMemberUpdated):

    if event.chat.type not in ("group", "supergroup"):

        return

    new_status = event.new_chat_member.status

    cid = event.chat.id

    title = event.chat.title or "Группа без названия"

    now = int(time.time())

 

    if new_status in ("member", "administrator"):

        try:

            m_count = await bot.get_chat_member_count(cid)

        except Exception:

            m_count = 0

        cur.execute("SELECT 1 FROM groups WHERE chat_id = ?", (cid,))

        is_new = cur.fetchone() is None

        cur.execute(

            "INSERT OR REPLACE INTO groups (chat_id, title, members_count, actions_count, last_active) "

            "VALUES (?, ?, ?, COALESCE((SELECT actions_count FROM groups WHERE chat_id = ?), 0), ?)",

            (cid, title, m_count, cid, now)

        )

        db.commit()

 

        if new_status == "member":

            welcome_group_msg = (

                "👋 <b>Йо, шиноби! Спасибо, что добавили Аниме-Качалку в беседу!</b>\n\n"

                "⚠️ <b>Важный шаг для запуска:</b>\n"

                "Сейчас у меня нет доступа к переписке в чате. Чтобы работали <b>РП-команды</b> (<i>обнять, расэнган, угостить раменом</i>), <b>переводчик цундере</b> и <b>модерация</b>, выдайте мне <b>права администратора</b> в настройках группы!\n\n"

                "📜 Список всех команд чата: <b>/rp</b>\n"

                "🎴 Прокачка героев и призы: <b>/card</b>"

            )

        else:

            welcome_group_msg = (

                "🔥 <b>Аниме-Качалка успешно активирована в чате!</b>\n\n"

                "✅ Права доступа получены — все игры, модерация и РП-команды уже работают!\n"

                "🎭 Отвечайте на сообщения друзей словами из списка <b>/rp</b> или пишите <code>цундере</code>!\n"

                "⚡ Прокачать своего героя: <b>/card</b>"

            )

 

        try:

            await bot.send_message(cid, welcome_group_msg, parse_mode="HTML")

        except Exception:

            pass

 

        if is_new:

            try:

                await bot.send_message(

                    ADMIN_ID,

                    f"➕ <b>Бота добавили в новый чат!</b>\n"

                    f"💬 Название: <b>{title}</b>\n"

                    f"👥 Участников: <b>{m_count} чел.</b>\n"

                    f"🆔 ID: <code>{cid}</code>",

                    parse_mode="HTML"

                )

            except Exception:

                pass

    elif new_status in ("left", "kicked"):

        cur.execute("DELETE FROM groups WHERE chat_id = ?", (cid,))

        db.commit()


 

 

def get_user(user_id, username=""):

    cur.execute(

        "SELECT user_id, username, level, energy, last_farm, amulet_until, stars_spent FROM users WHERE user_id = ?",

        (user_id,)

    )

    user = cur.fetchone()

    if not user:

        clean_name = username or "Без_ника"

        cur.execute("INSERT INTO users (user_id, username, notified) VALUES (?, ?, 1)", (user_id, clean_name))

        db.commit()

        return (user_id, clean_name, 1, 0, 0, 0, 0)

    _, old_uname, lvl, en, lf, am, st = user

    if username and old_uname != username:

        cur.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))

        db.commit()

        return (user_id, username, lvl, en, lf, am, st)

    return user

 

 

def process_referral_reward(referred_id: int):

    cur.execute("SELECT referrer_id, rewarded FROM referrals WHERE referred_id = ?", (referred_id,))

    row = cur.fetchone()

    if not row:

        return None

    referrer_id, rewarded = row

    if rewarded == 1:

        return None

 

    cur.execute("UPDATE referrals SET rewarded = 1 WHERE referred_id = ?", (referred_id,))

    ref_user = get_user(referrer_id)

    _, _, ref_lvl, ref_energy, _, _, _ = ref_user

    lvl_data = LEVELS.get(ref_lvl)

    if lvl_data:

        new_energy = min(ref_energy + 50, lvl_data.get("need"))

        cur.execute("UPDATE users SET energy = ? WHERE user_id = ?", (new_energy, referrer_id))

    db.commit()

    return referrer_id

 

 

def make_progress_bar(current: int, total: int, length: int = 10) -> str:

    if total <= 0:

        return "▓▓▓▓▓▓▓▓▓▓ 100%"

    ratio = min(max(current / total, 0.0), 1.0)

    filled = int(round(length * ratio))

    empty = length - filled

    percent = int(ratio * 100)

    bar = "▓" * filled + "░" * empty

    return f"[{bar}] {percent}%"

 

 

def bottom_menu_keyboard():

    return ReplyKeyboardMarkup(

        keyboard=[

            [KeyboardButton(text="🎴 Мой герой"), KeyboardButton(text="⚡ Впитать энергию")],

            [KeyboardButton(text="🛒 Лавка читера"), KeyboardButton(text="🗺 Дорога славы")],

            [KeyboardButton(text="🏆 Топ-10"), KeyboardButton(text="👥 Друзья (+50⚡)")]

        ],

        resize_keyboard=True,

        one_time_keyboard=True

    )
 

 

def main_keyboard(user_id, level, energy, need):

    buttons = []

    if level in LEVELS:

        if energy >= need:

            buttons.append([InlineKeyboardButton(text="🎁 ЗАБРАТЬ ПОДАРОК (Оставить заявку)", callback_data=f"claim_{user_id}")])

        else:

            buttons.append([InlineKeyboardButton(text="⚡ Впитать энергию", callback_data=f"farm_{user_id}")])

        buttons.append([InlineKeyboardButton(text="🛒 Лавка читера (Бусты за Stars)", callback_data=f"shop_{user_id}")])

    buttons.append([

        InlineKeyboardButton(text="🗺 Дорога славы", callback_data=f"levels_{user_id}"),

        InlineKeyboardButton(text="🏆 Топ-10", callback_data=f"top_{user_id}")

    ])

    buttons.append([InlineKeyboardButton(text="👥 Пригласить друга (+50⚡)", callback_data=f"ref_{user_id}")])

    buttons.append([InlineKeyboardButton(text="📖 Информация и правила", url="https://telegra.ph/Oznakomlenie-11-20")]) 

    return InlineKeyboardMarkup(inline_keyboard=buttons)

 

 

def shop_keyboard(user_id):

    return InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="🔮 Амулет удачи 48ч (50-150⚡) — 40 ⭐", callback_data=f"buy_amulet_{user_id}")],

        [InlineKeyboardButton(text="📦 Кейс с удачей (1-100⚡) — 25 ⭐", callback_data=f"buy_case_{user_id}")],

        [InlineKeyboardButton(text="⚡ Попытка прорыва уровня — 100 ⭐", callback_data=f"buy_skip_{user_id}")],

        [InlineKeyboardButton(text="⬅️ Вернуться к герою", callback_data=f"back_{user_id}")]

    ])

def get_card_text(user):

    _, uname, level, energy, last_farm, amulet_until, _ = user

    now = int(time.time())

    max_lvl = len(LEVELS)

 

    lvl_data = LEVELS.get(level)

    if not lvl_data:

        return (

            f"╭── <b>АНИМЕ-КАЧАЛКА</b> ──╮\n"

            f"👤 Сенсей: <b>@{uname}</b>\n"

            f"🏆 Ранг: <b>Уровень {level} из {max_lvl}</b>\n"

            f"╰───────────────────╯\n\n"

            "🔒 Вы прошли все 56 уровней и стали Богом Аниме! Ждите нового сезона!"

        )

 

    need = lvl_data.get("need")

    p_bar = make_progress_bar(energy, need)

    amulet_status = "🔥 Активен (50–150⚡)" if amulet_until > now else "💤 Спит (1–50⚡)"

 

    wait_time = (last_farm + COOLDOWN) - now

    if wait_time <= 0:

        timer_text = "🟢 <b>Статус:</b> Герой выспался и готов качаться!"

    else:

        hours = wait_time // 3600

        mins = (wait_time % 3600) // 60

        timer_text = f"⏳ <b>Перекур:</b> ещё {hours}ч {mins}м"

 

    return (

        f"╭── 🎴 <b>УРОВЕНЬ {level} / {max_lvl}</b> ──╮\n"

        f"👤 Сенсей: <b>@{uname}</b>\n"

        f"🦸 Герой: <b>{lvl_data.get('name')}</b>\n"

        f"🎁 Награда: <b>{lvl_data.get('reward')}</b>\n"

        f"╰───────────────────╯\n\n"

        f"⚡ <b>Шкала чакры:</b>\n"

        f"<code>{p_bar}</code> (<b>{energy} / {need}</b>)\n\n"

        f"🔮 <b>Амулет удачи:</b> {amulet_status}\n"

        f"{timer_text}"

    )

 

 

def get_shop_text():

    return (

        "╭── 🛒 <b>ЛАВКА ЧИТЕРА</b> ──╮\n"

        "<i>Ускорь прокачку за Telegram Stars ⭐</i>\n"

        "╰───────────────────╯\n\n"

        "🔮 <b>Амулет удачи (40 ⭐)</b>\n"

        "└ На 48 часов отменяет лень героя — выпадает строго от <b>50 до 150⚡</b> за сбор!\n\n"

        "📦 <b>Кейс с удачей (25 ⭐)</b>\n"

        "└ Кот в мешке с энергией! Внутри от <b>1 до 100⚡</b> мгновенно и без таймера.\n\n"

        "⚡ <b>Попытка прорыва (100 ⭐)</b>\n"

        "└ Запрещённая техника сенсея! Даёт шанс мгновенно закрыть весь текущий уровень."

    )

 

 

def get_levels_text(current_level: int = 1):

    max_lvl = len(LEVELS)

    start_lvl = max(1, min(current_level, max_lvl - 11))

    end_lvl = min(max_lvl, start_lvl + 11)

 

    text = (

        f"╭── 🗺 <b>ДОРОГА СЛАВЫ (Ур. {start_lvl}–{end_lvl} из {max_lvl})</b> ──╮\n"

        f"<i>Твои ближайшие герои и награды</i>\n"

        f"╰──────────────────────────────╯\n\n"

    )

    for i in range(start_lvl, end_lvl + 1):

        lvl_data = LEVELS.get(i)

        mark = "👉" if i == current_level else ("✅" if i < current_level else "⬜️")

        text += f"{mark} <b>Ур. {i}:</b> {lvl_data.get('name')}\n   └ {lvl_data.get('need')}⚡ ➔ 🎁 <b>{lvl_data.get('reward')}</b>\n"

 

    if end_lvl < max_lvl:

        final_data = LEVELS.get(max_lvl)

        text += f"\n🏆 <b>Финал (Ур. {max_lvl}):</b> {final_data.get('name')} ➔ 🎁 <b>{final_data.get('reward')}</b>"

    return text

 

 

def get_top_text():

    cur.execute("SELECT username, level, energy FROM users ORDER BY level DESC, energy DESC LIMIT 10")

    rows = cur.fetchall()

    text = (

        "╭── 🏆 <b>ТОП-10 ЛУЧШИХ СЕНСЕЕВ</b> ──╮\n"

        "<i>Самые мощные игроки Аниме-Качалки</i>\n"

        "╰─────────────────────────╯\n\n"

    )

    if not rows:

        return text + "Пока тут пусто. Стань первым!"

 

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for idx, (uname, lvl, en) in enumerate(rows, start=1):

        place = medals.get(idx, f"<b>{idx}.</b>")

        hero_data = LEVELS.get(lvl)

        if hero_data:

            hero_name, *_ = hero_data.get("name").split(" (")

        else:

            hero_name = "Легенда"

        text += f"{place} @{uname} — <b>Ур. {lvl}</b> ({hero_name}, {en}⚡)\n"

    return text

 

 

def get_ref_text(uid: int):

    clean_bot = BOT_USERNAME.replace("@", "").strip()

    slash = chr(47)

    ref_link = f"https:{slash}{slash}t.me{slash}{clean_bot}?start={uid}"

    cur.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND rewarded = 1", (uid,))

    (active_refs,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND rewarded = 0", (uid,))

    (pending_refs,) = cur.fetchone()

 

    text = (

        f"╭── 👥 <b>АКАДЕМИЯ СЕНСЕЯ</b> ──╮\n"

        f"<i>Приводи учеников и получай по +50⚡!</i>\n"

        f"╰───────────────────╯\n\n"

        f"✅ Активных учеников: <b>{active_refs} чел.</b> (+<b>{active_refs * 50}⚡</b>)\n"

        f"⏳ Ждут первой тренировки: <b>{pending_refs} чел.</b>\n\n"

        f"📜 <b>Как получить бонус:</b>\n"

        f"1. Отправь другу свою личную ссылку.\n"

        f"2. Когда он зайдёт и впервые нажмёт <b>«⚡ Впитать энергию»</b> — тебе автоматически упадут <b>+50⚡</b>!\n\n"

        f"🔗 <b>Твоя ссылка (нажми, чтобы скопировать):</b>\n"

        f"<code>{ref_link}</code>"

    )

    return text, ref_link






async def send_or_edit_screen(target, text: str, kb: InlineKeyboardMarkup, photo_id: str = "", is_edit: bool = False):

    if not is_edit:

        if photo_id:

            await target.answer_photo(photo=photo_id, caption=text, parse_mode="HTML", reply_markup=kb)

        else:

            await target.answer(text=text, parse_mode="HTML", reply_markup=kb)

        return

 

    if photo_id:

        if target.photo:

            await target.edit_media(media=InputMediaPhoto(media=photo_id, caption=text, parse_mode="HTML"), reply_markup=kb)

        else:

            await target.delete()

            await target.answer_photo(photo=photo_id, caption=text, parse_mode="HTML", reply_markup=kb)

    else:

        if target.photo:

            await target.delete()

            await target.answer(text=text, parse_mode="HTML", reply_markup=kb)

        else:

            await target.edit_text(text=text, parse_mode="HTML", reply_markup=kb)

 

 

async def send_or_edit_card(target, user, is_edit=False):

    uid, _, lvl, energy, _, _, _ = user

    lvl_data = LEVELS.get(lvl)

    need = lvl_data.get("need") if lvl_data else 0

    photo_id = lvl_data.get("photo") if lvl_data else ""

    text = get_card_text(user)

    kb = main_keyboard(uid, lvl, energy, need)

    await send_or_edit_screen(target, text, kb, photo_id=photo_id, is_edit=is_edit)

 

 

def check_owner(call: types.CallbackQuery, target_id: int):

    if call.from_user.id != ADMIN_ID and is_maintenance():

        return False

    return call.from_user.id == target_id
 

 

@dp.message(Command("start"))

async def cmd_start(message: types.Message):

    uid = message.from_user.id

    parts = (message.text or "").split(maxsplit=1)

    if len(parts) == 2:

        _, raw_ref = parts

        ref_code = raw_ref.strip()

        if ref_code.isdigit():

            referrer_id = int(ref_code)

            if referrer_id != uid:

                cur.execute("SELECT 1 FROM users WHERE user_id = ?", (uid,))

                if not cur.fetchone():

                    cur.execute("INSERT OR IGNORE INTO referrals (referred_id, referrer_id, rewarded) VALUES (?, ?, 0)", (uid, referrer_id))

                    db.commit()

 

    user = get_user(uid, message.from_user.username)

    _, uname, _, _, _, _, _ = user

    welcome_text = (

        f"👋 <b>Йо, @{uname}! Добро пожаловать в Аниме-Качалку!</b>\n\n"

        "Здесь ты станешь великим сенсеем и будешь вливать энергию в легендарных героев — от голодного Наруто до Бога Аниме.\n\n"

        "📜 <b>Правила простые:</b>\n"

        "1️⃣ Раз в 3 часа жми <b>«Впитать энергию»</b> — герой пойдёт тренироваться и принесёт от 1 до 50⚡.\n"

        "2️⃣ Заполнишь шкалу — забирай реальные <b>подарки Telegram и редкие NFT</b>!\n"

        "3️⃣ Лень ждать? Загляни в <b>Лавку читера</b> за Звёздами.\n\n"

        "👇 <i>Используй кнопки снизу для быстрого управления!</i>"

    )

    kb_bottom = bottom_menu_keyboard() if message.chat.type == "private" else None

    welcome_banner = BANNERS.get("welcome")

    if welcome_banner:

        await message.answer_photo(photo=welcome_banner, caption=welcome_text, parse_mode="HTML", reply_markup=kb_bottom)

    else:

        await message.answer(welcome_text, parse_mode="HTML", reply_markup=kb_bottom)

    await send_or_edit_card(message, user, is_edit=False)

 

 

@dp.message(Command("card"))

@dp.message(F.text == "🎴 Мой герой")

async def cmd_card(message: types.Message):

    user = get_user(message.from_user.id, message.from_user.username)

    await send_or_edit_card(message, user, is_edit=False)

 

 

@dp.message(Command("farm"))

@dp.message(F.text == "⚡ Впитать энергию")

async def cmd_farm_text(message: types.Message):

    user = get_user(message.from_user.id, message.from_user.username)

    uid, uname, level, energy, last_farm, amulet_until, _ = user

    now = int(time.time())

 

    lvl_data = LEVELS.get(level)

    if not lvl_data:

        return await message.reply("🔒 Все доступные герои уже на пике формы, ждите обновления!")

    need = lvl_data.get("need")

    if energy >= need:

        return await message.reply("🎁 Шкала полная! Хватит качать, жми кнопку подарка в /card!")

    if now - last_farm < COOLDOWN:

        rem = (last_farm + COOLDOWN) - now

        msg = random.choice(WAIT_TEXTS).format(h=rem // 3600, m=(rem % 3600) // 60)

        return await message.reply(f"@{uname}, {msg}")

 

    gain = random.randint(50, 150) if amulet_until > now else random.randint(1, 50)

    new_energy = min(energy + gain, need)

 

    cur.execute("UPDATE users SET energy = ?, last_farm = ?, notified = 0 WHERE user_id = ?", (new_energy, now, uid))

    db.commit()

 

    referrer_id = process_referral_reward(uid)

    if referrer_id:

        try:

            await bot.send_message(referrer_id, f"🎉 <b>Твой ученик @{uname} прошёл первую тренировку!</b>\nТебе начислено <b>+50⚡</b> к текущему герою!", parse_mode="HTML")

        except Exception:

            pass

 

    phrase = random.choice(FARM_TEXTS).format(gain=gain)

    p_bar = make_progress_bar(new_energy, need)

    await message.reply(f"👤 @{uname}: {phrase}\n<code>{p_bar}</code> (<b>{new_energy}/{need}⚡</b>)", parse_mode="HTML")

@dp.message(Command("shop"))

@dp.message(F.text == "🛒 Лавка читера")

async def cmd_shop_text(message: types.Message):

    uid = message.from_user.id

    get_user(uid, message.from_user.username)

    await send_or_edit_screen(message, get_shop_text(), shop_keyboard(uid), photo_id=BANNERS.get("shop"), is_edit=False)

 

 

@dp.message(Command("levels"))

@dp.message(F.text == "🗺 Дорога славы")

async def cmd_levels_text(message: types.Message):

    uid = message.from_user.id

    user = get_user(uid, message.from_user.username)

    _, _, lvl, _, _, _, _ = user

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎴 Моя карточка", callback_data=f"back_{uid}")]])

    await send_or_edit_screen(message, get_levels_text(lvl), kb, photo_id=BANNERS.get("levels"), is_edit=False)

 

 

@dp.message(Command("top"))

@dp.message(F.text == "🏆 Топ-10")

async def cmd_top_text(message: types.Message):

    uid = message.from_user.id

    get_user(uid, message.from_user.username)

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎴 Моя карточка", callback_data=f"back_{uid}")]])

    await send_or_edit_screen(message, get_top_text(), kb, photo_id=BANNERS.get("top"), is_edit=False)

 

 

@dp.message(Command("ref"))

@dp.message(F.text == "👥 Друзья (+50⚡)")

async def cmd_ref_text(message: types.Message):

    uid = message.from_user.id

    get_user(uid, message.from_user.username)

    text, _ = get_ref_text(uid)

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="🎴 Моя карточка", callback_data=f"back_{uid}")]

    ])

    await message.answer(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data.startswith("ref_"))

async def cb_ref(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Открой свою ссылку командой /ref", show_alert=True)

    text, _ = get_ref_text(target_id)

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="⬅️ Вернуться к герою", callback_data=f"back_{target_id}")]

    ])

    await send_or_edit_screen(call.message, text, kb, photo_id="", is_edit=True)

 



@dp.message(Command("promo"))

async def cmd_use_promo(message: types.Message):

    raw_text = (message.text or "").strip()

    parts = raw_text.split(maxsplit=1)

    if len(parts) < 2:

        return await message.reply("🎟 <b>Как активировать промокод:</b>\nНапиши <code>/promo ТВОЙ_КОД</code>", parse_mode="HTML")

 

    _, code_part = parts

    code = code_part.strip().upper()

    uid = message.from_user.id

    user = get_user(uid, message.from_user.username)

    _, _, level, current_energy, _, _, _ = user

 

    cur.execute("SELECT reward, uses_left FROM promocodes WHERE code = ?", (code,))

    promo = cur.fetchone()

    if not promo:

        return await message.reply(f"❌ Промокод <b>{code}</b> не найден или уже закончился!", parse_mode="HTML")

 

    reward, uses_left = promo

    if uses_left <= 0:

        return await message.reply("😢 Все активации этого промокода уже разобрали!")

 

    cur.execute("SELECT 1 FROM promo_used WHERE user_id = ? AND code = ?", (uid, code))

    if cur.fetchone():

        return await message.reply("⚠️ Ты уже активировал этот промокод ранее!")

 

    lvl_data = LEVELS.get(level)

    need = lvl_data.get("need") if lvl_data else (current_energy + reward)

    if current_energy >= need:

        return await message.reply("🎁 У твоего героя шкала уже полная! Сначала забери подарок в /card, а потом вводи промокод!")

 

    new_energy = min(current_energy + reward, need)

    cur.execute("UPDATE users SET energy = ? WHERE user_id = ?", (new_energy, uid))

    cur.execute("UPDATE promocodes SET uses_left = uses_left - 1 WHERE code = ?", (code,))

    cur.execute("INSERT INTO promo_used (user_id, code) VALUES (?, ?)", (uid, code))

    db.commit()

 

    await message.reply(f"🎉 <b>Промокод {code} активирован!</b>\nНачислено <b>+{reward}⚡</b>! Проверить шкалу: /card", parse_mode="HTML")




@dp.message(F.photo, F.from_user.id == ADMIN_ID)

async def admin_get_photo_id(message: types.Message):

    if message.from_user.id in admin_waiting_broadcast or message.from_user.id in admin_waiting_group_broadcast:

        return

    *_, largest_photo = message.photo

    await message.reply(f"🖼 <b>Код картинки (file_id):</b>\n<code>{largest_photo.file_id}</code>", parse_mode="HTML")

 

 

def get_admin_dashboard():

    now = int(time.time())

    cur.execute("SELECT COUNT(*), SUM(stars_spent) FROM users")

    total_users, total_stars = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM users WHERE last_farm >= ?", (now - 86400,))

    (active_24h,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM users WHERE last_farm >= ?", (now - 7 * 86400,))

    (active_7d,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM groups")

    (groups_count,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM referrals WHERE rewarded = 1")

    (active_refs,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM claims WHERE status = 'pending'")

    (pending_claims,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM claims WHERE status = 'done'")

    (done_claims,) = cur.fetchone()

 

    maint = is_maintenance()

    status_line = "🔴 <b>НА ТЕХ. ОБСЛУЖИВАНИИ</b>" if maint else "🟢 <b>РАБОТАЕТ В ШТАТНОМ РЕЖИМЕ</b>"

 

    text = (

        f"👑 <b>Админ-панель и Аналитика</b>\n"

        f"📡 Статус: {status_line}\n\n"

        f"👥 <b>Аудитория:</b>\n"

        f"∙ Игроков в базе: <b>{total_users}</b>\n"

        f"∙ Активны за 24ч: <b>{active_24h}</b> | за 7д: <b>{active_7d}</b>\n"

        f"∙ Групповых чатов: <b>{groups_count}</b>\n"

        f"∙ Пришло по рефералкам: <b>{active_refs}</b>\n\n"

        f"💰 <b>Финансы и Призы:</b>\n"

        f"∙ Заработано всего: <b>{total_stars or 0} ⭐</b>\n"

        f"∙ Ожидают подарка: <b>{pending_claims} чел.</b> (выдано: {done_claims})"

    )

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [

            InlineKeyboardButton(text="👥 Аудитория", callback_data="adm_sec_aud"),

            InlineKeyboardButton(text=f"💰 Касса и Призы ({pending_claims})", callback_data="adm_sec_cash"),

        ],

        [

            InlineKeyboardButton(text="🚀 Активность", callback_data="adm_sec_act"),

            InlineKeyboardButton(text="🛠 Настройки", callback_data="adm_sec_sys"),

        ],

        [

            InlineKeyboardButton(text="🔄 Обновить сводку", callback_data="admin_refresh"),

        ]

    ])

    return text, kb

 

 

@dp.callback_query(F.data == "adm_sec_aud")

async def cb_adm_sec_aud(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="💬 Статистика чатов", callback_data="admin_groups_stats")],

        [InlineKeyboardButton(text="🏆 Топ донатеров", callback_data="admin_top_donors")],

        [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]

    ])

    await call.message.edit_text("👥 <b>Раздел: Аудитория и Лидеры</b>\nВыберите нужный отчёт:", parse_mode="HTML", reply_markup=kb)

    await call.answer()

 

 

@dp.callback_query(F.data == "adm_sec_cash")

async def cb_adm_sec_cash(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    cur.execute("SELECT COUNT(*) FROM claims WHERE status = 'pending'")

    (pending_claims,) = cur.fetchone()

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text=f"🎁 Заявки на подарки ({pending_claims})", callback_data="admin_claims")],

        [InlineKeyboardButton(text="🧾 История платежей Stars", callback_data="admin_payments")],

        [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]

    ])

    await call.message.edit_text("💰 <b>Раздел: Касса и Выдача призов</b>\nВыберите действие:", parse_mode="HTML", reply_markup=kb)

    await call.answer()

 

 

@dp.callback_query(F.data == "adm_sec_act")

async def cb_adm_sec_act(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="🎟 Создать промокод", callback_data="admin_new_promo")],

        [InlineKeyboardButton(text="📋 Список промокодов", callback_data="admin_list_promo")],

        [InlineKeyboardButton(text="📢 Рассылка в ЛС", callback_data="admin_broadcast")],

        [InlineKeyboardButton(text="📣 Рассылка по чатам", callback_data="admin_group_broadcast")],

        [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]

    ])

    await call.message.edit_text("🚀 <b>Раздел: Активность и Продвижение</b>\nВыберите инструмент:", parse_mode="HTML", reply_markup=kb)

    await call.answer()

 

 

@dp.callback_query(F.data == "adm_sec_sys")

async def cb_adm_sec_sys(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    maint = is_maintenance()

    toggle_btn_text = "🟢 Включить бота (Разослать всем)" if maint else "🔴 Выключить на тех. работы"

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text=toggle_btn_text, callback_data="admin_toggle_maint")],

        [InlineKeyboardButton(text="💾 Скачать полную базу", callback_data="admin_backup")],

        [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]

    ])

    await call.message.edit_text("🛠 <b>Раздел: Система и Резервные копии</b>\nУправление состоянием бота:", parse_mode="HTML", reply_markup=kb)

    await call.answer()



 



@dp.message(Command("admin"))

async def cmd_admin(message: types.Message):

    if message.from_user.id != ADMIN_ID:

        return

    admin_waiting_broadcast.discard(ADMIN_ID)

    admin_waiting_group_broadcast.discard(ADMIN_ID)

    admin_waiting_promo.discard(ADMIN_ID)

    text, kb = get_admin_dashboard()

    await message.answer(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data == "admin_refresh")

async def cb_admin_refresh(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    admin_waiting_broadcast.discard(ADMIN_ID)

    admin_waiting_group_broadcast.discard(ADMIN_ID)

    admin_waiting_promo.discard(ADMIN_ID)

    text, kb = get_admin_dashboard()

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data == "admin_new_promo")

async def cb_admin_new_promo(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    admin_waiting_broadcast.discard(ADMIN_ID)

    admin_waiting_group_broadcast.discard(ADMIN_ID)

    admin_waiting_promo.add(ADMIN_ID)

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin_refresh")]])

    await call.message.edit_text(

        "🎟 <b>Создание нового промокода</b>\n\n"

        "Отправьте следующим сообщением 3 значения через пробел:\n"

        "<code>НАЗВАНИЕ ЭНЕРГИЯ КОЛИЧЕСТВО</code>\n\n"

        "<i>Пример:</i> <code>RAMEN777 200 30</code>",

        parse_mode="HTML",

        reply_markup=kb

    )

 

 

@dp.message(F.from_user.id == ADMIN_ID, lambda m: m.from_user.id in admin_waiting_promo)

async def process_new_promo(message: types.Message):

    admin_waiting_promo.discard(ADMIN_ID)

    parts = (message.text or "").split()

    if len(parts) != 3:

        return await message.reply("❌ Нужно ввести ровно 3 значения через пробел.\nПример: <code>RAMEN777 200 30</code>", parse_mode="HTML")

 

    raw_code, reward_str, uses_str = parts

    if not reward_str.isdigit() or not uses_str.isdigit():

        return await message.reply("❌ Энергия и количество активаций должны быть числами без плюсов.\nПример: <code>RAMEN777 200 30</code>", parse_mode="HTML")

 

    code = raw_code.strip().upper()

    reward = int(reward_str)

    uses = int(uses_str)

 

    cur.execute("INSERT OR REPLACE INTO promocodes (code, reward, uses_left) VALUES (?, ?, ?)", (code, reward, uses))

    db.commit()

    await message.reply(f"✅ <b>Промокод создан!</b>\n🎟 Код: <code>{code}</code>\n⚡ Награда: <b>+{reward}⚡</b>\n👥 Активаций: <b>{uses} шт.</b>", parse_mode="HTML")

 

 

@dp.callback_query(F.data == "admin_list_promo")

async def cb_admin_list_promo(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    cur.execute("SELECT code, reward, uses_left FROM promocodes WHERE uses_left > 0")

    rows = cur.fetchall()

    if not rows:

        return await call.answer("Активных промокодов сейчас нет!", show_alert=True)

    text = "📋 <b>Активные промокоды:</b>\n\n"

    for code, reward, uses in rows:

        text += f"∙ <code>{code}</code> — <b>+{reward}⚡</b> (осталось {uses} шт.)\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]])

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data == "admin_toggle_maint")

async def cb_admin_toggle_maint(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

 

    new_state = "0" if is_maintenance() else "1"

    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('maintenance', ?)", (new_state,))

    db.commit()

 

    text, kb = get_admin_dashboard()

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

    await call.answer("Статус изменён! Запускаю рассылку игрокам...")

 

    cur.execute("SELECT user_id FROM users")

    users = cur.fetchall()

 

    if new_state == "1":

        notify_msg = (

            "🛠 <b>ВНИМАНИЕ, СЕНСЕИ! ТЕХНИЧЕСКИЕ РАБОТЫ</b>\n\n"

            "Мы поставили качалку на короткую паузу, чтобы накатить крутое обновление и улучшить стабильность.\n\n"

            "🔒 <i>Не переживайте: весь ваш уровень, чакра, рефералы и амулеты надёжно сохранены!</i>\n"

            "🔔 Мы сразу напишем вам, как только откроем двери обратно!"

        )

    else:

        notify_msg = (

            "🎉 <b>МЫ ВЕРНУЛИСЬ! ТЕХ. РАБОТЫ ЗАВЕРШЕНЫ!</b>\n\n"

            "Сервера отполированы, чакра кипит — <b>Аниме-Качалка снова открыта для всех!</b> ⚡\n\n"

            "🔥 Залетайте в <b>/card</b>, собирайте энергию и продолжайте путь к редким NFT-подаркам!"

        )

 

    sent = 0

    for (uid,) in users:

        if uid == ADMIN_ID:

            continue

        try:

            await bot.send_message(uid, notify_msg, parse_mode="HTML")

            sent += 1

            await asyncio.sleep(0.05)

        except Exception:

            pass

 

    await call.message.answer(f"📨 <b>Оповещение о смене статуса завершено!</b>\nДоставлено: <b>{sent}</b> игрокам.", parse_mode="HTML")

 

 

@dp.callback_query(F.data == "admin_backup")

async def cb_admin_backup(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    await call.answer("Собираю полный снимок базы...")

    db.commit()

 

    backup_path = "backup_full.db"

    b_conn = sqlite3.connect(backup_path)

    db.backup(b_conn)

    b_conn.close()

 

    cur.execute("SELECT COUNT(*) FROM users")

    (u_cnt,) = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM referrals")

    (r_cnt,) = cur.fetchone()

 

    await call.message.answer_document(

        document=FSInputFile(backup_path),

        caption=(

            f"💾 <b>Полная резервная копия базы данных!</b>\n"

            f"👥 Игроков: <b>{u_cnt}</b> | 🤝 Рефералов: <b>{r_cnt}</b>\n\n"

            f"<i>Сохранены все таблицы до мелочей. Для восстановления просто отправьте этот файл боту в личку.</i>"

        ),

        parse_mode="HTML"

    )
 

 

@dp.message(F.document, F.from_user.id == ADMIN_ID)

async def admin_restore_db(message: types.Message):

    if message.from_user.id != ADMIN_ID:

        return

    doc = message.document

    if not doc.file_name.endswith(".db"):

        return await message.reply("❌ Это не файл базы данных (нужен файл с расширением .db)")

    try:

        file_info = await bot.get_file(doc.file_id)

        temp_path = "temp_restore.db"

        await bot.download_file(file_info.file_path, temp_path)

 

        global db, cur

        db.close()

        shutil.move(temp_path, "game_v2.db")

        db = sqlite3.connect("game_v2.db", check_same_thread=False)

        cur = db.cursor()

        cur.execute("PRAGMA journal_mode=WAL;")

        cur.execute("PRAGMA synchronous=FULL;")

        init_db()

 

        cur.execute("SELECT COUNT(*), COALESCE(SUM(energy), 0) FROM users")

        users_count, total_energy = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM referrals WHERE rewarded = 1")

        (refs_count,) = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM groups")

        (groups_count,) = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM chat_members")

        (members_count,) = cur.fetchone()

 

        await message.reply(

            f"✅ <b>ПОЛНАЯ БАЗА ДАННЫХ ВОССТАНОВЛЕНА!</b>\n\n"

            f"👥 Игроков: <b>{users_count}</b> (сумма энергии: <b>{total_energy}⚡</b>)\n"

            f"🤝 Рефералов: <b>{refs_count}</b>\n"

            f"💬 Групповых чатов: <b>{groups_count}</b>\n"

            f"📊 Участников в статистике чатов: <b>{members_count}</b>",

            parse_mode="HTML"

        )

    except Exception as e:

        await message.reply(f"❌ Ошибка при восстановлении базы: <code>{e}</code>", parse_mode="HTML")






@dp.callback_query(F.data == "admin_top_donors")

async def cb_admin_top_donors(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    cur.execute("SELECT username, user_id, stars_spent, level FROM users WHERE stars_spent > 0 ORDER BY stars_spent DESC LIMIT 10")

    rows = cur.fetchall()

    if not rows:

        return await call.answer("Покупок за Stars пока не было!", show_alert=True)

    text = "🏆 <b>Топ-10 донатеров бота:</b>\n\n"

    for idx, (uname, uid, spent, lvl) in enumerate(rows, start=1):

        text += f"{idx}. @{uname} (ID: <code>{uid}</code>) — <b>{spent} ⭐</b> (Ур. {lvl})\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]])

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data == "admin_payments")

async def cb_admin_payments(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    cur.execute("SELECT username, item, amount, created_at FROM payments ORDER BY id DESC LIMIT 10")

    rows = cur.fetchall()

    if not rows:

        return await call.answer("История платежей пока пуста!", show_alert=True)

    item_names = {"amulet": "🔮 Амулет", "case": "📦 Кейс", "skip": "⚡ Прорыв"}

    text = "🧾 <b>Последние 10 покупок Stars:</b>\n\n"

    for uname, item, amount, ts in rows:

        dt = datetime.fromtimestamp(ts).strftime("%d.%m %H:%M")

        text += f"∙ <code>{dt}</code> | @{uname} — {item_names.get(item, item)} (<b>{amount} ⭐</b>)\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]])

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data == "admin_broadcast")

async def cb_admin_broadcast(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    admin_waiting_promo.discard(ADMIN_ID)

    admin_waiting_group_broadcast.discard(ADMIN_ID)

    admin_waiting_broadcast.add(ADMIN_ID)

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin_refresh")]])

    await call.message.edit_text("📢 <b>Рассылка в личку игрокам</b>\n\nОтправьте следующим сообщением текст или фото с подписью.", parse_mode="HTML", reply_markup=kb)

 

 

@dp.message(F.from_user.id == ADMIN_ID, lambda m: m.from_user.id in admin_waiting_broadcast)

async def process_broadcast(message: types.Message):

    admin_waiting_broadcast.discard(ADMIN_ID)

    cur.execute("SELECT user_id FROM users")

    users = cur.fetchall()

    sent = 0

    for (uid,) in users:

        try:

            await message.copy_to(chat_id=uid)

            sent += 1

            await asyncio.sleep(0.05)

        except Exception:

            pass

    await message.answer(f"✅ <b>Рассылка в ЛС завершена!</b>\nДоставлено: <b>{sent}</b> из {len(users)} игроков.", parse_mode="HTML")





@dp.callback_query(F.data == "admin_groups_stats")

async def cb_admin_groups_stats(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    cur.execute(

        "SELECT chat_id, title, members_count, actions_count, last_active "

        "FROM groups ORDER BY actions_count DESC LIMIT 15"

    )

    rows = cur.fetchall()

    if not rows:

        return await call.answer("Бот пока не добавлен ни в один чат!", show_alert=True)

 

    cur.execute("SELECT COUNT(*), SUM(members_count), SUM(actions_count) FROM groups")

    total_chats, total_members, total_actions = cur.fetchone()

 

    text = (

        f"💬 <b>Статистика групповых чатов</b>\n"

        f"∙ Всего групп: <b>{total_chats}</b> | Участников: <b>{total_members or 0}</b>\n"

        f"∙ Всего действий в чатах: <b>{total_actions or 0}</b>\n\n"

        f"<b>Топ-15 активных чатов:</b>\n"

    )

    for idx, (cid, title, members, actions, last_ts) in enumerate(rows, start=1):

        clean_title = (title or "Чат").replace("<", "").replace(">", "")

        dt = datetime.fromtimestamp(last_ts).strftime("%d.%m %H:%M") if last_ts else "—"

        text += (

            f"{idx}. <b>{clean_title}</b> (👥 {members or '?'})\n"

            f"   └ Действий: <b>{actions or 0}</b> | Актив: <code>{dt}</code>\n"

        )

 

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="🔄 Обновить участников", callback_data="admin_groups_refresh")],

        [InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")]

    ])

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

 

 

@dp.callback_query(F.data == "admin_groups_refresh")

async def cb_admin_groups_refresh(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    await call.answer("Обновляю данные по чатам...")

    cur.execute("SELECT chat_id FROM groups")

    chats = cur.fetchall()

    for (cid,) in chats:

        try:

            chat_obj = await bot.get_chat(cid)

            m_count = await bot.get_chat_member_count(cid)

            cur.execute(

                "UPDATE groups SET title = ?, members_count = ? WHERE chat_id = ?",

                (chat_obj.title or "Чат", m_count, cid)

            )

        except Exception:

            cur.execute("DELETE FROM groups WHERE chat_id = ?", (cid,))

    db.commit()

    await cb_admin_groups_stats(call)

 

 

@dp.callback_query(F.data == "admin_group_broadcast")

async def cb_admin_group_broadcast(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    admin_waiting_promo.discard(ADMIN_ID)

    admin_waiting_broadcast.discard(ADMIN_ID)

    admin_waiting_group_broadcast.add(ADMIN_ID)

    cur.execute("SELECT COUNT(*) FROM groups")

    (groups_count,) = cur.fetchone()

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin_refresh")]])

    await call.message.edit_text(
          f"📣 <b>Рассылка по групповым чатам</b>\nВ базе чатов: <b>{groups_count}</b>\n\nОтправьте следующим сообщением текст или фото с подписью.",

        parse_mode="HTML",

        reply_markup=kb

    )

 

 

@dp.message(F.from_user.id == ADMIN_ID, lambda m: m.from_user.id in admin_waiting_group_broadcast)

async def process_group_broadcast(message: types.Message):

    admin_waiting_group_broadcast.discard(ADMIN_ID)

    cur.execute("SELECT chat_id FROM groups")

    chats = cur.fetchall()

    sent = 0

    for (cid,) in chats:

        try:

            await message.copy_to(chat_id=cid)

            sent += 1

            await asyncio.sleep(0.05)

        except Exception:

            cur.execute("DELETE FROM groups WHERE chat_id = ?", (cid,))

            db.commit()

    await message.answer(f"✅ <b>Рассылка по чатам завершена!</b>\nДоставлено в <b>{sent}</b> групп.", parse_mode="HTML")

 

 

@dp.callback_query(F.data == "admin_claims")

async def cb_admin_claims(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    cur.execute("SELECT id, user_id, username, level, reward FROM claims WHERE status = 'pending' LIMIT 10")

    rows = cur.fetchall()

    if not rows:

        return await call.answer("Активных заявок нет!", show_alert=True)

    text = "🎁 <b>Невыданные подарки:</b>\n\n"

    buttons = []

    for cid, uid, uname, lvl, rew in rows:

        text += f"#{cid} | @{uname} (ID: <code>{uid}</code>) — Ур.{lvl} ({rew})\n"

        buttons.append([InlineKeyboardButton(text=f"✅ Выдано #{cid} (@{uname})", callback_data=f"done_claim_{cid}")])

    buttons.append([InlineKeyboardButton(text="⬅️ Назад в админку", callback_data="admin_refresh")])

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

 

 

@dp.callback_query(F.data.startswith("done_claim_"))

async def cb_done_claim(call: types.CallbackQuery):

    if call.from_user.id != ADMIN_ID:

        return

    _, _, cid_str = call.data.split("_")

    cur.execute("UPDATE claims SET status = 'done' WHERE id = ?", (int(cid_str),))

    db.commit()

    await call.answer("Заявка закрыта!", show_alert=True)

    await cb_admin_claims(call)

BAN_TEXTS = [

    "🔨 <b>Техника запечатывания Шинигами!</b> {t_name} изгнан(а) из беседы <b>{dur}</b>!",

    "🌀 <b>Камуи!</b> {t_name} отправлен(а) в другое измерение <b>{dur}</b>!",

    "💥 <b>Аматерасу!</b> {t_name} выжжен(а) из списка участников <b>{dur}</b>!",

    "⚔️ <b>Райкири в бан-лист!</b> {t_name} покидает нашу деревню <b>{dur}</b>!",

]

 

UNBAN_TEXTS = [

    "🕊 <b>Эдо Тенсей!</b> {t_name} воскрешён(а) и снова может вернуться в беседу!",

    "✨ <b>Печать снята!</b> {t_name} официально разбанен(а) — двери Конохи снова открыты!",

]

 

MUTE_TEXTS = [

    "🔇 <b>Техника теневого молчания!</b> {t_name} запечатал(а) рот <b>на {dur}</b>!",

    "🤐 <b>Гендзюцу тишины!</b> {t_name} отправлен(а) медитировать в мут <b>на {dur}</b>!",

    "🍙 <b>Рот забит онигири!</b> {t_name} не сможет писать в чат <b>{dur}</b>!",

    "⚡ <b>Чидори по клавиатуре!</b> {t_name} отдыхает в муте <b>{dur}</b>!",

]

 

UNMUTE_TEXTS = [

    "🔊 <b>Кай! Гендзюцу рассеяно!</b> С {t_name} снят мут, снова можно болтать!",

    "🎉 <b>Голос вернулся!</b> {t_name} снова в строю и может писать в беседу!",

]

 

 

async def is_chat_admin_or_creator(chat_id: int, user_id: int) -> bool:

    if user_id == ADMIN_ID:

        return True

    try:

        member = await bot.get_chat_member(chat_id, user_id)

        if member.status in ("creator", "administrator"):

            return True

    except Exception:

        pass

    return False

 

 

def parse_duration(args_list: list) -> tuple[int, str]:

    if not args_list:

        return 0, "навсегда"

 

    num_str = ""

    unit_str = ""

    for item in args_list:

        digits = "".join(ch for ch in item if ch.isdigit())

        letters = "".join(ch for ch in item if ch.isalpha())

        if digits and not num_str:

            num_str = digits

        if letters and not unit_str:

            unit_str = letters

 

    if not num_str:

        return 0, "навсегда"

 

    val = int(num_str)

    if val <= 0:

        return 0, "навсегда"

 

    if unit_str.startswith("с") or unit_str.startswith("s"):

        return max(val, 35), f"{val} сек."

    if unit_str.startswith("ч") or unit_str.startswith("h"):

        return val * 3600, f"{val} ч."

    if unit_str.startswith("д") or unit_str.startswith("d"):

        return val * 86400, f"{val} дн."

    if unit_str.startswith("н") or unit_str.startswith("w"):

        return val * 604800, f"{val} нед."

    if unit_str.startswith("мес") or unit_str.startswith("mo"):

        return val * 2592000, f"{val} мес."

 

    return val * 60, f"{val} мин."

 

 
   
@dp.message(F.reply_to_message, F.text)

async def handle_chat_moderation(message: types.Message):

    parts = (message.text or "").strip().lower().split()

    cmd = parts.pop(0) if parts else ""

    if message.chat.type not in ("group", "supergroup") or cmd not in ("бан", "разбан", "мут", "размут"):

        return await try_execute_rp_technique(message)
 

    is_boss = await is_chat_admin_or_creator(message.chat.id, message.from_user.id)

    if not is_boss:

        return await message.reply("⛔ <b>Эта техника доступна только создателю и админам чата!</b>", parse_mode="HTML")

 

    target = message.reply_to_message.from_user

    if target.id == bot.id:

        return await message.reply("😤 Б-бака! Я сам себя запечатывать не буду!")

 

    target_is_boss = await is_chat_admin_or_creator(message.chat.id, target.id)

    if target_is_boss:

        return await message.reply("🛡 Нельзя применить наказание к создателю или администратору!")

 

    clean_name = (target.full_name or target.username or "Шиноби").replace("<", "").replace(">", "")

    t_name = f"<b>{clean_name}</b>"

    cid = message.chat.id

    now = int(time.time())

 

    try:

        if cmd == "бан":

            seconds, label = parse_duration(parts)

            until = (now + seconds) if seconds > 0 else 0

            dur_text = f"на {label}" if seconds > 0 else "навсегда"

            if seconds > 0:

                await bot.ban_chat_member(cid, target.id, until_date=until)

            else:

                await bot.ban_chat_member(cid, target.id)

            cur.execute("INSERT OR REPLACE INTO chat_punishments (chat_id, user_id, user_name, p_type, until_ts) VALUES (?, ?, ?, 'ban', ?)", (cid, target.id, clean_name, until))

            db.commit()

            await message.answer(random.choice(BAN_TEXTS).format(t_name=t_name, dur=dur_text), parse_mode="HTML")

 

        elif cmd == "разбан":

            await bot.unban_chat_member(cid, target.id, only_if_banned=True)

            cur.execute("DELETE FROM chat_punishments WHERE chat_id = ? AND user_id = ? AND p_type = 'ban'", (cid, target.id))

            db.commit()

            await message.answer(random.choice(UNBAN_TEXTS).format(t_name=t_name), parse_mode="HTML")

 

        elif cmd == "мут":

            seconds, label = parse_duration(parts)

            if seconds == 0:

                seconds, label = 3600, "60 мин."

            until = now + seconds

            perms = types.ChatPermissions(can_send_messages=False)

            await bot.restrict_chat_member(cid, target.id, permissions=perms, until_date=until)

            cur.execute("INSERT OR REPLACE INTO chat_punishments (chat_id, user_id, user_name, p_type, until_ts) VALUES (?, ?, ?, 'mute', ?)", (cid, target.id, clean_name, until))

            db.commit()

            await message.answer(random.choice(MUTE_TEXTS).format(t_name=t_name, dur=label), parse_mode="HTML")

 

        elif cmd == "размут":

            perms = types.ChatPermissions(can_send_messages=True, can_send_audios=True, can_send_documents=True, can_send_photos=True, can_send_videos=True, can_send_video_notes=True, can_send_voice_notes=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)

            await bot.restrict_chat_member(cid, target.id, permissions=perms)

            cur.execute("DELETE FROM chat_punishments WHERE chat_id = ? AND user_id = ? AND p_type = 'mute'", (cid, target.id))

            db.commit()

            await message.answer(random.choice(UNMUTE_TEXTS).format(t_name=t_name), parse_mode="HTML")

 

    except Exception as e:

        await message.reply(f"⚠️ <b>Не удалось выполнить технику!</b>\nПричина: <code>{e}</code>", parse_mode="HTML") 

 

 

@dp.message(F.text.lower().in_({"список мутов", "список банов"}))

async def handle_punishments_list(message: types.Message):

    if message.chat.type not in ("group", "supergroup"):

        return

 

    cmd = message.text.strip().lower()

    p_type = "mute" if "мут" in cmd else "ban"

    cid = message.chat.id

    now = int(time.time())

 

    cur.execute("DELETE FROM chat_punishments WHERE chat_id = ? AND until_ts > 0 AND until_ts <= ?", (cid, now))

    db.commit()

 

    cur.execute(

        "SELECT user_id, user_name, until_ts FROM chat_punishments WHERE chat_id = ? AND p_type = ?",

        (cid, p_type)

    )

    rows = cur.fetchall()

 

    if not rows:

        empty_msg = "🟢 <b>В этом чате сейчас никто не сидит в муте!</b>" if p_type == "mute" else "🟢 <b>Список забаненных в этом чате пуст!</b>"

        return await message.reply(empty_msg, parse_mode="HTML")

 

    header = "🔇 <b>Список замученных в чате:</b>\n\n" if p_type == "mute" else "🔨 <b>Список забаненных в чате:</b>\n\n"

    text = header

    for idx, (uid, uname, until_ts) in enumerate(rows, start=1):

        if until_ts == 0:

            time_left = "навсегда"

        else:

            dt = datetime.fromtimestamp(until_ts).strftime("%d.%m в %H:%M")

            time_left = f"до <code>{dt}</code>"

        text += f"{idx}. <b>{uname}</b> (ID: <code>{uid}</code>) — {time_left}\n"

 

    await message.reply(text, parse_mode="HTML")



@dp.message(F.text.lower().in_({"стата", "топ", "топ чата", "молчуны"}))

async def handle_chat_activity_stats(message: types.Message):

    if message.chat.type not in ("group", "supergroup"):

        return

 

    cmd = message.text.strip().lower()

    cid = message.chat.id

    now = int(time.time())

 

    if cmd == "молчуны":

        three_days_ago = now - (3 * 86400)

        cur.execute("""

            SELECT user_name, last_msg_ts, msg_total

            FROM chat_members

            WHERE chat_id = ? AND last_msg_ts < ?

            ORDER BY last_msg_ts ASC LIMIT 25

        """, (cid, three_days_ago))

        rows = cur.fetchall()

        if not rows:

            return await message.reply("🔥 <b>Красавцы! В этом чате нет молчунов — все писали за последние 3 дня!</b>", parse_mode="HTML")

 

        text = "😴 <b>Список молчунов чата (молчат больше 3 дней):</b>\n\n"

        for idx, (uname, last_ts, total) in enumerate(rows, start=1):

            days_silent = max(1, (now - last_ts) // 86400)

            text += f"{idx}. <b>{uname}</b> — молчит <b>{days_silent} дн.</b> (всего: {total} сообщ.)\n"

        return await message.reply(text, parse_mode="HTML")

 

    cur.execute("""

        SELECT user_name, msg_total, msg_today

        FROM chat_members

        WHERE chat_id = ?

        ORDER BY msg_total DESC LIMIT 50

    """, (cid,))

    rows = cur.fetchall()

 

    if not rows:

        return await message.reply("📊 Статистика чата пока пуста — напишите пару сообщений!", parse_mode="HTML")

 

    cur.execute("SELECT SUM(msg_total), SUM(msg_today) FROM chat_members WHERE chat_id = ?", (cid,))

    sum_total, sum_today = cur.fetchone()

 

    text = (

        f"📊 <b>ТОП-50 БОЛТУНОВ ЧАТА</b>\n"

        f"💬 Всего сообщений: <b>{sum_total or 0}</b> (за сегодня: <b>{sum_today or 0}</b>)\n\n"

    )

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for idx, (uname, total, today) in enumerate(rows, start=1):

        mark = medals.get(idx, f"<b>{idx}.</b>")

        text += f"{mark} <b>{uname}</b> — <b>{total}</b> сообщ. (сегодня: +{today})\n"

 

    await message.reply(text, parse_mode="HTML")


    


active_emoji_quiz = {}

used_quiz_indices = {}

async def process_emoji_quiz_answer(event: types.Message):

    cid = event.chat.id

    if cid not in active_emoji_quiz:

        return

    guess = event.text.strip().lower().replace(",", "").replace(".", "").replace("!", "").replace(":", "")

    quiz = active_emoji_quiz.get(cid)

    if guess not in quiz.get("answers"):

        return

    title = quiz.get("title")

    del active_emoji_quiz[cid]

    uname = (event.from_user.full_name or event.from_user.username or "Шиноби").replace("<", "").replace(">", "")

    try:

        await event.reply(

            f"🎉 <b>ЕСТЬ ПРАВИЛЬНЫЙ ОТВЕТ!</b>\n\n"

            f"🏆 Самый быстрый знаток аниме: <b>{uname}</b>\n"

            f"🎬 Загаданный тайтл: <b>{title}</b>\n\n"

            f"<i>Напиши <code>викторина</code> для нового раунда!</i>",

            parse_mode="HTML"

        )

    except Exception:

        pass

 

 

def get_next_quiz_for_chat(cid: int):

    used = used_quiz_indices.setdefault(cid, set())

    available = [i for i in range(len(ANIME_EMOJI_QUIZ)) if i not in used]

    if not available:

        used.clear()

        available = list(range(len(ANIME_EMOJI_QUIZ)))

    chosen_idx = random.choice(available)

    used.add(chosen_idx)

    emojis, answers, title = ANIME_EMOJI_QUIZ[chosen_idx]

    return emojis, answers, title, len(available) - 1

 

 

@dp.message(F.text.lower().in_({"викторина", "эмодзи", "сдаюсь"}))

async def handle_emoji_quiz_cmd(message: types.Message):

    if message.chat.type not in ("group", "supergroup"):

        return await message.reply("🧠 Викторина работает в групповых чатах! Добавь меня в беседу с друзьями!")

 

    cid = message.chat.id

    cmd = message.text.strip().lower()

    now = int(time.time())

 

    if cmd == "сдаюсь":

        quiz = active_emoji_quiz.get(cid)

        if not quiz:

            return await message.reply("🤷‍♂️ Сейчас нет активной загадки! Напиши <code>викторина</code>, чтобы начать.", parse_mode="HTML")

        if now - quiz.get("ts") < 15:

            return await message.reply("⏳ Подождите хотя бы 15 секунд, дайте ребятам подумать!")

        title = quiz.get("title")

        del active_emoji_quiz[cid]

        return await message.reply(f"🏳️ <b>Никто не угадал!</b> Это было аниме: <b>{title}</b>\nПишите <code>викторина</code> для нового раунда!", parse_mode="HTML")

 

    if cid in active_emoji_quiz:

        q = active_emoji_quiz.get(cid)

        return await message.reply(

            f"🧠 <b>Загадка уже идёт!</b> Угадайте аниме по эмодзи:\n\n"

            f"👉 <b>{q.get('emojis')}</b>\n\n"

            f"<i>Пишите название прямо в чат!</i>",

            parse_mode="HTML"

        )

 

    emojis, answers, title, left_cnt = get_next_quiz_for_chat(cid)

    active_emoji_quiz[cid] = {"emojis": emojis, "answers": answers, "title": title, "ts": now}

    await message.answer(

        f"🧠 <b>АНИМЕ-ВИКТОРИНА!</b> (Новых в колоде: {left_cnt})\n"

        f"Угадайте тайтл по смайликам:\n\n"

        f"👉 <b>{emojis}</b>\n\n"

        f"💬 <i>Пишите название прямо в чат!</i>",

        parse_mode="HTML"

    )

 

 

async def auto_emoji_quiz_loop():

    msk = timezone(timedelta(hours=3))

    last_sent_slot = ""

 

    while True:

        await asyncio.sleep(30)

        now_msk = datetime.now(msk)

        slot_key = now_msk.strftime("%Y-%m-%d-%H")

 

        if now_msk.hour % 2 == 0 and now_msk.minute == 0 and last_sent_slot != slot_key:

            last_sent_slot = slot_key

            cur.execute("SELECT chat_id FROM groups")

            chats = cur.fetchall()

            now = int(time.time())

 

            for (cid,) in chats:

                if cid in active_emoji_quiz:

                    del active_emoji_quiz[cid]

 

                emojis, answers, title, left_cnt = get_next_quiz_for_chat(cid)

                active_emoji_quiz[cid] = {"emojis": emojis, "answers": answers, "title": title, "ts": now}

                try:

                    await bot.send_message(

                        cid,

                        f"⏰ <b>ВРЕМЯ ДЛЯ АНИМЕ-ВИКТОРИНЫ!</b> (Каждые 2 часа)\n"

                        f"Угадайте тайтл по смайликам:\n\n"

                        f"👉 <b>{emojis}</b>\n\n"

                        f"💬 <i>Кто первый напишет название в чат?</i>",

                        parse_mode="HTML"

                    )

                    await asyncio.sleep(0.1)

                except Exception:

                    active_emoji_quiz.pop(cid, None)



@dp.message(Command("rp"))

async def cmd_rp_help(message: types.Message):

    words = ", ".join(f"<code>{k}</code>" for k in RP_TECHNIQUES.keys())

    rp_list = (

        "😤 <b>ЦУНДЕРЕ РП-КОМАНДЫ В ЧАТЕ</b>\n\n"

        "<b>Как использовать:</b>\n"

        "1️⃣ Ответь (Reply) на сообщение друга командой ниже\n"

        "2️⃣ Или напиши в чат: <code>обнять @ник</code>\n"

        "3️⃣ Нажми <b>Enter</b> и напиши фразу с новой строки — персонаж скажет её после действия!\n\n"

        f"💬 <b>Доступные слова ({len(RP_TECHNIQUES)} шт.):</b>\n{words}"

    )

    await message.reply(rp_list, parse_mode="HTML")

 

 

def make_user_link(user: types.User) -> str:

    safe_name = (user.full_name or user.username or "Шиноби").replace("<", "").replace(">", "")

    return f'<a href="tg://user?id={user.id}"><b>{safe_name}</b></a>'

 

 

async def try_execute_rp_technique(message: types.Message) -> bool:

    if message.chat.type not in ("group", "supergroup") or not message.text:

        return False

 

    first_line, *rest_lines = message.text.strip().split("\n", 1)

    first_line = first_line.strip()

    speech = rest_lines.pop(0).strip() if rest_lines else ""

 

    lower_line = first_line.lower()

    if lower_line == "цундере" or lower_line.startswith("цундере "):

        await handle_tsundere_translator(message)

        return True

 

    matched_cmd = ""

    rest_text = ""

 

    for cmd_key in sorted(RP_TECHNIQUES.keys(), key=len, reverse=True):

        if lower_line == cmd_key or lower_line.startswith(cmd_key + " "):

            matched_cmd = cmd_key

            rest_text = first_line[len(cmd_key):].strip()

            break

 

    if not matched_cmd:

        return False

 

    sender = message.from_user

    target_link = ""

 

    if message.reply_to_message and message.reply_to_message.from_user:

        target_user = message.reply_to_message.from_user

        if target_user.id == sender.id:

            await message.reply("😤 Н-нельзя применять это на самого себя, бака!")

            return True

        if target_user.id == bot.id:

            await message.reply("🛡️ Хмф! Руки прочь от бота!")

            return True

        target_link = make_user_link(target_user)

    elif rest_text:

        mention_user = None

        if message.entities:

            for ent in message.entities:

                if ent.type == "text_mention" and ent.user:

                    mention_user = ent.user

                    break

        if mention_user:

            target_link = make_user_link(mention_user)

        else:

            raw_tag, *_ = rest_text.split()

            clean_tag = raw_tag.replace("<", "").replace(">", "")

            if clean_tag.startswith("@"):

                uname_clean = clean_tag[1:]

                cur.execute(

                    "SELECT user_id, user_name FROM chat_members WHERE chat_id = ? AND LOWER(user_name) = ?",

                    (message.chat.id, uname_clean.lower())

                )

                row = cur.fetchone()

                if row:

                    db_uid, db_uname = row

                    target_link = f'<a href="tg://user?id={db_uid}"><b>{db_uname}</b></a>'

                else:

                    target_link = f'<a href="https://t.me{uname_clean}"><b>{clean_tag}</b></a>'

            else:

                target_link = f"<b>{clean_tag}</b>"

    else:

        return False

 

    emoji, action_tpl, reaction = RP_TECHNIQUES[matched_cmd]

    sender_link = make_user_link(sender)

    action_line = action_tpl.format(s=sender_link, t=target_link)

 

    result_text = f"{emoji} <i>{action_line}</i>"

    if speech:

        safe_speech = speech.replace("<", "").replace(">", "")

        result_text += f"\n🗯️ {sender_link}: <i>«{safe_speech}»</i>"

    result_text += f"\n💢 <b>Реакция:</b> <i>{reaction}</i>"

 

    await message.answer(result_text, parse_mode="HTML", disable_web_page_preview=True)

    return True




@dp.callback_query(F.data.startswith("back_"))

async def cb_back(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Вызови своего героя командой /card", show_alert=True)

    await send_or_edit_card(call.message, get_user(target_id), is_edit=True)

 


@dp.callback_query(F.data.startswith("levels_"))

async def cb_levels(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Вызови своё меню командой /card", show_alert=True)

    user = get_user(target_id)

    _, _, lvl, _, _, _, _ = user

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Вернуться к герою", callback_data=f"back_{target_id}")]])

    await send_or_edit_screen(call.message, get_levels_text(lvl), kb, photo_id=BANNERS.get("levels"), is_edit=True)

 

 

@dp.callback_query(F.data.startswith("top_"))

async def cb_top(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Открой свой топ командой /top", show_alert=True)

    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Вернуться к герою", callback_data=f"back_{target_id}")]])

    await send_or_edit_screen(call.message, get_top_text(), kb, photo_id=BANNERS.get("top"), is_edit=True)

 

 

@dp.callback_query(F.data.startswith("ref_"))

async def cb_ref(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Открой свою ссылку командой /ref", show_alert=True)

    try:

        bot_info = await bot.get_me()

        b_uname = bot_info.username

    except Exception:

        b_uname = ""

    text, ref_link = get_ref_text(target_id, b_uname)

    share_url = f"https://t.me{quote(ref_link)}"

    kb = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="📤 Отправить ссылку другу", url=share_url)],

        [InlineKeyboardButton(text="⬅️ Вернуться к герою", callback_data=f"back_{target_id}")]

    ])

    await send_or_edit_screen(call.message, text, kb, photo_id="", is_edit=True)

 

 

@dp.callback_query(F.data.startswith("farm_"))

async def cb_farm(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Не трогай чужого персонажа! Напиши /card", show_alert=True)

 

    user = get_user(target_id)

    uid, uname, level, energy, last_farm, amulet_until, _ = user

    now = int(time.time())

    lvl_data = LEVELS.get(level)

    if not lvl_data:

        return await call.answer("Уровень в разработке!", show_alert=True)

 

    if now - last_farm < COOLDOWN:

        rem = (last_farm + COOLDOWN) - now

        msg = random.choice(WAIT_TEXTS).format(h=rem // 3600, m=(rem % 3600) // 60)

        return await call.answer(msg, show_alert=True)

 

    gain = random.randint(50, 150) if amulet_until > now else random.randint(1, 50)

    new_energy = min(energy + gain, lvl_data.get("need"))

    cur.execute("UPDATE users SET energy = ?, last_farm = ?, notified = 0 WHERE user_id = ?", (new_energy, now, uid))

    db.commit()

 

    referrer_id = process_referral_reward(uid)

    if referrer_id:

        try:

            await bot.send_message(referrer_id, f"🎉 <b>Твой ученик @{uname} прошёл первую тренировку!</b>\nТебе начислено <b>+50⚡</b> к текущему герою!", parse_mode="HTML")

        except Exception:

            pass

 

    await call.answer(random.choice(FARM_TEXTS).format(gain=gain), show_alert=True)

    await send_or_edit_card(call.message, get_user(uid), is_edit=True)

@dp.callback_query(F.data.startswith("claim_"))

async def cb_claim(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Это чужой приз!", show_alert=True)

 

    user = get_user(target_id)

    uid, uname, level, energy, _, _, _ = user

    lvl_data = LEVELS.get(level)

    if not lvl_data or energy < lvl_data.get("need"):

        return await call.answer("Сначала докачай энергию до конца!", show_alert=True)

 

    reward_name = lvl_data.get("reward")

    cur.execute("INSERT INTO claims (user_id, username, level, reward) VALUES (?, ?, ?, ?)", (uid, uname, level, reward_name))

    cur.execute("UPDATE users SET level = ?, energy = 0, notified = 1 WHERE user_id = ?", (level + 1, uid))

    db.commit()

 

    await bot.send_message(ADMIN_ID, f"🎉 <b>НОВАЯ ЗАЯВКА НА ПОДАРОК!</b>\nИгрок: @{uname} (ID: <code>{uid}</code>)\nУровень: {level}\nПриз: <b>{reward_name}</b>\n\nУправление: /admin", parse_mode="HTML")

    await call.answer("🎉 Заявка на подарок отправлена админу!", show_alert=True)

    await send_or_edit_card(call.message, get_user(uid), is_edit=True)

 

 

@dp.callback_query(F.data.startswith("shop_"))

async def cb_shop(call: types.CallbackQuery):

    _, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Открой свою лавку командой /shop", show_alert=True)

    await send_or_edit_screen(call.message, get_shop_text(), shop_keyboard(target_id), photo_id=BANNERS.get("shop"), is_edit=True)

 

 

@dp.callback_query(F.data.startswith("buy_"))

async def cb_buy(call: types.CallbackQuery):

    _, item, target_str = call.data.split("_")

    target_id = int(target_str)

    if not check_owner(call, target_id):

        return await call.answer("Это чужое меню!", show_alert=True)

 

    prices_map = {

        "amulet": ("Амулет удачи на 48ч", "Добыча 50-150 энергии без лени героя", 40),

        "case": ("Кейс с удачей", "Случайный бонус от 1 до 100 энергии прямо сейчас", 25),

        "skip": ("Попытка прорыва уровня", "Запрещённая техника мгновенного закрытия уровня", 100),

    }

    title, desc, amount = prices_map.get(item)

    await call.message.answer_invoice(title=title, description=desc, payload=item, currency="XTR", prices=[LabeledPrice(label=title, amount=amount)])

    await call.answer()

 

 

@dp.pre_checkout_query()

async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

 

 

@dp.message(F.successful_payment)

async def process_payment(message: types.Message):

    payload = message.successful_payment.invoice_payload

    paid_stars = message.successful_payment.total_amount

    uid = message.from_user.id

    user = get_user(uid, message.from_user.username)

    _, uname, level, energy, _, amulet_until, _ = user

    now = int(time.time())

 

    cur.execute("UPDATE users SET stars_spent = stars_spent + ? WHERE user_id = ?", (paid_stars, uid))

    cur.execute("INSERT INTO payments (user_id, username, item, amount, created_at) VALUES (?, ?, ?, ?, ?)", (uid, uname, payload, paid_stars, now))

    db.commit()

 

    lvl_data = LEVELS.get(level)

    if not lvl_data:

        return

    need = lvl_data.get("need")

 

    if payload == "amulet":

        new_until = max(amulet_until, now) + (48 * 3600)

        cur.execute("UPDATE users SET amulet_until = ? WHERE user_id = ?", (new_until, uid))

        db.commit()

        await message.answer("🔮 <b>Амулет удачи надет!</b> Ближайшие 48 часов герой пашет на максимум (50–150⚡)!", parse_mode="HTML")

    elif payload == "case":

        bonus = random.randint(1, 100)

        new_energy = min(energy + bonus, need)

        cur.execute("UPDATE users SET energy = ? WHERE user_id = ?", (new_energy, uid))

        db.commit()

        await message.answer(f"📦 <b>Ты вскрыл ящик и вытащил +{bonus}⚡!</b>", parse_mode="HTML")

    elif payload == "skip":

        if random.randint(1, 100) <= 5:

            cur.execute("UPDATE users SET energy = ? WHERE user_id = ?", (need, uid))

            db.commit()

            await message.answer("🔥 <b>БЕЗУМИЕ! Запрещённая техника сработала!</b> Уровень пройден! Забирай подарок в /card!", parse_mode="HTML")

        else:

            await message.answer("💨 <b>ПУФ! Техника пшикнула дымом...</b> Прорыв не удался. Попробуй ещё раз!", parse_mode="HTML")

async def notify_ready_users():

    while True:

        await asyncio.sleep(60)

        now = int(time.time())

        cur.execute("SELECT user_id, level, energy FROM users WHERE notified = 0 AND last_farm > 0 AND last_farm <= ?", (now - COOLDOWN,))

        rows = cur.fetchall()

        for uid, lvl, en in rows:

            cur.execute("UPDATE users SET notified = 1 WHERE user_id = ?", (uid,))

            db.commit()

            lvl_data = LEVELS.get(lvl)

            if not lvl_data or en >= lvl_data.get("need"):

                continue

            try:

                kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎴 Открыть карточку", callback_data=f"back_{uid}")]])

                await bot.send_message(uid, random.choice(NOTIFY_TEXTS), parse_mode="HTML", reply_markup=kb)

                await asyncio.sleep(0.05)

            except Exception:

                pass

 

 

async def auto_backup_db():

    while True:

        await asyncio.sleep(6 * 3600)

        try:

            db.commit()

            snap_path = "auto_backup_full.db"

            snap_conn = sqlite3.connect(snap_path)

            db.backup(snap_conn)

            snap_conn.close()

 

            cur.execute("SELECT COUNT(*), COALESCE(SUM(energy), 0) FROM users")

            u_cnt, sum_en = cur.fetchone()

            cur.execute("SELECT COUNT(*) FROM referrals WHERE rewarded = 1")

            (r_cnt,) = cur.fetchone()

            cur.execute("SELECT COUNT(*) FROM chat_members")

            (m_cnt,) = cur.fetchone()

 

            await bot.send_document(

                chat_id=ADMIN_ID,

                document=FSInputFile(snap_path),

                caption=(

                    f"🔄 <b>Автосохранение полной базы (раз в 6 часов)</b>\n"

                    f"👥 Игроков: <b>{u_cnt}</b> ({sum_en}⚡) | 🤝 Рефов: <b>{r_cnt}</b> | 📊 Чаты: <b>{m_cnt}</b>\n\n"

                    f"<i>Сохранены все таблицы. Для восстановления просто перешлите этот файл боту.</i>"

                ),

                parse_mode="HTML"

            )

        except Exception:

            pass

 

 

async def set_bot_commands():

    commands = [

        BotCommand(command="card", description="🎴 Мой аниме-герой и энергия"),

        BotCommand(command="farm", description="⚡ Отправить героя на тренировку"),

        BotCommand(command="shop", description="🛒 Лавка читера (Бусты за Stars)"),

        BotCommand(command="levels", description="🗺 Дорога славы (Все 56 уровней)"),

        BotCommand(command="top", description="🏆 Топ-10 лучших Сенсеев"),

        BotCommand(command="ref", description="👥 Пригласить друга (+50⚡)"),

        BotCommand(command="promo", description="🎟 Ввести промокод"),

        BotCommand(command="rp", description="🎭 Список РП-команд для чата"),

    ]

    try:

        await bot.set_my_commands(commands)

    except Exception as e:

        logging.warning("set_bot_commands failed: %s", e)

 

 
# --- ПЕРЕВОДЧИК НА ЯЗЫК ЦУНДЕРЕ (100 ФРАЗ + СТИКЕРЫ) ---

TSUNDERE_STICKERS = [

    # Сюда можно вставить file_id стикеров в кавычках через запятую, например:

    # "CAACAgIAAxkBAA...",

]

 

TSUNDERE_PHRASES = [

    # 1–35: Милые и смущённые

    "Б-бака! Я перевёл это не ради тебя, просто мимо проходил: «{text}» 😤💢",

    "Н-не подумай ничего лишнего! Я просто так сказал(а): «{text}» 😳👉👈",

    "Хмф! Если ты не понял(а), повторяю последний раз: «{text}» 😒✨",

    "Я-я вовсе не волнуюсь за тебя, дурак! Но: «{text}» 🥺💢",

    "Т-только не зазнавайся, ладно?! Короче: «{text}» 😳🔥",

    "Ой, всё! Не смотри на меня так, я просто скажу: «{text}» 🙈💢",

    "М-мне абсолютно всё равно, что ты подумаешь! Но: «{text}» 😤💕",

    "Не вздумай улыбаться! Это чистая случайность, что я говорю: «{text}» 😳⚡",

    "П-подумаешь, мелочь какая... В общем: «{text}» 🙄🌸",

    "Я сделал(а) это только потому, что мне было скучно! Слушай: «{text}» 😒💫",

    "Б-бесишь! Почему я вообще должен(на) объяснять тебе: «{text}» 😤💢",

    "Не придумывай себе глупостей, бака! Я имел(а) в виду: «{text}» 😳✨",

    "Хм! Будь благодарен(на), что я вообще снизошёл(ла) до слов: «{text}» 👑😤",

    "Я-я не краснею! Просто в чате жарко! Короче: «{text}» 🥵💢",

    "Т-ты всё равно без меня не справишься, поэтому: «{text}» 🙄💖",

    "Не смей принимать это близко к сердцу, дурачок: «{text}» 😳👉👈",

    "Ч-что?! Я не заикаюсь! Просто запоминай: «{text}» 😤⚡",

    "Л-ладно, так уж и быть, скажу по-хорошему: «{text}» 🥺✨",

    "Не смотри на меня такими глазами! Я сказал(а): «{text}» 🙈🔥",

    "Э-это не забота, ясно?! Просто не хочу лишних проблем: «{text}» 😒💢",

    "Пф, ещё чего! Не радуйся раньше времени, но: «{text}» 😤🌸",

    "Я-я просто случайно нажал(а) отправить! Не читай это: «{text}» 😳💫",

    "Ты такой(ая) беспомощный(ая), что мне пришлось сказать: «{text}» 🙄💕",

    "Н-не подходи слишком близко, когда я говорю: «{text}» 😳💢",

    "Хмф! Можешь считать, что тебе сегодня крупно повезло: «{text}» 😤✨",

    "Я вовсе не ждал(а) твоего ответа! Просто держу в курсе: «{text}» 😒⚡",

    "Д-дурак! Кто вообще так делает?! Ладно, слушай: «{text}» 🥺🔥",

    "Не смей рассказывать об этом остальным в чате! Понятно?! «{text}» 🤫😳",

    "Я-я помог(ла) тебе только из жалости, ясно?! Вот: «{text}» 😤💖",

    "Ой, замолчи уже! Просто прими к сведению: «{text}» 🙄💢",

    "Н-не называй меня милым(ой)! Я сейчас серьёзно говорю: «{text}» 😳🌸",

    "Хм! Если забудешь мои слова — больше не заговорю с тобой: «{text}» 😒✨",

    "Т-ты первый(ая) начал(а), так что не обижайся: «{text}» 😤💫",

    "Я не скучал(а)! Просто в чате было слишком тихо без: «{text}» 🥺⚡",

    "Б-бака! Запомни это раз и навсегда: «{text}» 😳💕",

    # 36–50: Дерзкие и колкие

    "Слышь, чудо в перьях, разуй глаза и читай: «{text}» 😒💢",

    "У тебя вместо мозгов тарелка рамена? Объясняю на пальцах: «{text}» 🤦‍♂️🔥",

    "Хмф, какой(ая) же ты тормоз... Даже Наруто быстрее понял бы: «{text}» 🙄⚡",

    "Не беси меня своей тупостью, бака! Короче: «{text}» 😤💥",

    "Ой, только не ной потом, что тебя не предупреждали: «{text}» 😒🔪",

    "Ты серьёзно сейчас? Боже, с кем я сижу в одном чате... «{text}» 🤦‍♀️💢",

    "Закрой рот и просто молча впитывай мудрость: «{text}» 😤👑",

    "Пф, на твоём месте я бы вообще молчал(а), но ладно: «{text}» 🙄💫",

    "Какой же ты невыносимый(ая) душнила! В общем: «{text}» 😒🔥",

    "Не строй из себя умника, тебе это не идёт! Слушай сюда: «{text}» 😤⚡",

    "Мда, тяжелый случай... Повторяю для особо одарённых: «{text}» 🤦‍♂️💢",

    "Хватит тупить, у меня от тебя уже голова болит! Короче: «{text}» 😣💥",

    "Ты всегда такой(ая) бестолковый(ая) или только по праздникам? «{text}» 🙄🔪",

    "Ой, не смеши мои тапочки! Всем и так ясно, что: «{text}» 😒✨",

    "Ещё одно глупое слово — и получишь сковородкой! Запомни: «{text}» 🍳😤",

    # 51–70: Продолжение дерзких и колких

    "Б-бака! Где ты вообще таких глупостей набрался(лась)?! «{text}» 😤💢",

    "Не лезь со своими советами, без тебя разберёмся! Но: «{text}» 😒⚡",

    "Какой же ты жалкий(ая)... Ладно, так уж и быть, слушай: «{text}» 🙄🔥",

    "У меня аллергия на твою логику! Просто прочитай: «{text}» 🤧💢",

    "Ты что, головой о клавиатуру ударился(лась)?! Я говорю: «{text}» 🤦‍♀️💥",

    "Хмф, вечно от тебя одни проблемы в этом чате: «{text}» 😤💫",

    "Не раздражай меня, пока я в хорошем настроении! Короче: «{text}» 😒🔪",

    "С такими мыслями тебе только в генинах вечно сидеть: «{text}» 🙄⚡",

    "Ой, да кому вообще интересно твоё мнение?! Вот факт: «{text}» 😤👑",

    "Ты даже простую вещь понять не можешь, ну что за наказание: «{text}» 😣💢",

    "Пф, нашёлся(лась) тут герой... Спустись с небес на землю: «{text}» 😒✨",

    "Не выводи меня из себя, иначе пожалеешь! В общем: «{text}» 😤🔥",

    "Похоже, тебе срочно нужен воспитательный подзатыльник: «{text}» 👋💥",

    "Хватит нести чушь, уши вянут! Записывай: «{text}» 🙄💢",

    "Какой(ая) же ты вредный(ая), просто слов нет! Короче: «{text}» 😤⚡",

    "Не делай такое умное лицо, тебе не идёт! Слушай: «{text}» 😒💫",

    "Ты безнадёжен(на), честное слово... Повторяю: «{text}» 🤦‍♂️🔥",

    "Ой, иди уже погуляй, не мешай нормальным людям: «{text}» 🙄🔪",

    "Если ещё раз так сделаешь — запру в гендзюцу навечно! «{text}» 👁😤",

    "Б-бесишь! Почему я вечно должен(на) всё за тебя исправлять: «{text}» 😤💢",

    # 71–100: Пикантные и смущённо-дерзкие аниме-реакции

    "И-извращенец!! Куда ты вообще смотришь, когда читаешь: «{text}» 😳🔞",

    "Х-хентай!! Не смей подходить ко мне с такими мыслями: «{text}» 🙈💢",

    "Н-не пялься на меня так, дурак! Я-я просто сказал(а): «{text}» 😳🔥",

    "Ч-что у тебя вообще на уме, извращенец несчастный?! «{text}» 🥵💢",

    "Убери свои грязные мыслишки подальше, бака!! Я про: «{text}» 😳💥",

    "Н-не шепчи мне такое на ухо, у меня аж мурашки! Короче: «{text}» 🙈⚡",

    "К-какой же ты бесстыжий! При всём чате такое говорить: «{text}» 😳🌸",

    "Т-ты специально меня смущаешь, извращенец?! Я сказал(а): «{text}» 🥵🔥",

    "Не смей раздевать меня взглядом, дурак! Просто слушай: «{text}» 👀💢",

    "О-отойди на два метра! Слишком близко!! В общем: «{text}» 😳💦",

    "Х-хватит так двусмысленно улыбаться, хентай!! «{text}» 🙈💢",

    "Я-я тебе сейчас врежу за такие намёки, извращенец! Но: «{text}» 👊😳",

    "Н-не трогай меня без разрешения, бака!! Я имею в виду: «{text}» 😳⚡",

    "У тебя в голове вообще ничего приличного нет?! Слушай: «{text}» 🥵💥",

    "П-прекрати говорить таким голосом, я не ведусь на это: «{text}» 🙈🌸",

    "К-куда руки тянешь, извращенец?! Сначала дослушай: «{text}» 😳🔥",

    "Н-не смей фантазировать обо мне всякое, дурак!! «{text}» 🥵💢",

    "Т-ты что, совсем стыд потерял(а)?! При людях же: «{text}» 😳💦",

    "М-мне не жарко, просто ты невыносимый извращенец! Короче: «{text}» 🙈⚡",

    "Не смотри на мои губы, когда я говорю: «{text}» 😳💋",

    "Б-бесстыдник! За такие слова в приличном чате бьют: «{text}» 😤🔞",

    "Н-не прижимайся так, бака!! Я просто хотел(а) сказать: «{text}» 😳💥",

    "Х-хентай! У тебя на лице написано, о чём ты сейчас думаешь: «{text}» 🥵🌸",

    "О-отвернись немедленно, пока я не покраснел(а)!! «{text}» 🙈🔥",

    "Т-ты специально такие пошлые намёки кидаешь, дурак?! «{text}» 😳💢",

    "Не смей брать меня за руку так внезапно, извращенец: «{text}» 😳💦",

    "К-какой же ты наглый тип... Ладно, только никому не говори: «{text}» 🤫🥵",

    "П-перестань смущать меня перед всем чатом, бака!! «{text}» 🙈⚡",

    "Я-я не разрешал(а) тебе так близко наклоняться! В общем: «{text}» 😳💋",

    "С-сплошной разврат у тебя в голове, извращенец! Запоминай: «{text}» 😤🔞",

]




@dp.message(F.text.lower().startswith("цундере"))

async def handle_tsundere_translator(message: types.Message):

    raw_text = (message.text or "").strip()

    parts = raw_text.split(maxsplit=1)

 

    target_text = ""

    if len(parts) == 2:

        _, arg_text = parts

        target_text = arg_text.strip()

    elif message.reply_to_message:

        target_text = (message.reply_to_message.text or message.reply_to_message.caption or "").strip()

 

    if not target_text:

        return await message.reply(

            "😤 <b>Б-бака!</b> Напиши <code>цундере [текст]</code> или ответь словом <code>цундере</code> на сообщение друга!",

            parse_mode="HTML"

        )

 

    clean_text = target_text.replace("<", "").replace(">", "").replace("&", "")

    if len(clean_text) > 300:

        clean_text = clean_text[:297] + "..."

 

    if TSUNDERE_STICKERS:

        try:

            await message.answer_sticker(random.choice(TSUNDERE_STICKERS))

        except Exception:

            pass

 

    result = random.choice(TSUNDERE_PHRASES).format(text=clean_text)

    if message.reply_to_message:

        await message.reply_to_message.reply(result, parse_mode="HTML")

    else:

        await message.reply(result, parse_mode="HTML")




EVENING_COMPLIMENTS = [

    "Ты сегодня болтал(а) быстрее, чем Наруто уплетает рамен в Ичираку!",

    "Твоя харизма сегодня ярче, чем Расэнган в ночном небе!",

    "Даже Сатору Годжо снял бы повязку, чтобы почитать твои сообщения!",

    "Ты главный двигатель этого чата — без тебя здесь была бы тишина как в склепе Орочимару!",

    "Твои сообщения сегодня заряжают чат лучше любой чакры Девятихвостого!",

    "Итачи Учиха одобряет твой стиль общения — ни одного лишнего слова, чистый шедевр!",

    "Ты сегодня в ударе, как Сайтама на распродаже в супермаркете!",

    "С такими темпами общения тебе пора выдавать титул Хокаге этой беседы!",

    "Твой юмор и активность сегодня просто 10 из 10 по шкале Ани Форджер!",

    "Даже Какаши отложил свою книжку, чтобы почитать твои перлы в чате!",

    "Твоя энергия сегодня бьёт через край, как у Иноске перед дракой!",

    "Ты настоящий легендарный саннин общения в этой группе!",

    "Без твоих сообщений этот чат потерял бы половину своего вайба!",

    "Твоя клавиатура сегодня дымится сильнее, чем клинок Танджиро!",

    "Ты сегодня сияешь ярче, чем Сусаноо Мадары!",

    "Леви Аккерман поставил бы тебе пятёрку за образцовую активность в беседе!",

    "Твои сообщения сегодня спасают чат от скуки лучше любого аниме-марафона!",

    "Ты абсолютный чемпион по скорости печати — Киллуа на молнии нервно курит в сторонке!",

    "Сегодня весь чат держался на твоей легендарной активности!",

    "Даже Рюк забыл про яблоки, зачитавшись твоими сообщениями!",

    "Твой вклад в жизнь чата сегодня тянет на S-ранг!",

    "С тобой в чате веселее, чем на фестивале в Конохе!",

    "Твоя общительность сегодня на уровне Бога Аниме!",

    "Ты заряжаешь позитивом лучше, чем утренний онигири!",

    "Если бы за сообщения давали пояс чемпиона, он бы уже висел у тебя!",

    "Твой стиль общения настолько крут, что даже Саске бы улыбнулся!",

    "Сегодня ты абсолютный MVP нашей беседы — заслуженный респект!",

    "Твоя активность сегодня пробила небеса, как бур Симона!",

    "Ты главный генератор контента и хорошего настроения в этом чате!",

    "Весь чат аплодирует стоя твоей сегодняшней активности!",

]

 

 

async def evening_chat_summary():

    from datetime import timezone, timedelta

    msk = timezone(timedelta(hours=3))

    last_sent_date = ""

 

    while True:

        await asyncio.sleep(30)

        now_msk = datetime.now(msk)

        today_str = now_msk.strftime("%Y-%m-%d")

 

        if now_msk.hour == 22 and now_msk.minute == 0 and last_sent_date != today_str:

            last_sent_date = today_str

            cur.execute("SELECT DISTINCT chat_id FROM chat_members WHERE msg_today > 0")

            active_chats = cur.fetchall()

 

            for (cid,) in active_chats:

                cur.execute("SELECT SUM(msg_today) FROM chat_members WHERE chat_id = ?", (cid,))

                (total_today,) = cur.fetchone()

 

                cur.execute("""

                    SELECT user_id, user_name, msg_today

                    FROM chat_members

                    WHERE chat_id = ? AND msg_today > 0

                    ORDER BY msg_today DESC LIMIT 3

                """, (cid,))

                top_three = cur.fetchall()

                if not top_three:

                    continue

 

                first_winner, *_ = top_three

                winner_id, winner_name, winner_msgs = first_winner

 

                w_user = get_user(winner_id, winner_name)

                _, _, w_lvl, w_energy, _, _, _ = w_user

                lvl_data = LEVELS.get(w_lvl)

                if lvl_data:

                    new_en = min(w_energy + 15, lvl_data.get("need"))

                    cur.execute("UPDATE users SET energy = ? WHERE user_id = ?", (new_en, winner_id))

 

                compliment = random.choice(EVENING_COMPLIMENTS)

                summary_text = (

                    f"🌙 <b>ВЕЧЕРНИЕ ИТОГИ ДНЯ В ЧАТЕ!</b>\n\n"

                    f"💬 За сегодня мы написали: <b>{total_today} сообщ.</b>\n\n"

                    f"👑 <b>Главный активист дня:</b> <b>{winner_name}</b> ({winner_msgs} сообщ.)\n"

                    f"✨ <i>{compliment}</i>\n"

                    f"🎁 <b>Награда победителю:</b> начислено <b>+15⚡</b> к твоему аниме-герою!\n\n"

                    f"🔥 <b>Тройка лидеров сегодня:</b>\n"

                )

                medals = {1: "🥇", 2: "🥈", 3: "🥉"}

                for idx, (_, uname, msgs) in enumerate(top_three, start=1):

                    summary_text += f"{medals.get(idx)} <b>{uname}</b> — {msgs} сообщ.\n"

 

                try:

                    await bot.send_message(cid, summary_text, parse_mode="HTML")

                    await asyncio.sleep(0.1)

                except Exception:

                    pass

 

            cur.execute("UPDATE chat_members SET msg_today = 0")

            db.commit()



from chat_extra import setup_chat_extra

setup_chat_extra(dp, bot, cur, db, ADMIN_ID, LEVELS, get_user, active_emoji_quiz)



async def main():
    
    await set_bot_commands()

    try:

        await bot.delete_webhook(drop_pending_updates=True)

    except Exception as e:

        logging.warning("delete_webhook failed: %s", e)

    asyncio.create_task(notify_ready_users())

    asyncio.create_task(auto_backup_db())

    asyncio.create_task(auto_emoji_quiz_loop())

    asyncio.create_task(evening_chat_summary())

    await dp.start_polling(bot)

 

 

if __name__ == "__main__":

    asyncio.run(main())
