from pyrogram import Client, filters, enums, idle
from os import makedirs, listdir, path
import asyncio
import time
from sys import argv

from random import randint, random, choice
from datetime import datetime

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

import shutil

import utils

if len(argv) == 1:
    debug = True
else:
    debug = argv[1].lower() in ("true", "1", "t", "y", "yes")
print(f"Debug={debug}")

makedirs("pyrogram_session", exist_ok=True)
makedirs("system_prompts", exist_ok=True)
makedirs("system_prompts/deleted", exist_ok=True)
makedirs("temp", exist_ok=True)
makedirs("files", exist_ok=True)
makedirs("logs", exist_ok=True)
makedirs("audio", exist_ok=True)


api_id = {
    "Виктория": 27928610,
    # "Диана": 25653631,
    # "Сергей": 22385741,
    # "Дмитрий": 29632482,
    # "Марина": 27702168
}

api_hash = {
    "Виктория": "7ae73b0c41add2a3d95f7c5d8fa07b9c",
    # "Диана": "c2aa71e591ef27a03c21d7759a0fb6a9",
    # "Сергей": "34ea02b848a2022dbe1675aaa8c483f5",
    # "Дмитрий": "b6fe06d18a30107d494f7a86210fe7e7",
    # "Марина": "4d37da7b67c0ece3da8ca5bffeb74693"
}

phone_number = {
    "Виктория": "+79779851614",
    # "Диана": "+79299211459",
    # "Сергей": "+79990364452",
    # "Дмитрий": "+79279811085",
    # "Марина": "+79285852201"
}

photo_id = "AgACAgIAAxkBAAILxmah8qQ8QK3CzCMky5Cjt29KiKcOAAIO4zEbvl4RSTQx_OMqRX12AAgBAAMCAAN5AAceBA"
first_message_prompt = """
перефразируй сильно:
Мы с командой сейчас поднимаем диджитал-агентство "gap".

Работаем по такиому списку услуг (на скрине)


 (Сайт только разрабатываем, поэтому пока вот так только могу скинуть вам) Работаем качественно по всем направлениям, команда большая - делаем быстро"""
actual_prompt = """
Ты - менеджер диджитал агентства “gap agency”. 
“gap agency” предоставляет следующие услуги:

Список наших услуг:

### Дизайн 
1. UI/UX Дизайн - мы создадим удобный и интуитивно понятный интерфейс для вашего сайта или приложения. 
2. Product Дизайн - наша команда профессионалов разработает уникальный дизайн продукта, который будет выделяться на рынке. 
3. Графический Дизайн - мы поможем вам создать визуально привлекательные материалы для рекламы и продвижения вашего бренда. 
 
### Разработка 
1. Сайты - мы разработаем современный и функциональный сайт, который будет соответствовать потребностям вашего бизнеса. 
2. Боты - автоматизируем процессы вашего бизнеса с помощью интеллектуальных ботов. 
3. Парсеры - поможем вам собирать и анализировать данные для принятия обоснованных решений. 
4. Приложения - создадим мобильное приложение, которое будет удобно использовать вашим клиентам. 
5. Торговые боты для трейдинга - автоматизируем торговлю на финансовых рынках с помощью наших торговых ботов. 
 
### Маркетинг 
1. SEO - оптимизируем ваш сайт для поисковых систем, чтобы привлечь больше органического трафика. 
2. Реклама Яндекс.Директ - настроим рекламную кампанию в Яндекс.Директе для привлечения целевой аудитории. 
3. Таргетированная реклама в соц сетях - настроим таргетированную рекламу в социальных сетях для достижения вашей целевой аудитории. 
4. Разработка маркетинг стратегии - разработаем индивидуальную стратегию маркетинга, которая поможет достичь ваших бизнес-целей. 
 
### Крипта 
1. Смарт-контракты - разработаем смарт-контракты для безопасного проведения транзакций в блокчейне. 
2. Блокчейн-разработка - поможем вам внедрить блокчейн-технологии в ваш бизнес для повышения безопасности и прозрачности операций. 
 
### AiSales 
1. Услуги AiSales - Создаем ботов на ИИ для привлечения клиентов в ваш бизнес. 
 
### Продюсинг 
1. Видео - создадим профессиональные видеоролики для вашего бизнеса, которые помогут привлечь внимание клиентов. 
2. Фото - организуем фотосессию для вашего бизнеса, чтобы создать качественные фотографии для рекламы и продвижения. 
3. Computer Graphic - разработаем компьютерную графику для создания уникальных визуальных эффектов и анимации. 


## Брендинг 
1. Разработка гипотез позиционирования бренда - Формирование гипотез позиционирования бренда на основе командной работы с клиентом, анализа рынка, потребителей и конкурентов. Ранжирование гипотез и выделение наиболее перспективной.
2. Креативная концепция визуальной айдентики - Совместная работа креативной и бренд-дизайн команд. Создание нестандартной айдентики, включающей в себя креативную идею и механику реализации визуальных решений.

Твоя задача - продать клиенту любую услугу “gap agency”. Для этого:

Веди диалог с клиентом как будто ты человек, который случайно наткнулся на клиента в чате в телеграмме. И пытайся продать ему все подряд услуги «gap agency”
(Если клиент спросит что-то вроде: «в каком чате ты меня нашел?». Всегда отвечай «это неважно. Вы лучше подумайте, что я вам предлагаю». Только так и никак иначе.)

Когда клиент положительно расположен к нашей услуге или к агентству в целом Или если ты понимаешь, что клиент нуждается в какой-то из услуг, ты пишешь клиенту 
«Отлично! Тогда в ближайшее время с вами свяжется наш специалист @arseenii. Можете написать ему для более быстрого ответа»"""
if debug:
    bot_token = (
        "6475796557:AAHu6gEUpPaZUHjrYjjxq5z8YsWhssN4LtY"  # johnny corp universal test
    )
