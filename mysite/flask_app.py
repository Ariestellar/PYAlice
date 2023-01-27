from flask import Flask, request
import json
import logging
import git
import gspread

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Указываем путь к JSON с ключами для GoogleSheets
googleSheetsAPI = gspread.service_account(filename='pyalice-68958b2cdb2b.json')

# Получаем таблицу с тестом
tableWithTest = googleSheetsAPI.open_by_key('1r9DtG5vVRb71lgD-Mlr-42VhUog3q0HvkW7TvgpNbsM')
# Получаем список тестовых вопросов
list_test_questions = tableWithTest.sheet1.get_all_values()


# Массив первого порядка это каждый вопрос массив второго порядка это элементы вопроса у них индексы:
# Индексы:
# 0 - номер по порядку
# 1 - текст вопроса
# 2 - ответ на вопрос
# 3 - правильный развернутый ответ (используется и в режиме обучения)


def make_response(text, state=None, buttons=None, data_session=None):
    response = {'response': {'text': text}, 'session_state': {}, 'version': '1.0'}
    if data_session is not None:
        response['session_state'] = data_session
    if state is not None:
        response['session_state']['currentState'] = state
    if buttons:
        response['response']['buttons'] = buttons
    return response


def fallback(state):
    text = 'Прости, не расслышал, повтори ещё раз или выбери вручную.'
    return make_response(text, state)  # Возвращаем текущее состояние, что бы не сбросилось


# Запустить режим тестирования
def start_test_mode():  # Запуск режима тестирования
    text = 'Начинаю тестирование.\n' \
           'Операторы Python и теги HTML.\n' \
           'Для выхода в меню скажи: «Меню».\n' \
           'Если не хочешь отвечать на вопрос, скажи: «Пропустить».\n' \
           'Команда: «Ответ Инита», поможет узнать правильный ответ.\n' \
           + list_test_questions[1][1]
    return make_response(text, state='test', buttons=[button('Пропустить'), button('Ответ ИНИТА'), button('В меню')],
                         data_session={'currentQuestionIndex': 1})

#Логика процесса тестирования
def testing(event):  # Процесс тестирования
    buttons = [button('Пропустить'), button('Ответ ИНИТА'), button('В меню')]
    current_question_index = event['state']['session'].get('currentQuestionIndex', {})
    intents = event['request'].get('nlu', {}).get('intents')
    # Обрабатываем интенты «Пропустить» и «Ответ Инита»
    if 'skip' in intents:
        current_question_index += 1
        text = list_test_questions[current_question_index][1]
        return make_response(text, state='test', buttons=buttons,
                             data_session={'currentQuestionIndex': current_question_index})
    elif 'give_answer' in intents:
        text = list_test_questions[current_question_index][3]
        current_question_index += 1
        text += '\n\n' + list_test_questions[current_question_index][1]
        return make_response(text, state='test', buttons=buttons,
                             data_session={'currentQuestionIndex': current_question_index})

    # Проверяем ответы, если не сработали интенты
    if event['request'].get('command') == list_test_questions[current_question_index][2].lower():
        current_question_index += 1
        text = 'Верный ответ\n' + list_test_questions[current_question_index][1]
    else:
        text = 'Не верный ответ'

    return make_response(text, state='test', buttons=buttons,
                         data_session={'currentQuestionIndex': current_question_index})


def about_skill():
    text = 'Спасибо, что поинтересовались.\n' \
           ' Я могу рассказать об операторах Python и тегах HTML,\n' \
           ' а также протестировать твои знания.'
    return make_response(text)


def support():
    text = 'Возможности "ИНИТА GO":\n' \
           'Для начала тестирования скажи "Тест".\n' \
           'Я буду задавать вопросы по тегам Python и HTML.\n' \
           'Если ответишь неверно  -  подскажу правильный вариант.\n' \
           'В разделе обучения расскажу какие теги HTML, операторы и ключевые слова Python существуют и для чего они ' \
           'используются.\n' \
           'Если хочешь начать, скажи "Учиться".\n' \
           'Чтобы связаться с моими авторами, скажи "Связаться с разработчиком" и опиши свой вопрос или пожелание.'
    # Кнопки: Связь с разработчиками, Тест, Учиться, Выход, Повтори

    # Связь с разработчиками - 'Пожалуйста, скажи или напиши своё пожелание, я передам его команде разработки.'
    return make_response(text)


# Запустить режим обучения
def start_learning_mode():
    text = 'Давай начнем.\n' \
           'Для повтора скажи: «Повторить».\n ' \
           'Для выхода в меню скажи: «Меню».\n' \
           'Для перехода к следующему оператору скажи: «Дальше».\n'\
            + list_test_questions[1][3]
    return make_response(text, state='learning', buttons=[button('Повторить'), button('Дальше'), button('В меню')], data_session={'currentQuestionIndex': 1})

#Логика процесса обучения
def learning(event):
    buttons = [button('Повторить'), button('Дальше'), button('В меню')]
    current_question_index = event['state']['session'].get('currentQuestionIndex', {})
    intents = event['request'].get('nlu', {}).get('intents')
    text = ""
    # Обрабатываем интенты «Дальше» и «Повторить»
    if 'next' in intents:
        current_question_index += 1
        text = list_test_questions[current_question_index][3]
        return make_response(text, state='learning', buttons=buttons,
                             data_session={'currentQuestionIndex': current_question_index})
    elif 'repeat' in intents:
        text = list_test_questions[current_question_index][3]
        return make_response(text, state='learning', buttons=buttons,
                             data_session={'currentQuestionIndex': current_question_index})

    return make_response(text, state='learning', buttons=buttons)

def welcome_message():
    text = 'Привет! Меня зовут Инита.\n' \
           'Я, навык, который станет помощником в мире кода Python и HTML\n' \
           'Я тестирую твои знания и помогу обучиться новому.\n' \
           'Если возникнут вопросы о моей функциональности, скажи: «Инита, что ты умеешь?».\n' \
           'По другим вопросам тебе поможет команда: «Инита, помощь».\n' \
           'С чего начнём?\n' \
           'Учимся или тестируем знания?'
    return make_response(text,
                         buttons=[button('Тест'), button('Учиться'), button('Что ты умеешь?'), button('Инита помощь'),
                                  button('Выход'), button('Повтори')])


def menu():
    text = 'С чего начнём?\n' \
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
    state = event['state']['session'].get('currentState', {})  # Достаем состояние из запроса
    if event['session']['new']:
        return welcome_message()
    elif 'menu' in intents:  # Меню главнее теста т.к. в него можно вернутся откуда угодно
        return menu()
    elif state == 'test':
        return testing(event)
    elif state == 'learning':
        return learning(event)
    elif 'test' in intents:
        return start_test_mode()
    elif 'learning' in intents:
        return start_learning_mode()
    else:
        return fallback(state)


def button(title, hide=True):
    return {'title': title, 'hide': hide, }


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        git.cmd.Git().pull('https://github.com/Ariestellar/PYAlice', 'main')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
