import logging

from telegram import Update
from telegram.ext import ContextTypes

from services.yandex_music import get_track_info, InvalidUrlError, TrackNotFoundError

logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "👋 Привет! Я помогу узнать информацию о треке из Яндекс.Музыки.\n\n"
    "Просто отправь мне ссылку на трек, например:\n"
    "https://music.yandex.ru/album/12360955/track/178495"
)

HELP_TEXT = (
    "Отправь мне ссылку на трек из Яндекс.Музыки.\n\n"
    "Поддерживаемый формат:\n"
    "https://music.yandex.ru/album/<id>/track/<id>\n\n"
    "UTM-метки в ссылке не помеха — отрежу автоматически."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает входящее сообщение — ожидает ссылку на трек."""
    text = update.message.text.strip()
    user = update.effective_user
    logger.info("Сообщение от пользователя id=%s: %s", user.id, text)

    # Проверяем что сообщение похоже на ссылку
    if "music.yandex.ru" not in text:
        await update.message.reply_text(
            "Это не похоже на ссылку Яндекс.Музыки.\n"
            "Отправь ссылку вида:\n"
            "https://music.yandex.ru/album/<id>/track/<id>"
        )
        return

    # Показываем что бот обрабатывает запрос
    await update.message.chat.send_action("typing")

    try:
        track = await get_track_info(text)
    except InvalidUrlError:
        await update.message.reply_text(
            "Не могу распознать ссылку. Убедись что это ссылка именно на трек, а не на альбом или артиста."
        )
        return
    except TrackNotFoundError:
        await update.message.reply_text(
            "Не удалось получить информацию о треке. Попробуй позже."
        )
        return

    year_str = f" ({track.year})" if track.year else ""
    response = (
        f"🎵 {track.title}\n"
        f"👤 {track.artists}\n"
        f"⏱ {track.duration}\n"
        f"💿 {track.album}{year_str}"
    )
    await update.message.reply_text(response)
