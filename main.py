import asyncio
import logging
import sys

import structlog

# Python 3.14 убрал автосоздание event loop — создаём вручную
if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.new_event_loop())
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import settings
from handlers.track import start, help_command, handle_message

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Запуск бота")

    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен, polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
