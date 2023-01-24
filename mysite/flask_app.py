from flask import Flask, request
import json
import logging
from flask_ngrok import run_with_ngrok
import git

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


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
    return {
        'response': {
            'text': 'Привет',
        },
        'version': '1.0'
    }

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        git.cmd.Git().pull('https://github.com/Ariestellar/PYAlice', 'main')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
