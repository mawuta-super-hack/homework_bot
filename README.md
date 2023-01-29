# Бот-ассистент 

***Бот-ассистент предназначен для проверки статуса домашних работ студентов Яндекс.Практикум. Бот делает запрос к API Яндекс.Практикум и высылает сообщение со статусом домашней работы.***


### Возможности бота:
- делает запрос к API.
- определяет корректность ответа.
- определяет статус домашней работы.
- отправляет сообщение со статусом домашней работы в чат пользователя.


### Технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)


### Пример наполнения .env-файла:

```
PRACTICUM_TOKEN = 'token'
TELEGRAM_TOKEN = 'some_token'
TELEGRAM_CHAT_ID = 'chat_id'
```

### Получение токенов:
Получить токен Практикум.Домашка можно по [ссылке.](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a)

Получить токен телеграм-бота можно в диалоге с ботом @BotFather: нажмите кнопку Start («Запустить»). Затем отправьте команду "/newbot" и укажите параметры нового бота. @BotFather отправит в чат токен для работы с Bot API. <br>


Получить ID чата можно путем отправки боту @userinfobot сообщения от любого пользователя telegram. В ответ бот направит сообщение с данными о пользователе. 
### Описание команд для запуска приложения локально:

Клонирование репозитория и переход в него в командной строке:

```
git clone https://git@github.com:mawuta-super-hack/homework_bot.git
```

```
cd ./homework_bot
```


Установка и активация виртуального окружения:

```
python -m venv env
```

```
source venv/Scripts/activate
```


Установка зависимостей из файла requirements.txt:
```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск файла "homework.py":
```
python homework.py
```

### Автор проекта:
Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>