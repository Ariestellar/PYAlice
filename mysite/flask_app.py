from flask import Flask, request
import json
import logging
import git

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def make_response(text, state=None, buttons=None):
    response = {'response': {'text': text}, 'session_state': {}, 'version': '1.0'}
    if state is not None:
        response['session_state']['screen'] = state
    if buttons:
        response['response']['buttons'] = buttons
    return response


def fallback(event):
    text = 'Прости, не расслышал, повтори ещё раз или выбери вручную.'
    return make_response(text,
                         event['meta']['interfaces']['screen'])  # Возвращаем текщее состояние, что бы не сбросилось


def test(intent_name=None):
    text = 'Начинаю тестирование.' \
           'Операторы Python и теги HTML.' \
           'Для выхода в меню скажи: «Меню».' \
           'Если не хочешь отвечать на вопрос, скажи: «Пропустить».' \
           'Команда: «Ответ Инита», поможет узнать правильный ответ.'
    return make_response(text, state='test')


def about_skill():
    text = 'Спасибо, что поинтересовались.' \
           ' Я могу рассказать об операторах Python и тегах HTML,' \
           ' а также протестировать твои знания.'
    return make_response(text)


def support():
    text = 'Возможности "ИНИТА GO":' \
           'Для начала тестирования скажи "Тест".' \
           'Я буду задавать вопросы по тегам Python и HTML.' \
           'Если ответишь неверно  -  подскажу правильный вариант.' \
           'В разделе обучения расскажу какие теги HTML, операторы и ключевые слова Python существуют и для чего они используются. Если хочешь начать, скажи "Учиться".' \
           'Чтобы связаться с моими авторами, скажи "Связаться с разработчиком" и опиши свой вопрос или пожелание.'
    # Кнопки: Связь с разработчиками, Тест, Учиться, Выход, Повтори

    # Связь с разработчиками - 'Пожалуйста, скажи или напиши своё пожелание, я передам его команде разработки.'
    return make_response(text)


def learning():
    text = 'Давай начнем.' \
           'Для повтора скажи: «Повторить», для возврата в главное меню скажи: «Назад», для перехода к следующему оператору скажи: «Дальше».'
    return make_response(text, state='learning')


def welcome_message():
    text = 'Привет! Меня зовут Инита. Я, навык, который станет помощником в мире кода Python и ' \
           'Я тестирую твои знания и помогу обучиться новому.' \
           'Если возникнут вопросы о моей функциональности, скажи: «Инита, что ты умеешь?».' \
           'По другим вопросам тебе поможет команда: «Инита, помощь».' \
           'С чего начнём? ' \
           'Учимся или тестируем знания?'
    return make_response(text,
                         buttons=[button('Тест'), button('Учиться'), button('Что ты умеешь?'), button('Инита помощь'),
                                  button('Выход'), button('Повтори')])


def menu():
    text = 'С чего начнём? ' \
           'Учимся или тестируем знания?'
    return make_response(text,
                         buttons=[button('Тест'), button('Учиться'), button('Что ты умеешь?'), button('Инита помощь'),
                                  button('Выход'), button('Повтори')])


def goodbye_message():
    text = 'Всего доброго!'
    return make_response(text)


@app.route('/', methods=["POST"])
def main():
    event = request.json
    intents = event['request'].get('nlu', {}).get('intents')  # Достаем словарь интентов из запроса
    logging.info('Intents-state:')
    logging.info(intents)
    #state = event['request'].get('screen').get('session_state', {})  # Достаем состояние из запроса
    state = event['request']  # Достаем состояние из запроса
    logging.info('CurrentState:')
    logging.info(state)
    if event['session']['new']:
        return welcome_message()
    #elif state == 'test':
        #return test()
    elif 'menu' in intents:
        return menu()
    elif 'test' in intents:
        return test()
    elif 'learning' in intents:
        return learning()
    else:
        return fallback(event)


def button(title, hide=True):
    return {'title': title, 'hide': hide, }


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        git.cmd.Git().pull('https://github.com/Ariestellar/PYAlice', 'main')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
