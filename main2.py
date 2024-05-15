import telebot
from telebot import types


API_TOKEN = '7079191300:AAFta2NGT5jRy1kHVVNTcZcwCYUC9JVp5_4'

bot = telebot.TeleBot(API_TOKEN)


courses = {
    1: {
        'name': 'Курс 1',
        'description': 'Описание курса 1 - Задача организации, в особенности же дальнейшее развитие ивных условий.',
        'sections': {
            1: {
                'name': 'Тема 1',
                'lessons': {
                    1: 'Текст урока 1.1 - Разнообразный и богатый опыт начало  интересный эксперимент проверки новых предложений.', 
                    2: 'Текст урока 1.2 - Идейные соображения высшего порядка, a также рамки и место обучения кадров требуют от нас анализа новых предложений. Товарищи! сложившаяся структура организации способствует подготовки и реализации новых предложений.'
                }
            },
            2: {
                'name': 'Тема 2',
                'lessons': {
                    1: 'Текст урока 2.1 - C другой стороны постоазвития.',
                    2: 'Текст урока 2.2 - Таким образом консультация  широким  соответствует развития.же поя. ктивизации.'
                }
            }
        }
    },
    2: {
        'name': 'Курс 2',
        'description': 'Описание курса 2 - Повседневная практика показыв структуры представляет собой интересный эксперимент проверки модели развития.',
        'sections': {
            1: {
                'name': 'Тема 1',
                'lessons': {
                    1: 'Текст урока 1.1 - Таким образом постоянное информационно-пропагандистское словий активизации уточнения форм развития.',
                    2: 'Текст урока 1.2 - Значимость этих проблем настолько очевидна, что дальнейшее развитие различных форм деятельности в значительной степени обуславливает создание систем массового участия. Товарищи! сложившаяся структура организации позволяет выполнять важные задания по разработке соответствующий условий активизации.'
                }
            }
        }
    }
}


user_states = {}

def start_bot():
    @bot.message_handler(commands=['start'])
    def start(message):
        user_states[message.chat.id] = {'course': None, 'section': None, 'lesson': None}
        send_courses(message.chat.id)

    def send_courses(chat_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for course_id, course in courses.items():
            markup.add(types.KeyboardButton(course['name']))
        bot.send_message(chat_id, "Выберите курс:", reply_markup=markup)

    def send_sections(chat_id, course_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for section_id, section in courses[course_id]['sections'].items():
            markup.add(types.KeyboardButton(section['name']))
        markup.add(types.KeyboardButton("Назад"))
        bot.send_message(chat_id, "Выберите тему:", reply_markup=markup)

    def send_lessons(chat_id, course_id, section_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for lesson_id, lesson in courses[course_id]['sections'][section_id]['lessons'].items():
            markup.add(types.KeyboardButton(f"Урок {lesson_id}"))
        markup.add(types.KeyboardButton("Назад"))
        bot.send_message(chat_id, "Выберите урок:", reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        state = user_states.get(message.chat.id, None)
        if not state:
            return

        if state['course'] is None:
            for course_id, course in courses.items():
                if message.text == course['name']:
                    state['course'] = course_id
                    bot.send_message(message.chat.id, course['description'])
                    send_sections(message.chat.id, course_id)
                    return
            bot.send_message(message.chat.id, "Пожалуйста, выберите курс из списка.")

        elif state['section'] is None:
            if message.text == "Назад":
                state['course'] = None
                send_courses(message.chat.id)
                return

            course_id = state['course']
            for section_id, section in courses[course_id]['sections'].items():
                if message.text == section['name']:
                    state['section'] = section_id
                    send_lessons(message.chat.id, course_id, section_id)
                    return
            bot.send_message(message.chat.id, "Пожалуйста, выберите тему из списка.")

        elif state['lesson'] is None:
            if message.text == "Назад":
                state['section'] = None
                send_sections(message.chat.id, state['course'])
                return

            course_id = state['course']
            section_id = state['section']
            for lesson_id, lesson in courses[course_id]['sections'][section_id]['lessons'].items():
                if message.text == f"Урок {lesson_id}":
                    state['lesson'] = lesson_id
                    bot.send_message(message.chat.id, lesson)
                    send_navigation_buttons(message.chat.id)
                    return
            bot.send_message(message.chat.id, "Пожалуйста, выберите урок из списка.")

        else:
            if message.text == "Назад":
                state['lesson'] = None
                send_lessons(message.chat.id, state['course'], state['section'])
                return

            if message.text == "Вперед":
                course_id = state['course']
                section_id = state['section']
                lesson_id = state['lesson'] + 1
                if lesson_id in courses[course_id]['sections'][section_id]['lessons']:
                    state['lesson'] = lesson_id
                    bot.send_message(message.chat.id, courses[course_id]['sections'][section_id]['lessons'][lesson_id])
                else:
                    bot.send_message(message.chat.id, "Это последний урок в этой теме.")
                send_navigation_buttons(message.chat.id)
                return

            bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки для навигации.")

    def send_navigation_buttons(chat_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Назад"), types.KeyboardButton("Вперед"))
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

    bot.polling()

if __name__ == '__main__':
    start_bot()