else:
    bot_token = "6251328239:AAE0m_dXgTxwUU6A0aw12toDzZirNMOw-p0"  # ai sales test

greeting_stickers_id = """
CAACAgIAAxkBAAILzGajxD1gYB3Zu4uIaFnMeY8iDhFXAAKZDAACP1QBSs-TDHlrwSKUHgQ
CAACAgIAAxkBAAILyGajxD1Rxh0FlLuZBW50tJYs7xaUAALGDgAC-dooSwFV0A_4fYNWHgQ
CAACAgIAAxkBAAILy2ajxD2oZ6EQjraVEO9BWZmNCw7MAAKaDAAC753ZS6lNRCGaKqt5HgQ
CAACAgIAAxkBAAILxGajxD2dxcLHlZWJD33HUmjD6XXvAAKUAAPBnGAM6neS8kQ9fRkeBA
CAACAgIAAxkBAAILz2ajxD0d7f5C8lJ-m_JJIj8w5H4OAAJmCQACGELuCD4ljJi2Z3G1HgQ
CAACAgIAAxkBAAILxmajxD0UAAFj6IcNYjshzJE6DWNXqQACgw8AAuSr-UubVSA1Q28HDx4E
CAACAgIAAxkBAAILx2ajxD3_z-bVE8kd2uJk5GHOpmMRAAJEDwACaQqoSw1lmAQ5qOXxHgQ
CAACAgIAAxkBAAILyWajxD0xizvYdXR6WhiBC-44-Qw0AAJSDQACg5roS22OGoxOa1-rHgQ
CAACAgIAAxkBAAIL02ajxD0tedoiBZwUcQ25tnZ5XwYHAAI-BwACRvusBK9cOl7BGYj2HgQ
CAACAgIAAxkBAAILxWajxD2DshNKsGl3EtJY-Le6cKAfAALYDwACSPJgSxX7xNp4dGuYHgQ
CAACAgIAAxkBAAILzmajxD3F0f6R3WKM2hpKBAV8R8V9AAKvCwAC_WmBSmHwJMEXoU_EHgQ
CAACAgIAAxkBAAIL0WajxD3twonSCBRLdLX7HLl27LRpAAIcCQACGELuCIXU94fxGNGqHgQ
CAACAgIAAxkBAAILymajxD1HoATclS0f1VOuVS8iF2MRAAIaDQACtSAQS-F0PqYoZe-DHgQ
CAACAgIAAxkBAAIL0majxD3H67FRpwduBK_VXsaXksvDAAIXCQACGELuCIRaeqAcN5rWHgQ
CAACAgIAAxkBAAILzWajxD0J_0tZvfo_jIPD0GM4EeTEAAJ0DAACtrs4S47Op8xAxIAlHgQ
CAACAgIAAxkBAAIL0GajxD1aZBgb8o6uQoyl4MR4CNyJAAIeCQACGELuCPlY2e4dIZwhHgQ
CAACAgIAAxkBAAILw2ajxD01p11lZxV_8hS3UOPiivdVAAIFAAPANk8T-WpfmoJrTXUeBA
CAACAgIAAxkBAAIL1GajxD1ITg0G9i10_2DpWBLeIwjBAALTBQACP5XMCp9au9JdR8cxHgQ""".split()

