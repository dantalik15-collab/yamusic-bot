import pytest

from services.yandex_music import parse_track_url, _format_duration, InvalidUrlError


class TestParseTrackUrl:
    def test_parse_standard_url(self):
        # Arrange
        url = "https://music.yandex.ru/album/9378276/track/60618611"

        # Act
        album_id, track_id = parse_track_url(url)

        # Assert
        assert album_id == 9378276
        assert track_id == 60618611

    def test_parse_url_with_utm_params(self):
        # Arrange
        url = "https://music.yandex.ru/album/9378276/track/60618611?utm_source=web&utm_medium=copy_link"

        # Act
        album_id, track_id = parse_track_url(url)

        # Assert
        assert album_id == 9378276
        assert track_id == 60618611

    def test_raises_on_album_url(self):
        # Arrange — ссылка на альбом, без track_id
        url = "https://music.yandex.ru/album/9378276"

        # Act & Assert
        with pytest.raises(InvalidUrlError):
            parse_track_url(url)

    def test_raises_on_artist_url(self):
        # Arrange
        url = "https://music.yandex.ru/artist/3426942"

        # Act & Assert
        with pytest.raises(InvalidUrlError):
            parse_track_url(url)

    def test_raises_on_random_text(self):
        # Arrange
        url = "просто текст без ссылки"

        # Act & Assert
        with pytest.raises(InvalidUrlError):
            parse_track_url(url)

    @pytest.mark.parametrize("url", [
        "https://music.yandex.ru/album/111/track/222",
        "http://music.yandex.ru/album/111/track/222",
        "music.yandex.ru/album/111/track/222",
    ])
    def test_parse_various_url_formats(self, url: str):
        # Act
        album_id, track_id = parse_track_url(url)

        # Assert
        assert album_id == 111
        assert track_id == 222


class TestFormatDuration:
    @pytest.mark.parametrize("ms,expected", [
        (228000, "3:48"),
        (60000,  "1:00"),
        (3661000, "61:01"),
        (0, "0:00"),
        (999, "0:00"),  # меньше секунды
    ])
    def test_format_duration(self, ms: int, expected: str):
        assert _format_duration(ms) == expected
