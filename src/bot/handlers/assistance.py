from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.contacts import Contacts
from bot.constants.messages import ASK_YOUR_QUESTION, ASSISTANCE_MESSAGE
from bot.constants.states.main_states import States
from bot.keyboards.assistance import (
    assistance_questions_keyboard_contact,
    region_keyboard_markup,
)


async def receive_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для выбор региона оказания помощи."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ASSISTANCE_MESSAGE, reply_markup=region_keyboard_markup
    )
    return States.REGION


async def contact_with_us_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для связи с нами."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=Contacts[context.user_data[States.REGION]].value,
        reply_markup=assistance_questions_keyboard_contact,
    )
    return States.SELECTED_TYPE


async def ask_question_assistance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> States:
    """Обработчик для задания вопроcа."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=ASK_YOUR_QUESTION)
    return States.ASK_QUESTION