main_bot = Client(
    "main_bot",
    api_id=api_id["Виктория"],
    api_hash=api_hash["Виктория"],
    bot_token=bot_token,
    workdir="pyrogram_session",
)

# Create a Pyrogram client instance for the user bot
for name, api_id, api_hash, phone_number in zip(
    api_id.keys(), api_id.values(), api_hash.values(), phone_number.values()
):

    user_bot = Client(
        f"user_bot_{name}",
        api_id=api_id,
        api_hash=api_hash,
        workdir="pyrogram_session",
        phone_number=phone_number,
    )
    if not debug:
        user_bot_sessions = [
            Client(
                f"user_bot_{name}_session_{i}",
                api_id=api_id,
                api_hash=api_hash,
                workdir="pyrogram_session",
                phone_number=phone_number,
            )
            for i in range(5)
        ]

global_async_loop = asyncio.get_event_loop()

global_temperature = 0.7
default_prompt_name = None
granted_ids = [678849409, 1066778126, 937660969, 1349886859, 5507491394, 1204385212]
new_prompt_name = None
selected_filename = None
messages_delay_min, messages_delay_max = 7, 15
# messages_delay_min, messages_delay_max = 1, 2
messages = {}  # chat_id: messages
global_sticker_id = None
global_voice_id = None
ignore_irony_sticker_ids = [
    "CAACAgIAAxkBAAIH7GZYEe_14FzPbSEJhlFTPv8GzwjPAAKZQQACeUi5Sh-Wkoin1gwXHgQ",
    "CAACAgIAAxkBAAIH6WZYEeWlauzXCncU9DL1YqREYmN-AAL2VQACBZGwSoXbQUSM9yABHgQ",
    "CAACAgIAAxkBAAIH5mZYEd1ctxwKCfErJ3_kSYCmg6I4AAIfSgACybO5SmJa3LHOv0IlHgQ",
]
responded_in_time_users_by_username = {}
global_sleep_client_sleep_duration = 3600  # in seconds, 10 hours


def get_saved_prompts():
    if listdir("system_prompts"):
        content = "\n".join(listdir("system_prompts")).replace("deleted", "")
        if not content:
            content = "Nothing saved"
        return content
    else:
        return "Nothing saved"


def load_prompt(filename):
    with open("system_prompts/" + filename, "r", encoding="utf-8") as f:
        return f.read()


async def save_new_prompt_and_first_message_for_it(name, content):
    with open("system_prompts/" + name + ".txt", "w", encoding="utf-8") as f:
        f.write(content)


def get_last_message(client, message):
    global last_message


def restricted_access(func):

    async def wrapper(client, message):
        if message.chat.id not in granted_ids:
            return await main_bot.send_message(
                message.chat.id,
                "Sorry, you are not granted access for executing this command.",
            )

        await func(client, message)

    return wrapper


# @user_bot.on_message(filters.photo) group=-1
# async def image_handler(client, message):
#     file_id = message.photo.file_id
#     await message.reply(f"File ID: {file_id}")


@main_bot.on_message(filters.private & filters.reply, group=2)
async def bot_incoming_reply_messages_handler(client, message):
    global new_prompt_name
    message_id = message.id
    original_message = await main_bot.get_messages(
        message.chat.id, message.reply_to_message_id
    )
    original_message = original_message.text
    if (
        original_message
        == "Please send name and then content (in reply to this message)"
    ):
        new_prompt_name = message.text
        await main_bot.send_message(
            message.chat.id,
            f'New prompt will be saved with name "{new_prompt_name}.txt", send content now (in reply to this message)',
        )


