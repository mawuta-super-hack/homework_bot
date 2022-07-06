import logging
import os
import sys
import time
from http import HTTPStatus
from json import JSONDecodeError

import requests
import telegram
from dotenv import load_dotenv

import settings

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s',
    encoding='UTF-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s'
)
handler.setFormatter(formatter)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_message(bot, message):
    """Функция отвечает за отправку сообщений."""
    try:
        logging.debug('Попытка отправить сообщение в телеграм.')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        if 'Изменился статус' in message:
            logging.info('Сообщение отправлено!')
    except Exception as e:
        msg = f'Не удалось отправить сообщение в телеграм, ошибка {e}'
        raise telegram.error.TelegramError(msg)
    return True


def get_api_answer(current_timestamp):
    """Функция делает запрос к api."""
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    try:
        get_answer = requests.get(
            settings.ENDPOINT,
            params=params,
            headers=headers)
    except Exception as e:
        msg = f'Не удалось сделать запрос к API, ошибка {e}'
        raise requests.HTTPError(msg)
    code = get_answer.status_code
    if code != HTTPStatus.OK:
        msg = f'Запрос не выполнен, получен код {code}'
        raise ValueError(msg)
    else:
        try:
            response = get_answer.json()
        except Exception as e:
            raise JSONDecodeError(f'В ответе нет допустимого json, {e}')
    return response


def check_response(response):
    """Функция определяет корректность ответа."""
    homeworks = response['homeworks']
    if type(homeworks) is not list:
        logging.error('Получен не список}')
        raise TypeError('Получен не список')
    homework = homeworks
    return homework


def parse_status(homework):
    """Функция определяет статус домашней работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    for status, result in settings.HOMEWORK_STATUSES.items():
        try:
            if homework_status == status:
                verdict = result
                break
        except Exception as e:
            raise KeyError(f'Неизветный статус домашней работы. {e}')
    message = f'Изменился статус проверки работы "{homework_name}". {verdict}'
    return message


def check_tokens():
    """Функция определяет наличие переменных окружения."""
    var = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    check = True
    for i in var:
        if i is None:
            check = False
            logging.critical('Доступны не все переменные окружения')
    return check


def main():
    """Основная логика работы бота."""
    new_error = []
    old_error = []
    current_timestamp = int(time.time())
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    check = check_tokens()
    if check is False:
        raise NameError('Доступны не все переменные окружения')
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks != []:
                homework = homeworks[0]
                message = parse_status(homework)
                send_message(bot, message)
            else:
                logging.debug('Статус домашки не изменился')
            current_timestamp = int(time.time())
            time.sleep(settings.RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            new_error.append(message)
            if new_error != old_error:
                send_message(bot, message)
                logging.info('Cообщение об ошибке отправлено!')
                old_error = new_error.copy()
                new_error.clear()
            else:
                old_error = new_error.copy()
                new_error.clear()
            time.sleep(settings.RETRY_TIME)


if __name__ == '__main__':
    main()
