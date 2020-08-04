# Start the bot
# Create the Updater and pass it your bot's token.
import sys

import click
from loguru import logger
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

COMPONENT_NAME = "feedback-bot"


@click.command()
@click.option("--dev", is_flag=True, help="Запустить бот в режиме разработчика.")
def main(dev: bool):
    """
    Запустить бота - сборщика обратной связи.

    Перед запуском надо установить переменные окружения: TG_BOT_TOKEN, TG_CHAT_ID, COMMAND_REPLIES_PATH
    """
    from feedback_bot.bot import (
        error,
        forward_callback,
        help_callback,
        reply_callback,
        start_callback,
    )
    from feedback_bot.log import DevelopFormatter, JsonSink
    from feedback_bot.config import PROXY, TG_TOKEN

    logger.remove()
    if dev:
        develop_fmt = DevelopFormatter(COMPONENT_NAME)
        logger.add(sys.stdout, format=develop_fmt)
    else:
        json_sink = JsonSink(COMPONENT_NAME)
        logger.add(json_sink)

    if PROXY is not None:
        updater = Updater(TG_TOKEN, use_context=True, request_kwargs={"proxy_url": PROXY})
    else:
        updater = Updater(TG_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_callback))
    dp.add_handler(CommandHandler("help", help_callback))

    # Messages handler
    dp.add_handler(MessageHandler(Filters.reply, reply_callback))
    dp.add_handler(MessageHandler(Filters.all, forward_callback))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    logger.info("Bot started.")
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