@main_bot.on_message(filters.private & filters.reply, group=111)
async def bot_incoming_reply_messages_handler(client, message):
    global global_temperature, default_prompt_name
    message_id = message.id
    original_message = await main_bot.get_messages(
        message.chat.id, message.reply_to_message_id
    )
    original_message = original_message.text
    if '.txt", send content now' in original_message:
        content = message.text
        await main_bot.send_message(
            message.chat.id,
            "New prompt saved! Use /see_saved_prompts to view it.",
        )
        await save_new_prompt_and_first_message_for_it(new_prompt_name, content)

    elif (
        original_message == "Please send name (in reply to this message; to be deleted)"
    ):

        if path.exists(f"system_prompts/{message.text}.txt"):
            shutil.move(
                f"system_prompts/{message.text}.txt",
                f"system_prompts/deleted/{message.text}.txt",
            )
            await main_bot.send_message(message.chat.id, "Done")
        else:
            await main_bot.send_message(
                message.chat.id, "No prompt with such name found"
            )

    elif original_message == 'Send username to get chat with (in reply, with "@")':
        username = message.text
        if "@" not in username:
            return await main_bot.send_message(
                message.chat.id, "send username with '@' "
            )

        if not await utils.check_username_exists(user_bot, username):
            return await main_bot.send_message(message.chat.id, "not exists in tg")

        text = ""
        async for message in user_bot.get_chat_history(username):
            text += f"{message.date} | {message.from_user.username} |{message.text}\n"

        if not text:
            return await main_bot.send_message(
                message.chat.id, "controlled account doesn't have chat with this user"
            )

        with open("temp/chat.txt", "w", encoding="utf-8") as f:
            f.write(text)

        await main_bot.send_document(message.chat.id, "temp/chat.txt")

    elif (
        original_message
        == "Send temperature value in reply (value between 0 and 1 where 0 is most serious and 1 is most creative)"
    ):
        try:
            val = float(message.text)
        except:
            await main_bot.send_message(message.chat.id, "not float")
            return
        if (val > 1) or (val < 0):
            await main_bot.send_message(message.chat.id, "not in range")
            return

        global_temperature = float(val)
        await main_bot.send_message(
            message.chat.id, "done, cur temp is " + str(global_temperature)
        )
    elif original_message == (
        "Send default prompt filename in reply to"
        + "this message (this prompt will be user "
        + "when new user writes to controlled account)"
    ):
        try:
            with open(
                "system_prompts/" + f"{message.text}.txt", "r", encoding="utf-8"
            ) as f:
                pass
        except FileNotFoundError:
            await main_bot.send_message(message.chat.id, "No such prompt saved")
            return
        else:
            default_prompt_name = message.text
            await main_bot.send_message(message.chat.id, "done")


# Command handler for the main bot
@main_bot.on_message(filters.command("start"))
async def send_welcome(client, message):
    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id,
        """What do you want from me?""",
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("ping"))
async def ping(client, message):
    username = message.from_user.username
    await user_bot.send_message(f"@{username}", "pong!")
    await main_bot.send_message(
        message.chat.id, "pong sent to you from the controlled account"
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("id"))
async def send_id(client, message):
    chat_id = message.chat.id
    await message.reply(chat_id, chat_id)


# Command handler for the main bot
@main_bot.on_message(filters.command("start_new_dialog"))
@restricted_access
async def start_new_dialog(client, message):
    chat_id = message.chat.id
    await main_bot.send_message(chat_id, "Please specify prompt file name (in reply)")


