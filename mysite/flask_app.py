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

# class ClientStates():
#     test = State()
#     learn = State()

def make_response(text):
    return {'response': {'text': text}, 'version': '1.0'}


def fallback():
    text = 'Прости, не расслышал, повтори ещё раз или выбери вручную.'
    return make_response(text)


def start_test():
    #ClientStates.test.Set()
    text = 'Начинаю тестирование.' \
           'Операторы Python и теги HTML.' \
           'Для выхода в меню скажи: «Меню».' \
           'Если не хочешь отвечать на вопрос, скажи: «Пропустить».' \
           'Команда: «Ответ Инита», поможет узнать правильный ответ.'
    return make_response(text)


def start_about():
    text = 'Спасибо, что поинтересовались.' \
           ' Я могу рассказать об операторах Python и тегах HTML,' \
           ' а также протестировать твои знания.'
    return make_response(text)

def start_help():
    text = 'Возможности "ИНИТА GO":' \
           'Для начала тестирования скажи "Тест".' \
           'Я буду задавать вопросы по тегам Python и HTML.' \
           'Если ответишь неверно  -  подскажу правильный вариант.' \
           'В разделе обучения расскажу какие теги HTML, операторы и ключевые слова Python существуют и для чего они используются. Если хочешь начать, скажи "Учиться".' \
           'Чтобы связаться с моими авторами, скажи "Связаться с разработчиком" и опиши свой вопрос или пожелание.'
            # Кнопки: Связь с разработчиками, Тест, Учиться, Выход, Повтори


            #Связь с разработчиками - 'Пожалуйста, скажи или напиши своё пожелание, я передам его команде разработки.'
    return make_response(text)

def start_learning():
    text = 'Давай начнем.' \
           'Для повтора скажи: «Повторить», для возврата в главное меню скажи: «Назад», для перехода к следующему оператору скажи: «Дальше».'
    return make_response(text)


def welcome_message():
    text = 'Привет! Меня зовут Инита. Я, навык, который станет помощником в мире кода Python и ' \
           'Я тестирую твои знания и помогу обучиться новому.' \
           'Если возникнут вопросы о моей функциональности, скажи: «Инита, что ты умеешь?».' \
           'По другим вопросам тебе поможет команда: «Инита, помощь».' \
           'С чего начнём? ' \
           'Учимся или тестируем знания?'

    #Кнопки: Тест, Учиться, Что ты умеешь? Инита помощь, Выход, Повтори
    return make_response(text)


def goodbye_message():
    text = 'Всего доброго!'

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
