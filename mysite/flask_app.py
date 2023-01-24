from flask import Flask, request
import json
import logging
import git

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

#Это понадобится если нужен будет туннель
# from flask_ngrok import run_with_ngrok
# run_with_ngrok(app)  # Запустить ngrok при запуске приложения, нужен для проброски тоннеля сервера
# if __name__ == '__main__':
#     app.run()


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
        git.cmd.Git().pull('https://github.com/Ariestellar/PYAlice', 'main')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