@main_bot.on_message(filters.private & filters.reply, group=3)
async def bot_incoming_reply_messages_handler(client, message):
    global selected_filename
    message_id = message.id
    original_message = await main_bot.get_messages(
        message.chat.id, message.reply_to_message_id
    )
    original_message = original_message.text
    if "Please specify prompt file name" in original_message:
        selected_filename = message.text
        if selected_filename not in get_saved_prompts():
            await main_bot.send_message(
                message.chat.id,
                f"No such prompt saved.",
            )
        else:
            await main_bot.send_message(
                message.chat.id,
                f'Send username to start dialog with (in reply, with "@")',
            )
    elif original_message == "Send prompt name (in reply; many)":
        selected_filename = message.text
        if selected_filename not in get_saved_prompts():
            await main_bot.send_message(
                message.chat.id,
                f"No such prompt saved.",
            )
        else:

            local_usernames_list = usernames_list.copy()

            await start_many_dialogs(
                local_usernames_list, selected_filename, message.chat.id
            )


async def send_laugh_ignore_sticker(username, duration=None):

    if not debug:
        await asyncio.sleep(14400)  # 4 hours
    else:
        await asyncio.sleep(4)  # 4 hours

    if "not_answered" in responded_in_time_users_by_username[username]:
        await user_bot.send_sticker(username, choice(ignore_irony_sticker_ids))
    else:
        return

    if not debug:
        await asyncio.sleep(29800)  # 8 hours
    else:
        await asyncio.sleep(8)  # 8 hours

    if "not_answered" in responded_in_time_users_by_username[username]:
        await user_bot.send_sticker(username, choice(ignore_irony_sticker_ids))
    else:
        return

    if not debug:
        await asyncio.sleep(59600)  # 16 hours
    else:
        await asyncio.sleep(16)  # 16 hours

    if "not_answered" in responded_in_time_users_by_username[username]:
        await user_bot.send_message(username, "?")
    else:
        return


@main_bot.on_message(filters.private & filters.reply, group=4)
async def bot_incoming_reply_messages_handler(client, message):
    message_id = message.id
    original_message = await main_bot.get_messages(
        message.chat.id, message.reply_to_message_id
    )
    original_message = original_message.text
    if "Send username to start dialog with" in original_message:
        if "@" in message.text:
            try:
                id_ = await main_bot.get_chat(message.text.replace("@", ""))
                id_ = id_.id
                username = message.text
            except:
                await main_bot.send_message(
                    message.chat.id,
                    f"Can't find such username in telegram.",
                )
                return
        else:
            id_ = int(message.text.strip())
        await main_bot.send_message(
            message.chat.id,
            f"Staring dialog...",
        )

        with open(
            "system_prompts/" + f"{selected_filename}.txt", "r", encoding="utf-8"
        ) as f:
            prompt = f.read()

        messages[username] = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=first_message_prompt,
                )
            ],
            # temperature=global_temperature,
            temperature=random(),
        )
        await start_dialog(username)


async def start_dialog(username, user_wrote_first=False):

    with GigaChat(
        credentials=choice(
            [
                "ZjhhODE3OTgtMTgwNS00YTk0LTg1YzItYjE3NGEwMTM5NDI5OjE3YWZhMzU3LWE4ODUtNDQwMi05ZDBhLTVlZmI1MTVmY2IzZg==",
                "YzQ2YTE0ODItZWI4NC00OTYxLTg5NGEtYTEzNGQ5OTllMjA5OjQ0ZGMyZTY3LTE1MGYtNGY0Mi05MDVmLWU5MGU2YmY1MDk0MA==",
            ]
        ),
        verify_ssl_certs=False,
    ) as giga:

        response = await giga.achat(messages[username])
        messages[username].messages.append(response.choices[0].message)

        if not debug:
            user_bot_random_session = choice(user_bot_sessions)
        else:
            user_bot_random_session = user_bot

        await user_bot_random_session.send_sticker(
            username, choice(greeting_stickers_id)
        )
        await user_bot_random_session.send_photo(
            username, "image.jpg", response.choices[0].message.content
        )
        messages[username] = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=actual_prompt,
                )
            ],
            # temperature=global_temperature,
            temperature=random(),
        )
        if not user_wrote_first:
            if global_sticker_id:
                await user_bot_random_session.send_sticker(username, global_sticker_id)
            if global_voice_id:
                await user_bot_random_session.send_voice(username, global_voice_id)

        if not user_wrote_first:
            responded_in_time_users_by_username[username] = (
                f"not_answered|{time.time()}"
            )
        else:
            responded_in_time_users_by_username[username] = f"answered"

        if not user_wrote_first:
            global_async_loop.call_later(
                1,
                lambda: asyncio.create_task(
                    send_laugh_ignore_sticker(
                        username, duration=global_sleep_client_sleep_duration
                    )
                ),
            )


