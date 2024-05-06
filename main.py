#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

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
    return [array[i:i+num] for i in range(0, len(array), num)]


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
    text: str

    key = 'course_'

    def __init__(self, id: int, name: str, sections: list, text:str=''):
        self.id = id
        self.name = name
        self.sections = sections
        self.text = text

    def get_inline_button(self):
        return InlineKeyboardButton(self.name, callback_data=self.key + str(self.id))


COURSES = [
    Course(1, 'Python', [Section(1, 'Урок 1', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.'), 
                         Section(2, 'Урок 2', ''), 
                         Section(3, 'Урок 3', '')], 
                         'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'),
    Course(2, 'SQL', [Section(1, 'Урок 1'), 
                      Section(2, 'Урок 2'), 
                      Section(3, 'Урок 3'), ], 
                      'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'),
    Course(3, 'PHP', [Section(1, 'Урок 1'), 
                      Section(2, 'Урок 2'), 
                      Section(3, 'Урок 3'), ], 
                      'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'),
    Course(4, 'Telegram', [Section(1, 'Урок 1'), 
                           Section(2, 'Урок 2'), 
                           Section(3, 'Урок 3'), ], 
                           'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'),
    Course(5, 'HTML', [Section(1, 'Урок 1'), 
                       Section(2, 'Урок 2'), 
                       Section(3, 'Урок 3'), ], 
                       'Excepteur sint occaecat cupidatat non proident.'),
]

def get_course_by_course_key(course_key):
    id = int(course_key.replace(Course.key, ''))

    for c in COURSES:
        if c.id == id:
            return c
    
    return None

def get_section_by_key(section_key):
    id = int(section_key.replace(Section.key, ''))

    for s in Course.sections:
        if s.id == id:
            return s
    
    return None

#s.get_inline_button() for s in course.sections
#section = course.get_section_by_key(query.data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""

    courses = grouped([c.get_inline_button() for c in COURSES],3)

    keyboard = courses

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите курс:", reply_markup=reply_markup)

    return START_ROUTES


async def course_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    course = get_course_by_course_key(query.data)

    section_keyboard = grouped([s.get_inline_button() for s in course.sections],3)

    await query.answer()
    keyboard = section_keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Курс по: {course.name} \n {course.text} \n Выберите урок:', reply_markup=reply_markup
    )
    return START_ROUTES

async def section_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    section = get_section_by_key(query.data)

    await query.answer()
    keyboard = section
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f'Информация по: {Section.name} \n {Section.text}', reply_markup=reply_markup
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
                CallbackQueryHandler(course_detail, pattern="^" + Course.key),
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