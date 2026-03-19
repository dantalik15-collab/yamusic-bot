# Telegram-бот Яндекс.Музыка

Бот принимает ссылку на трек в Яндекс.Музыке и возвращает информацию о нём.

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env
# Вставь токен бота в .env
python main.py
```

## Запуск тестов

```bash
pytest
```

## Примечание о геоблокировке

Яндекс.Музыка блокирует запросы с зарубежных IP-адресов (код 451).
Бот работает только при запуске на территории России.

## Запуск на Windows

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Создание .env

Скопируй `.env.example` в `.env` и заполни токены:

```
TELEGRAM_BOT_TOKEN=токен_от_BotFather
YANDEX_MUSIC_TOKEN=токен_яндекс_музыки
```

Как получить токен Яндекс.Музыки: https://github.com/MarshalX/yandex-music-api/discussions/513

### 3. Запуск

```bash
python main.py
```

Бот будет работать пока открыт терминал.