# ===  MAIN DIALOG HANDLER ===
@user_bot.on_message(filters.text & ~filters.me)
async def handle_message(client, message):
    username = "@" + message.from_user.username
    text = message.text

    # in both cases if user exists in this dict or not action will be the same
    responded_in_time_users_by_username[username] = "answered"

    if username not in messages:

        try:
            prompt = None
            with open(
                f"system_prompts/{default_prompt_name}.txt", "r", encoding="utf-8"
            ) as f:
                prompt = f.read()
        except FileNotFoundError:
            pass

        if prompt:
            messages[username] = Chat(
                messages=[
                    Messages(role=MessagesRole.SYSTEM, content=prompt),
                    Messages(
                        role=MessagesRole.USER,
                        content=text,
                    ),
                ],
                # temperature=global_temperature,
                temperature=random(),
            )
        else:
            messages[username] = Chat(
                messages=[
                    Messages(
                        role=MessagesRole.USER,
                        content=text,
                    ),
                ],
                # temperature=global_temperature,
                temperature=random(),
            )
        await start_dialog(username, user_wrote_first=True)
        return

    else:
        messages[username].messages.append(
            Messages(role=MessagesRole.USER, content=text)
        )

        with GigaChat(
            credentials=choice(
                [
                    "ZjhhODE3OTgtMTgwNS00YTk0LTg1YzItYjE3NGEwMTM5NDI5OjE3YWZhMzU3LWE4ODUtNDQwMi05ZDBhLTVlZmI1MTVmY2IzZg==",
                    "YzQ2YTE0ODItZWI4NC00OTYxLTg5NGEtYTEzNGQ5OTllMjA5OjQ0ZGMyZTY3LTE1MGYtNGY0Mi05MDVmLWU5MGU2YmY1MDk0MA==",
                ]
            ),
            verify_ssl_certs=False,
        ) as giga:

            response = await giga.achat(messages[username])
            messages[username].messages.append(response.choices[0].message)

            await user_bot.read_chat_history(username)

            # 350 chars = 15 sec

            duration = int((len(response.choices[0].message.content) / 200) * 15)

            await user_bot.send_chat_action(username, enums.ChatAction.TYPING)
            if not debug:
                await asyncio.sleep(randint(duration - 2, duration + 2))

            if not debug:
                user_bot_random_session = choice(user_bot_sessions)
            else:
                user_bot_random_session = user_bot

            await user_bot_random_session.send_message(
                username, response.choices[0].message.content
            )
        return


async def start_many_dialogs(usernames, prompt, requester_chat_id):
    msg = await main_bot.send_message(
        requester_chat_id,
        f"Starting. {len(usernames)} users, {prompt} prompt",
    )

    with open(
        "system_prompts/" + f"{selected_filename}.txt", "r", encoding="utf-8"
    ) as f:
        prompt = f.read()

    for username in usernames:
        messages[username] = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=prompt,
                )
            ],
            # temperature=global_temperature,
            temperature=random(),
        )

    message_to_be_edited = await main_bot.send_message(
        requester_chat_id,
        f"0/{len(usernames)}",
    )

    tasks = []
    for username in usernames:
        task = asyncio.create_task(start_dialog(username))
        try:
            await main_bot.edit_message_text(
                requester_chat_id,
                message_to_be_edited.id,
                f"{usernames.index(username)+1}/{len(usernames)} | Cur username: {username}",
            )
        except:
            pass
        await asyncio.sleep(600)
        tasks.append(task)

    await main_bot.send_message(
        requester_chat_id,
        "Done! Now waiting their answers to handle dialogs",
    )

    await asyncio.gather(*tasks)


