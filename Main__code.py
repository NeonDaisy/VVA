import speech_recognition as sr
import datetime as dt
import pyttsx3 as pt
import requests

engine = pt.init()

data = {'VA_names': ("валерий", "валерун", "валеран", "валерьич", "валера", "валерка", "валя",),
        'input_method': dict(text=("текст", "Текст", "ТексТ", "тЕкСт", "ТеКсТ", "ntrcn"),
                             voice=("голос", "Голос", "ГоЛоС", "гОлОс", "голосочек", "ujkjc")),
        'to_be_cleaned': (
            'будет', 'здесь', 'можно', 'возможно', 'по-другому', 'ещё', 'немножко', 'как-нибудь', 'и', 'вот', 'это',
            'общем', 'быть', 'так', 'что', 'самое', 'в', 'сделать', 'пожалуйста', 'может', 'во', 'быстро', '.', ',', '?'),
        'weather': (
            'какая погодка', 'расскажи погодку', 'расскажи погоду', "какая погода", "расскажи про погоду",
            "скажи погоду", "чё с погодой", "поведай погоду", "погода", "какая погода сейчас на улице"),
        'utc_offset': {'москве': 3, 'санкт-петербурге': 3, 'новосибирске': 7, 'екатеринбурге': 5, 'нижнем новгороде': 3,
                       'казани': 3, 'челябинске': 5, 'омске': 6, 'самаре': 4, 'ростове на дону': 3, 'уфе': 5,
                       'красноярске': 7, 'воронеже': 3, 'перми': 5, 'волгограде': 4, 'краснодаре': 3, 'калининграде': 2,
                       'владивостоке': 10, 'спб': 3},
        'what_time_is_it': (
            'который час', 'сколько время', 'расскажи время', 'который сейчас час', 'сколько щас время',
            'подскажи время', "время", "скажи время")}

# приветствие
print('''
Я какое-то подобие рабочего ассистента
Зовут меня VVM
Но ты можешь звать меня Валерой
Могу кое-что сделать для тебя
''')


class manage_query:
    # управление функциями
    def manager_func(self, query):
        if query in data['what_time_is_it']:
            functions().what_time()
        elif query in data['weather']:
            functions().what_weather()
        else:
            if method_of_input:
                engine.say('непонимаю запроса')
                engine.runAndWait()
            print('Непонятный запрос какой-то\n'
                  'Для просмотра функций введи "возможности"')


    # убираем всю шелуху
    def clean_query(self, query):
        if query is not None:
            raw_query = query.split(' ')
            for dirty in raw_query:
                if dirty in data['to_be_cleaned']:
                    raw_query.remove(dirty)
                elif dirty in data['VA_names']:
                    raw_query.remove(dirty)
            processed_query = ' '.join(raw_query)
            manage_query().manager_func(processed_query)
        else:
            pass


# основные функции
class functions:
    # время
    def what_time(self):
        if method_of_input:
            print('Где именно?')
            engine.say('Где именно?')
            engine.runAndWait()
            global location_of_call
            location_of_call = True
            offset_city = records().mic_record()
        if not method_of_input:
            offset_city = input('Где именно? ').lower()
        if offset_city in data['utc_offset']:
            city_time = dt.datetime.utcnow() + dt.timedelta(hours=data['utc_offset'][offset_city])
            f_time = city_time.strftime("%H:%M:%S")
            print('Там где ты сказал, сейчас', f_time)
            engine.say('Там где ты сказал, сейчас')
            engine.say(f_time)
            engine.runAndWait()
        else:
            print('В базе такого города нет, но если попросить разраба, он может и добавит')
            engine.say('Я не знаю такого города')
            engine.runAndWait()

    # погода
    def what_weather(self):
        if method_of_input:
            print('Где именно?')
            engine.say('Где именно?')
            engine.runAndWait()
            global location_of_call
            location_of_call = True
            city = records().mic_record()
        if not method_of_input:
            city = input('Где именно? ').lower()
        url = f'http://wttr.in/{city}'
        weather_parameters = {
            'format': 2,
            'M': ''
        }
        try:
            response = requests.get(url, params=weather_parameters)
        except requests.ConnectionError:
            if method_of_input:
                engine.say('какая-то ошибка')
                engine.runAndWait()
            print('<сетевая ошибка>')
        if response.status_code == 200:
            print(response.text.strip())
        else:
            if method_of_input:
                engine.say('какая-то ошибка')
                engine.runAndWait()
            print('<ошибка на сервере погоды>')


# запись сообщений
class records:
    # преобразование голоса в текст
    def mic_record(self):
        try_to_rec = 0
        while True:
            if try_to_rec == 0 and not location_of_call:
                print('Говори что тебе нужно\n'
                      '')
                engine.say('Говори что тебе нужно')
                engine.runAndWait()
            elif try_to_rec == 0 and location_of_call:
                print('Слушая твои уточнения\n'
                      '')
                engine.say('слушаю твои уточнения')
                engine.runAndWait()
            elif 0 < try_to_rec < 2:
                print('Слушаю внимательней\n'
                      '')
                engine.say('Слушаю внимательней')
                engine.runAndWait()
            try:
                # записываем голосовое сообщение
                r = sr.Recognizer()
                with sr.Microphone(device_index=1) as source:
                    raw_audio = r.listen(source, phrase_time_limit=3)
                    user_audio = r.recognize_google(raw_audio, language='ru').lower()
                    return user_audio
            except sr.UnknownValueError:
                if try_to_rec < 2:
                    print("Нихера не слышно, говори в микрофон")
                    engine.say('повторите пожалуйста')
                    engine.runAndWait()
                    try_to_rec += 1
                    continue
                if try_to_rec == 2:
                    print('Всё равно не слышно, проверте микрофон')
                    engine.say('Я вас не слышу')
                    engine.runAndWait()
                    break

    # записываем текстовое сообщение
    def text_record(self):
        print('Хорошо, теперь пиши команду')
        user_text_query = input().lower()
        return user_text_query


# выбор метода ввода
try_input = 0
while True:
    if try_input == 0:
        print('Как коммандовать будешь? Текст или голос?')
    elif 0 < try_input < 3:
        print('Так всё же, как мне команды воспринимать?')
    elif try_input == 3:
        print('Всё равно ничего не понимаю\n'
              'Отключаюсь...')
        break
    choice_method_input = input()
    if choice_method_input in data['input_method']['text']:
        method_of_input = False
        location_of_call = False
        manage_query().clean_query(records().text_record())
        break
    elif choice_method_input in data['input_method']['voice']:
        method_of_input = True
        location_of_call = False
        print('Теперь тебе говорить для управления мной')
        engine.say('Теперь тебе нужно говорить для управления мной')
        engine.runAndWait()
        manage_query().clean_query(records().mic_record())
        break
    else:
        if try_input != 3:
            print('А тебя ведь нормально спросили\n'
                  '')
            try_input += 1
        continue
