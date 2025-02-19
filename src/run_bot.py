import logging.config

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ConversationHandler,
)

from bot.constants.patterns import HELP_TYPE_PATTERN
from bot.constants.regions import Regions
from bot.constants.states.main_states import PATTERN, States
from bot.core.config import settings
from bot.core.log_config import LOGGING_CONFIG
from bot.handlers.ask_question import ask_question_handler
from bot.handlers.assistance import (
    ask_question_assistance,
    contact_with_us_assistance,
    receive_assistance,
)
from bot.handlers.assistance_types import (
    fund_programs,
    select_type_of_help,
    selected_type_assistance,
)
from bot.handlers.back_handler import back_button
from bot.handlers.main_handlers import help_handler, start_handler
from bot.handlers.service_handlers import (
    answer_all_messages_handler,
    menu_handler,
)


def main():
    """Application launch point."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bot")
    logger.info("start")

    main_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            States.ASSISTANCE: [
                CallbackQueryHandler(
                    receive_assistance,
                    pattern=PATTERN.format(state=States.ASSISTANCE.value),
                ),
            ],
            States.REGION: [
                CallbackQueryHandler(
                    select_type_of_help,
                    pattern=PATTERN.format(state=region.name),
                )
                for region in Regions
            ],
            States.ASSISTANCE_TYPE: [
                CallbackQueryHandler(
                    selected_type_assistance,
                    pattern=HELP_TYPE_PATTERN,
                ),
                CallbackQueryHandler(
                    fund_programs,
                    pattern=PATTERN.format(state=States.FUND_PROGRAMS.value),
                ),
                CallbackQueryHandler(
                    contact_with_us_assistance,
                    pattern=PATTERN.format(state=States.CONTACT_US.value),
                ),
            ],
            States.SELECTED_TYPE: [
                CallbackQueryHandler(
                    ask_question_assistance,
                    pattern=PATTERN.format(state=States.ASK_QUESTION.value),
                )
            ],
            States.ASK_QUESTION: [ask_question_handler],
        },
        fallbacks=[
            CallbackQueryHandler(
                back_button,
                pattern=r"back_to_",
            ),
            start_handler,
        ],
    )
    app = (
        ApplicationBuilder()
        .token(settings.telegram_token.get_secret_value())
        .build()
    )
    app.add_handlers(
        [main_handler, help_handler, menu_handler, answer_all_messages_handler]
    )
    app.run_polling()


if __name__ == "__main__":
    main()
