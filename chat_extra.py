import sqlite3

import time

from datetime import datetime

from aiogram import Bot, Dispatcher, F, types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

 

INFO_URL = "https://telegra.ph/Oznakomlenie-11-20"  # <-- Вставьте сюда вашу ссылку со статьёй из Telegraph

 

PERSONAL_DOSSIER_QUOTES = [

    "Хмф, ну подумаешь, зашёл в профиль… Не зазнавайся, до Хокаге тебе ещё далеко, бака!",

    "Я-я не собирал на тебя досье специально! Просто само в базу записалось, дурак!",

    "Пф, цифры как цифры… Но если уйдёшь из чата, я, может быть, чуть-чуть соскучусь!",

    "Б-бака! Не пялься так гордо на свою статистику, тренируйся давай!",

    "Н-ну, для такого неуклюжего шиноби показатели вполне терпимые… но не расслабляйся!",

    "Ой, всё! Не смотри на меня так, будто ждёшь похвалы за эти цифры!",

    "Я запомнил(а) тебя с первого сообщения… но не думай, что ты особенный(ая), дурак!",

    "Хм! Будь благодарен(на), что я вообще веду учёт твоих похождений в этой беседе!",

    "Т-ты всё равно без моих подсказок пропадёшь, так что держись поближе к чату!",

    "Не вздумай улыбаться! Это чистая случайность, что у тебя такое неплохое досье!",

    "М-мне абсолютно всё равно, на каком ты месте в рейтинге! Понятно?!",

    "С такими темпами, может, когда-нибудь и станешь нормальным сенсеем… наверное!",

    "Б-бесишь! Почему я вечно должен(на) следить за твоей статистикой?!",

    "Хмф! Можешь считать, что тебе повезло попасть в этот чат, бака!",

    "Я вовсе не ждал(а), когда ты проверишь свой профиль! Просто держу в курсе!",

]

 

DOSSIER_CMDS = {"профиль", "кто я", "кто ты", "статус"}

VIEW_RULES_CMDS = {"правила", "/rules"}

DEL_RULES_CMDS = {"-правила", "удалить правила"}

INFO_CMDS = {"информация", "инфо", "гайд", "помощь", "/help"}

 

 

def ensure_extra_tables(c):

    c.execute("""

    CREATE TABLE IF NOT EXISTS chat_rules (

        chat_id INTEGER PRIMARY KEY,

        rules_text TEXT,

        updated_by TEXT,

        updated_at INTEGER

    )

    """)

    for col_sql in [

        "ALTER TABLE chat_members ADD COLUMN quiz_wins INTEGER DEFAULT 0",

        "ALTER TABLE chat_members ADD COLUMN first_seen_ts INTEGER DEFAULT 0",

    ]:

        try:

            c.execute(col_sql)

        except sqlite3.OperationalError:

            pass

 

 

