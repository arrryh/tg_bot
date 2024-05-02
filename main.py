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

    key = 'section_'

    def __init__(self, id: int, name: str, text: str = ''):
        self.id = id
        self.name = name
        self.text = text

    def get_inline_button(self):
        return InlineKeyboardButton(self.name, callback_data=self.key + str(self.id))


class Course:
    id: int
    name: str
    sections: list

    key = 'course_'

    def __init__(self, id: int, name: str, sections = list):
        self.id = id
        self.name = name
        self.sections = sections

    def get_inline_button(self):
        return InlineKeyboardButton(self.name, callback_data=self.key + str(self.id))


COURSES = [
    Course(1, 'Python', [Section(1, 'Урок 1'), Section(2, 'Урок 2'), Section(3, 'Урок 3'), ]),
    Course(2, 'SQL', [Section(1, 'Урок 1'), Section(2, 'Урок 2'), Section(3, 'Урок 3'), ]),
    Course(3, 'PHP', [Section(1, 'Урок 1'), Section(2, 'Урок 2'), Section(3, 'Урок 3'), ]),
    Course(4, 'Telegram', [Section(1, 'Урок 1'), Section(2, 'Урок 2'), Section(3, 'Урок 3'), ]),
    Course(5, 'HTML', [Section(1, 'Урок 1'), Section(2, 'Урок 2'), Section(3, 'Урок 3'), ]),
]

def get_course_by_course_key(course_key):
    id = int(course_key.replace(Course.key, ''))

    for c in COURSES:
        if c.id == id:
            return c
    
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""

    courses = grouped([c.get_inline_button() for c in COURSES],3)

    keyboard = courses

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите курс:", reply_markup=reply_markup)

    return START_ROUTES


async def course_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    course = get_course_by_course_key(query.data)

    section_keyboard = grouped([s.get_inline_button() for s in course.sections],3)
    #print(
    #    'course', 
    #    course.id, 
    #    course.name
    #)

    await query.answer()
    keyboard = section_keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Курс по: {course.name} \n {course.text}', reply_markup=reply_markup
    )
    return START_ROUTES

async def section_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show new choice of buttons"""

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = '7171139361:AAGA0v_6YNJqIvFCrBOU53dKyPGLLEZ2gTo'

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(course_detail, pattern="^" + Course.key),
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