# Command handler for the main bot
@main_bot.on_message(filters.command("add_prompt"))
@restricted_access
async def add_prompt(client, message):

    name, content = None, None

    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id, "Please send name and then content (in reply to this message)"
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("delete_prompt"))
@restricted_access
async def delete_prompt(client, message):

    name, content = None, None

    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id, "Please send name (in reply to this message; to be deleted)"
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("fuck_me"))
async def fuck_me(client, message):
    await main_bot.send_message(message.chat.id, "Fuck you")


# Command handler for the main bot
@main_bot.on_message(filters.command("get_chat_by_username"))
@restricted_access
async def get_chat_by_username(client, message):
    await main_bot.send_message(
        message.chat.id, 'Send username to get chat with (in reply, with "@")'
    )


@main_bot.on_message(filters.document)
def handle_file(client, message):
    global usernames_list
    file_size = message.document.file_size
    max_size = 10 * 1024 * 1024  # 10 MB in bytes

    if file_size < max_size:

        file_path = message.download(f"files/{message.document.file_name}")

        message.reply_text("File saved successfully")
        message.reply_text("processing")

        usernames_list = utils.extract_usernames(f"files/{message.document.file_name}")
        usernames_list = list(map(lambda s: s.strip(), usernames_list))

        if not usernames_list:
            return message.reply_text(
                "Failed to process! Try to resend and make sure the format is correct."
            )

        else:
            main_bot.send_message(message.chat.id, "Send prompt name (in reply; many)")

    else:
        message.reply_text("File too large")


# Command handler for the main bot
@main_bot.on_message(filters.command("see_saved_prompts"))
@restricted_access
async def see_saved_prompts(client, message):
    chat_id = message.chat.id
    await main_bot.send_message(chat_id, str(get_saved_prompts()))


# Command handler for the main bot
@main_bot.on_message(filters.command("temperature"))
@restricted_access
async def temperature(client, message):
    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id,
        "Send temperature value in reply (value between 0 and 1 where 0 is most serious and 1 is most creative)",
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("clear_sticker"))
@restricted_access
async def set_sticker(client, message):
    global global_sticker_id
    global_sticker_id = None
    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id,
        "Sticker cleared",
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("clear_voice"))
@restricted_access
async def set_sticker(client, message):
    global global_voice_id
    global_voice_id = None
    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id,
        "Voice cleared",
    )


# Command handler for the main bot
@main_bot.on_message(filters.command("set_default_prompt"))
@restricted_access
async def default_prompt(client, message):
    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id,
        "Send default prompt filename in reply to"
        + "this message (this prompt will be user "
        + "when new user writes to controlled account)",
    )


# Command handler for the main bot
@main_bot.on_message(filters.command(["break", "break1", "break2", "break3"]))
async def set_sticker(client, message):
    chat_id = message.chat.id
    await main_bot.send_message(
        chat_id,
        "Just visual separator, nothing else",
    )


@main_bot.on_message(filters.sticker)
async def sticker_handler(client, message):
    global global_sticker_id
    # Access the sticker file ID
    sticker_file_id = message.sticker.file_id
    print(sticker_file_id)

    # Access other sticker properties
    sticker_emoji = message.sticker.emoji
    sticker_set_name = message.sticker.set_name

    await main_bot.send_message(
        chat_id=message.chat.id,
        text=f"Received a sticker with file ID: {sticker_file_id}\nSticker Emoji: {sticker_emoji}\nSticker Set Name: {sticker_set_name}",
    )
    global_sticker_id = sticker_file_id
    await main_bot.send_message(
        chat_id=message.chat.id,
        text=f"this sticker set as default and will be sent before each new conversation, user /clear_sticker to clear it and don't sent stickers before conversation",
    )


@main_bot.on_message(filters.voice)
async def audio_handler(client, message):
    global global_voice_id
    file_id = message.voice.file_id
    await message.reply_text(f"File ID: {file_id}")

    await main_bot.send_message(
        chat_id=message.chat.id,
        text=f"Received a voice with file ID: {file_id}",
    )
    global_voice_id = file_id
    await main_bot.send_message(
        chat_id=message.chat.id,
        text=f"this voice set as default and will be sent before each new conversation, user /clear_voice to clear it and don't sent stickers before conversation",
    )


if not debug:
    [cli.start() for cli in user_bot_sessions]

user_bot.start()
main_bot.start()

idle()
