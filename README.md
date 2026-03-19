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

## Деплой на VPS через WinSCP + systemd

### 1. Загрузка файлов

Открой WinSCP, подключись к VPS по SFTP.
Загрузи папку `bot/` на сервер, например в `/home/user/bot/`.

### 2. Установка Python и зависимостей

```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv -y
cd /home/user/bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Создание .env на сервере

```bash
cp .env.example .env
nano .env  # вставь реальный токен
```

### 4. Создание systemd сервиса

```bash
sudo nano /etc/systemd/system/yamusic-bot.service
```

Содержимое файла:

```ini
[Unit]
Description=Yandex Music Telegram Bot
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/bot
ExecStart=/home/user/bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 5. Запуск сервиса

```bash
sudo systemctl daemon-reload
sudo systemctl enable yamusic-bot
sudo systemctl start yamusic-bot
```

### 6. Проверка статуса

```bash
sudo systemctl status yamusic-bot
# Логи:
sudo journalctl -u yamusic-bot -f
```