def setup_chat_extra(dp: Dispatcher, bot: Bot, cur, db, admin_id: int, levels: dict, get_user_fn, active_quiz_dict: dict = None):

    if active_quiz_dict is None:

        active_quiz_dict = {}

 

    async def is_boss_user(chat_id: int, user_id: int) -> bool:

        if user_id == admin_id:

            return True

        try:

            member = await bot.get_chat_member(chat_id, user_id)

            return member.status in ("creator", "administrator")

        except Exception:

            return False

 

    async def handle_set_rules(message: types.Message, raw_text: str):

        cid = message.chat.id

        uid = message.from_user.id

 

        if not await is_boss_user(cid, uid):

            return await message.reply("⛔ <b>Устанавливать правила могут только создатель и админы чата!</b>", parse_mode="HTML")

 

        if not raw_text:

            return await message.reply(

                "📜 <b>Как создать правила чата:</b>\n"

                "Напиши <code>+правила</code>, нажми <b>Enter</b> и распиши пункты с новой строки:\n\n"

                "<code>+правила\n1. Не спамить\n2. Уважать участников</code>",

                parse_mode="HTML"

            )

 

        safe_rules = raw_text.replace("<", "").replace(">", "")

        author_name = (message.from_user.full_name or message.from_user.username or "Админ").replace("<", "").replace(">", "")

        now = int(time.time())

 

        with sqlite3.connect("game_v2.db") as conn:

            conn.execute("PRAGMA busy_timeout=5000;")

            c = conn.cursor()

            ensure_extra_tables(c)

            c.execute(

                "INSERT OR REPLACE INTO chat_rules (chat_id, rules_text, updated_by, updated_at) VALUES (?, ?, ?, ?)",

                (cid, safe_rules, author_name, now)

            )

            conn.commit()

 

        await message.reply(

            "✅ <b>Правила беседы успешно сохранены!</b>\n"

            "Теперь любой участник может открыть их словом <code>правила</code>.",

            parse_mode="HTML"

        )

 

    async def handle_del_rules(message: types.Message):

        cid = message.chat.id

        uid = message.from_user.id

 

        if not await is_boss_user(cid, uid):

            return await message.reply("⛔ <b>Удалять правила могут только создатель и админы чата!</b>", parse_mode="HTML")

 

        with sqlite3.connect("game_v2.db") as conn:

            conn.execute("PRAGMA busy_timeout=5000;")

            c = conn.cursor()

            ensure_extra_tables(c)

            c.execute("DELETE FROM chat_rules WHERE chat_id = ?", (cid,))

            conn.commit()

 

        await message.reply("🗑 <b>Правила этого чата удалены!</b>", parse_mode="HTML")

 

    async def handle_show_rules(message: types.Message):

        cid = message.chat.id

        with sqlite3.connect("game_v2.db") as conn:

            conn.execute("PRAGMA busy_timeout=5000;")

            c = conn.cursor()

            ensure_extra_tables(c)

            c.execute("SELECT rules_text, updated_by, updated_at FROM chat_rules WHERE chat_id = ?", (cid,))

            row = c.fetchone()

 

        if not row or not row[0]:

            return await message.reply(

                "📜 <b>В этом чате ещё не установлены правила!</b>\n"

                "<i>Админы могут задать их командой <code>+правила [текст]</code>.</i>",

                parse_mode="HTML"

            )

 

        rules_text, author, upd_ts = row

        date_str = datetime.fromtimestamp(upd_ts).strftime("%d.%m.%Y")

        kb = InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text="😤 Ознакомлен(а), бака!", callback_data="chat_rules_ack")]

        ])

 

        msg_text = (

            f"📜 <b>ПРАВИЛА ЭТОЙ БЕСЕДЫ</b>\n"

            f"━━━━━━━━━━━━━━\n"

            f"{rules_text}\n"

            f"━━━━━━━━━━━━━━\n"

            f"✍️ <i>Обновил(а): {author} ({date_str})</i>"

        )

        await message.reply(msg_text, reply_markup=kb, parse_mode="HTML")

 

    async def handle_show_info(message: types.Message):

        kb = InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text="📖 Открыть полную инструкцию", url=INFO_URL)]

        ])

        info_text = (

            "📚 <b>ОБЩАЯ ИНФОРМАЦИЯ И ГАЙД ПО БОТУ</b>\n"

            "━━━━━━━━━━━━━━\n"

            "∙ 🎮 Суть игры и прокачка героев\n"

            "∙ 😤 Все РП-команды и реплики\n"

            "∙ 🎴 Досье шиноби и статистика чата\n"

            "∙ 🧠 Правила аниме-викторины\n"

            "∙ 🛡 Админ-команды для бесед\n"

            "━━━━━━━━━━━━━━\n"

            "😤 <i>«Хмф! Специально для тебя всё расписал(а) на одной странице — нажимай и читай, бака!»</i>"

        )

        await message.reply(info_text, reply_markup=kb, parse_mode="HTML")

 

    @dp.callback_query(F.data == "chat_rules_ack")

    async def cb_rules_ack(callback: types.CallbackQuery):

        await callback.answer("Хмф! Смотри не нарушай их, бака, а то получишь по шее!", show_alert=True)

 

    async def check_quiz_answer_safe(event: types.Message):

        cid = event.chat.id

        if cid not in active_quiz_dict or not event.text or not event.from_user or event.from_user.is_bot:

            return False

 

        guess = (

            event.text.strip().lower()

            .replace(",", "").replace(".", "").replace("!", "")

            .replace(":", "").replace("-", " ").replace("ё", "е")

        )

        guess = " ".join(guess.split())

        quiz = active_quiz_dict.get(cid)

        if not quiz:

            return False

 

        clean_answers = [

            " ".join(a.lower().replace("-", " ").replace("ё", "е").split())

            for a in quiz.get("answers", [])

        ]

        if guess not in clean_answers:

            return False

 

        title = quiz.get("title")

        active_quiz_dict.pop(cid, None)

 

        with sqlite3.connect("game_v2.db") as conn:

            conn.execute("PRAGMA busy_timeout=5000;")

            c = conn.cursor()

            ensure_extra_tables(c)

            c.execute(

                "UPDATE chat_members SET quiz_wins = quiz_wins + 1 WHERE chat_id = ? AND user_id = ?",

                (cid, event.from_user.id)

            )

            conn.commit()

 

        uname = (event.from_user.full_name or event.from_user.username or "Шиноби").replace("<", "").replace(">", "")

        await event.reply(

            f"🎉 <b>ЕСТЬ ПРАВИЛЬНЫЙ ОТВЕТ!</b>\n\n"

            f"🏆 Самый быстрый знаток аниме: <a href=\"tg://user?id={event.from_user.id}\"><b>{uname}</b></a>\n"

            f"🎬 Загаданный тайтл: <b>{title}</b>\n\n"

            f"<i>Напиши <code>викторина</code> для нового раунда!</i>",

            parse_mode="HTML",

            disable_web_page_preview=True

        )

        return True

 

    async def send_user_dossier(message: types.Message):

        target = message.reply_to_message.from_user if (message.reply_to_message and message.reply_to_message.from_user) else message.from_user

        if target.is_bot:

            return await message.reply("😤 Я — великий Цундере-бот этой беседы! Нечего в моё досье заглядывать!")

 

        cid = message.chat.id

        uid = target.id

        uname = (target.full_name or target.username or "Шиноби").replace("<", "").replace(">", "")

        now = int(time.time())

 

        try:

            member = await bot.get_chat_member(cid, uid)

            if uid == admin_id:

                role_str = "👑 Создатель"

            elif member.status == "creator":

                role_str = "👑 Создатель"

            elif member.status == "administrator":

                role_str = "🛡 Админ"

            else:

                role_str = "Участник"

        except Exception:

            role_str = "Участник"

 

        with sqlite3.connect("game_v2.db") as conn:

            conn.execute("PRAGMA busy_timeout=5000;")

            c = conn.cursor()

            ensure_extra_tables(c)

 

            c.execute(

                "SELECT msg_total, msg_today, quiz_wins, first_seen_ts FROM chat_members WHERE chat_id = ? AND user_id = ?",

                (cid, uid)

            )

            cm_row = c.fetchone()

            if cm_row:

                msg_total, msg_today, quiz_wins, first_ts = cm_row

            else:

                msg_total, msg_today, quiz_wins, first_ts = 0, 0, 0, now

 

            if not first_ts or first_ts <= 0:

                c.execute("UPDATE chat_members SET first_seen_ts = ? WHERE chat_id = ? AND user_id = ?", (now, cid, uid))

                conn.commit()

                first_ts = now

 

            c.execute("SELECT COUNT(*) + 1 FROM chat_members WHERE chat_id = ? AND msg_total > ?", (cid, msg_total))

            (chat_rank,) = c.fetchone()

 

            g_user = get_user_fn(uid, target.username)

            _, _, g_lvl, g_energy, _, _, _ = g_user

            lvl_data = levels.get(g_lvl)

            if lvl_data:

                hero_short = lvl_data.get("name").split(" (").pop(0)

                hero_line = f"{hero_short} (Ур. {g_lvl} ∙ <code>{g_energy}/{lvl_data.get('need')}⚡</code>)"

            else:

                hero_line = f"Бог Аниме (Ур. {g_lvl})"

 

            c.execute("SELECT COUNT(*) + 1 FROM users WHERE level > ? OR (level = ? AND energy > ?)", (g_lvl, g_lvl, g_energy))

            (global_rank,) = c.fetchone()

 

        first_date_str = datetime.fromtimestamp(first_ts).strftime("%d.%m.%Y")

        days_in_chat = max(1, (now - first_ts) // 86400)

        quote_line = PERSONAL_DOSSIER_QUOTES[uid % len(PERSONAL_DOSSIER_QUOTES)]

 

        dossier_text = (

            f"🎴 <b>ДОСЬЕ ШИНОБИ</b>\n"

            f"━━━━━━━━━━━━━━\n"

            f"👤 <a href=\"tg://user?id={uid}\"><b>{uname}</b></a> ∙ <i>{role_str}</i>\n"

            f"🦸 <b>Герой:</b> {hero_line}\n"

            f"🏆 <b>Топ:</b> #{chat_rank} в чате | #{global_rank} в боте\n"

            f"💬 <b>Чат:</b> {msg_total} сообщ. <i>(+{msg_today} сегодня)</i>\n"

            f"🧠 <b>Викторина:</b> {quiz_wins} побед\n"

            f"📅 <b>В чате с:</b> {first_date_str} <i>({days_in_chat} дн.)</i>\n"

            f"━━━━━━━━━━━━━━\n"

            f"😤 <i>«{quote_line}»</i>"

        )

        await message.reply(dossier_text, parse_mode="HTML", disable_web_page_preview=True)

 

    @dp.message.outer_middleware()

    async def chat_extra_middleware(handler, event: types.Message, data: dict):

        if event.chat and event.chat.type in ("group", "supergroup") and event.text:

            full_text = event.text.strip()

            lower_text = full_text.lower()

 

            if lower_text in DOSSIER_CMDS:

                await send_user_dossier(event)

                return

 

            if lower_text in VIEW_RULES_CMDS or lower_text.startswith("/rules@"):

                await handle_show_rules(event)

                return

 

            if lower_text in INFO_CMDS or lower_text.startswith("/help@"):

                await handle_show_info(event)

                return

 

            if lower_text in DEL_RULES_CMDS:

                await handle_del_rules(event)

                return

 

            for prefix in ("+правила", "новые правила", "/setrules"):

                if lower_text == prefix or lower_text.startswith(prefix + " ") or lower_text.startswith(prefix + "\n"):

                    rules_body = full_text[len(prefix):].strip()

                    await handle_set_rules(event, rules_body)

                    return

 

            if await check_quiz_answer_safe(event):

                return

 

        return await handler(event, data)
