from flask import Flask, request
import json
import logging
#
from flask_ngrok import run_with_ngrok
from pip._internal.vcs import git

app = Flask(__name__)
run_with_ngrok(app)  # Запустить ngrok при запуске приложения, нужен для проброски тоннеля сервера
logging.basicConfig(level=logging.DEBUG)


def make_response(text):
    return {'response': {'text': text}, 'version': '1.0'}


def fallback():
    text = 'Не понятно, повторите'
    return make_response(text)


def start_test():
    text = 'Начинаем тест'
    return make_response(text)


def start_learning():
    text = 'Начинаем обучение'
    return make_response(text)


def welcome_message():
    text = 'Приветcтвенное сообщение'
    return make_response(text)


@app.route('/', methods=["POST"])
def main():
    req = request.json
    intents = req['request'].get('nlu', {}).get('intents')  # Достаем словарь интентов из запроса
    print(intents)
    if req['session']['new']:
        return welcome_message()
    elif 'start_test' in intents:
        return start_test()
    elif 'start_learning' in intents:
        return start_learning()
    else:
        return fallback()


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


# request = {
#     "meta": {
#         "locale": "ru-RU",
#         "timezone": "UTC",
#         "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
#         "interfaces": {
#             "screen": {},
#             "payments": {},
#             "account_linking": {}
#         }
#     },
#     "session": {
#         "message_id": 0,
#         "session_id": "35f9ca30-36dd-4508-bb99-c04f021c0859",
#         "skill_id": "3529be8e-8eb3-4079-b432-671445c16834",
#         "user": {
#             "user_id": "AD1318CEB34263AE62E329C3A4C52E651484515C695D3535986B302D7D3330A7"
#         },
#         "application": {
#             "application_id": "CCB5DE9619835812132D9117146BED632190A27C16D4204DC95B448292F91EFB"
#         },
#         "user_id": "CCB5DE9619835812132D9117146BED632190A27C16D4204DC95B448292F91EFB",
#         "new": 'true'
#     },
#     "request": {
#         "command": "",
#         "original_utterance": "",
#         "nlu": {
#             "tokens": [],
#             "entities": [],
#             "intents": {}
#         },
#         "markup": {
#             "dangerous_context": 'false'
#         },
#         "type": "SimpleUtterance"
#     },
#     "version": "1.0"
# }

if __name__ == '__main__':
    app.run()
    # print(test(request))
