
#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging
import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
STAGE_ONE, STAGE_TWO, STAGE_THREE, STAGE_FOUR = range(4)

def grouped(array, num=3):
    array1 = [array[i:i+num] for i in range(0, len(array), num)]
    return array1

class Section:
    id: int
    name: str
    text: str

    key = 'selection_'

    def __init__(self, id: int, name ; str, text: str):
        self.id = id
        self.name = name
        self.text = text

class Course:
    id: int
    name: str
    key = 'course_'

    def __init__(self, id: int, name ; str):
        self.id = id
        self.name = name

    def get_inline_button(self):
        return  InlineKeyboardButton(self.name, callback_data=str(STAGE_ONE))

COURSES = [
    Course(1, 'Python'),
    Course(2, 'SQL'),
    Course(3, 'PHP'),
    Course(4, 'Telegram'),
    Course(6, 'HTML'),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""

    courses = grouped([c.get_inline_button() for c in COURSES],3)

    keyboard = courses

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите курс:", reply_markup=reply_markup)

    return START_ROUTES


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    folder = ''

    if query.data == '1':
        folder = 'cats'
    elif query.data == '2':
        folder = 'dogs'
    else:
        folder = 'cats'

    image_name = random_file(f'images/{folder}')
    image_path = f'images/{folder}/{image_name}'

    await query.message.reply_photo(
        photo=open(image_path, 'rb')
    )

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    course = get_course_by_course_key(guery.data)

print()

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(STAGE_THREE)),
            InlineKeyboardButton("4", callback_data=str(STAGE_FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = '7171139361:AAGA0v_6YNJqIvFCrBOU53dKyPGLLEZ2gTo'

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(STAGE_ONE) + "$"),
                # CallbackQueryHandler(two, pattern="^" + str(STAGE_TWO) + "$"),
                # CallbackQueryHandler(three, pattern="^" + str(STAGE_THREE) + "$"),
                # CallbackQueryHandler(four, pattern="^" + str(STAGE_FOUR) + "$"),
            ],
            # END_ROUTES: [
                # CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                # CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            # ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()