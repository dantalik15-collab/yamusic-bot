import re
import logging
from dataclasses import dataclass

from yandex_music import ClientAsync
from yandex_music.exceptions import YandexMusicError

logger = logging.getLogger(__name__)

TRACK_URL_PATTERN = re.compile(r"music\.yandex\.ru/album/(\d+)/track/(\d+)")


@dataclass
class TrackInfo:
    title: str
    artists: str
    duration: str
    album: str
    year: int | None


class TrackNotFoundError(Exception):
    pass


class InvalidUrlError(Exception):
    pass


def parse_track_url(url: str) -> tuple[int, int]:
    """Извлекает album_id и track_id из ссылки Яндекс.Музыки.

    Args:
        url: Ссылка вида https://music.yandex.ru/album/{album_id}/track/{track_id}

    Returns:
        Кортеж (album_id, track_id)

    Raises:
        InvalidUrlError: Если ссылка не соответствует ожидаемому формату
    """
    match = TRACK_URL_PATTERN.search(url)
    if not match:
        raise InvalidUrlError(f"Не удалось распарсить ссылку: {url}")
    return int(match.group(1)), int(match.group(2))


def _format_duration(ms: int) -> str:
    """Форматирует длительность из миллисекунд в MM:SS."""
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


async def get_track_info(url: str) -> TrackInfo:
    """Получает информацию о треке по ссылке Яндекс.Музыки.

    Args:
        url: Ссылка на трек

    Returns:
        TrackInfo с названием, артистом, длительностью, альбомом и годом

    Raises:
        InvalidUrlError: Если ссылка невалидна
        TrackNotFoundError: Если трек не найден
    """
    album_id, track_id = parse_track_url(url)
    logger.debug("Запрашиваем трек track_id=%s album_id=%s", track_id, album_id)

    try:
        from config import settings
        client = await ClientAsync(token=settings.yandex_music_token).init()
        tracks = await client.tracks([f"{track_id}:{album_id}"])
    except YandexMusicError as e:
        logger.error("Ошибка Яндекс.Музыки при запросе трека %s:%s — %s", track_id, album_id, e)
        raise TrackNotFoundError("Не удалось получить данные трека") from e

    if not tracks:
        raise TrackNotFoundError(f"Трек {track_id} не найден")

    t = tracks[0]
    logger.info("Трек получен: %s — %s", t.title, ", ".join(a.name for a in (t.artists or [])))

    return TrackInfo(
        title=t.title or "Неизвестно",
        artists=", ".join(a.name for a in (t.artists or [])) or "Неизвестно",
        duration=_format_duration(t.duration_ms) if t.duration_ms else "—",
        album=t.albums[0].title if t.albums else "Неизвестно",
        year=t.albums[0].year if t.albums else None,
    )