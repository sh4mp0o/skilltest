import requests
from config import TOKEN, ADMIN_ID

URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    params = {'offset': offset, 'timeout': 100}
    response = requests.get(URL + "getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    requests.get(URL + "sendMessage", params=params)

def handle_updates(updates):
    for update in updates['result']:
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')

            if chat_id == ADMIN_ID:  # Проверяем, если это админ
                if text.startswith("/reply"):
                    _, user_id, *reply_text = text.split(maxsplit=2)
                    reply_text = ' '.join(reply_text)
                    send_message(user_id, reply_text)
            else:
                # Пересылаем сообщение пользователю-администратору
                forward_text = f"Сообщение от {chat_id}:\n{text}"
                send_message(ADMIN_ID, forward_text)
                # Подтверждаем пользователю отправку сообщения
                send_message(chat_id, "Ваше сообщение отправлено администратору!")

        # Изменяем offset на новый, чтобы не обрабатывать одно сообщение несколько раз
        return update['update_id']

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates['result']:
            offset = handle_updates(updates) + 1

if __name__ == '__main__':
    main()
