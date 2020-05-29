import speech_recognition as sr
import datetime as dt
import pyttsx3 as pt
import requests
import webbrowser as bb
import random

engine = pt.init()

data = {'VA_names': ("валерий", "валерун", "валеран", "валерьич", "валера", "валерка", "валя",),
        'input_method': dict(text=("текст", "Текст", "ТексТ", "тЕкСт", "ТеКсТ", "ntrcn"),
                             voice=("голос", "Голос", "ГоЛоС", "гОлОс", "голосочек", "ujkjc")),
        'to_be_cleaned': (
            'будет', 'здесь', 'можно', 'возможно', 'по-другому', 'ещё', 'немножко', 'как-нибудь', 'и', 'вот', 'это',
            'общем', 'быть', 'так', 'что', 'самое', 'в', 'сделать', 'пожалуйста', 'может', 'во', 'быстро', '.', ',',
            '?', 'что', "ты", "давай", "хочу"),
        'weather': (
            'какая погодка', 'расскажи погодку', 'расскажи погоду', "какая погода", "расскажи про погоду",
            "скажи погоду", "чё с погодой", "поведай погоду", "погода", "какая погода сейчас на улице", 'gjujlf'),
        'utc_offset': {'москве': 3, 'санкт-петербурге': 3, 'новосибирске': 7, 'екатеринбурге': 5, 'нижнем новгороде': 3,
                       'казани': 3, 'челябинске': 5, 'омске': 6, 'самаре': 4, 'ростове на дону': 3, 'уфе': 5,
                       'красноярске': 7, 'воронеже': 3, 'перми': 5, 'волгограде': 4, 'краснодаре': 3, 'калининграде': 2,
                       'владивостоке': 10, 'спб': 3},
        'what_time_is_it': (
            'который час', 'сколько время', 'расскажи время', 'который сейчас час', 'сколько щас время',
            'подскажи время', "время", "скажи время", 'dhtvz'),
        'Show_me_what_you_can': ("умеешь", "можешь", "возможности", "djpvj;yjcnb"),
        'I_can_this': 'На данный момент я умею только такие вещи как\n'
                      '    Давать гороскопы (вместо анекдотов)\n'
                      '    Говорить время\n'
                      '    Рассказывать погоду\n'
                      '    Открывать браузер (тот что по-умолчанию)\n'
                      '    Делать запросы в Яндекс\n'
                      '    А для выхода введите "выход"'
                      'Понятное дело что не много, но мой разраб только учится',
        'exit': ("выход", "выйти", "всё", "ds[jl", "закончить", "конец", "стоп"),
        'i_dont_understand': ("непонимаю запроса", "что вы несёте", "нормально сказать можете", "у меня нет таких возможностей", "я так не умею"),
        'open_web': ("открой браузер", "открой окно браузера", "браузер"),
        'horoscope': dict(call=("сделай предсказание", "дай гороскоп", "предсказание по гороскопу"),
                          first=["Сегодня — идеальный день для новых начинаний.",
                                 "Оптимальный день для того, чтобы решиться на смелый поступок!",
                                 "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
                                 "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
                                 "Плодотворный день для того, чтобы разобраться с накопившимися делами."],
                          second=["Но помните, что даже в этом случае нужно не забывать про",
                                  "Если поедете за город, заранее подумайте про",
                                  "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
                                  "Если у вас упадок сил, обратите внимание на",
                                  "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"],
                          third=["отношения с друзьями и близкими.",
                                 "работу и деловые вопросы, которые могут так некстати помешать планам.",
                                 "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
                                 "бытовые вопросы — особенно те, которые вы не доделали вчера.",
                                 "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."],
                          fourth=["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
                                  "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
                                  "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
                                  "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
                                  "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."])}

# приветствие
print('''
Я какое-то подобие рабочего ассистента
Зовут меня VVM
Но ты можешь звать меня Валерой
Могу кое-что сделать для тебя
''')


# управление функциями
class manage_query:
    # управление функциями
    def manager_func(self, query):
        if query in data['Show_me_what_you_can']:
            print(data['I_can_this'])
            records().manage_of_record()
        elif query in data['exit']:
            print('Отключаюсь...')
            pass
        elif query in data['what_time_is_it']:
            functions().what_time()
        elif query in data['weather']:
            functions().what_weather()
        elif query in data['open_web']:
            functions().open_web()
        elif query == 'сделай запрос':
            functions().open_site()
        elif query in data['horoscope']['call']:
            functions().make_prediction()
        else:
            if method_of_input:
                dont_understand = random.choice(data['i_dont_understand'])
                engine.say(dont_understand)
                engine.runAndWait()
            print('Непонятный запрос какой-то\n'
                  'Для просмотра функций введи "возможности"\n'
                  '')
            records().manage_of_record()

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
            return processed_query
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
            offset_city = manage_query().clean_query(records().mic_record())
        if not method_of_input:
            offset_city = input('Где именно? ').lower()
        if offset_city in data['utc_offset']:
            city_time = dt.datetime.utcnow() + dt.timedelta(hours=data['utc_offset'][offset_city])
            f_time = city_time.strftime("%H:%M:%S")
            print('Там где ты сказал, сейчас', f_time)
            if method_of_input:
                engine.say('Там где ты сказал, сейчас')
                engine.say(f_time)
                engine.runAndWait()
        else:
            print('В базе такого города нет, но если попросить разраба, он может и добавит')
            if method_of_input:
                engine.say('Я не знаю такого города')
                engine.runAndWait()
        records().manage_of_record()

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
        location_of_call = False
        records().manage_of_record()

    # браузер
    def open_web(self):
        bb.open_new('https:')
        records().manage_of_record()

    # открытие конкретной страницы
    def open_site(self):
        global location_of_call
        location_of_call = True
        if method_of_input:
            site = records().mic_record()
        if not method_of_input:
            site = records().text_record()
        bb.open('https://yandex.ru/search/?text={}'.format(site), new=2)
        location_of_call = False
        records().manage_of_record()

    # предсказание
    def make_prediction(self):
        print("1 — Овен\n"
             "2 — Телец\n"
             "3 — Близнецы\n"
             "4 — Рак\n"
             "5 — Лев\n"
             "6 — Дева\n"
             "7 — Весы\n"
             "8 — Скорпион\n"
             "9 — Стрелец\n"
             "10 — Козерог\n"
             "11 — Водолей\n"
             "12 — Рыбы")
        if not method_of_input:
             print(input('Выберите свой знак зодиака: '))
        if method_of_input:
            global location_of_call
            location_of_call = True
            engine.say('выберите свой знак зодиака')
            records().mic_record()
        first = random.choice(data['horoscope']['first'])
        second = random.choice(data['horoscope']['second'])
        third = random.choice(data['horoscope']['third'])
        fourth = random.choice(data['horoscope']['fourth'])
        one = first, second
        two = third, fourth
        print(first, second)
        print(third, fourth)
        if method_of_input:
            engine.say(one)
            engine.say(two)
            engine.runAndWait()
        location_of_call = False
        records().manage_of_record()


# запись сообщений
class records:
    def manage_of_record(self):
        if method_of_input:
            manage_query().manager_func(manage_query().clean_query(records().mic_record()))
        else:
            manage_query().manager_func(manage_query().clean_query(records().text_record()))

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
                print('Слушаю твои уточнения\n'
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
                    return 'стоп'

    # записываем текстовое сообщение
    def text_record(self):
        if location_of_call == False:
            print('Хорошо, теперь пиши команду:')
        if location_of_call == True:
            print('Принемаются дополнения')
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
        manage_query().manager_func(manage_query().clean_query(records().text_record()))
        break
    elif choice_method_input in data['input_method']['voice']:
        method_of_input = True
        location_of_call = False
        print('Теперь тебе говорить для управления мной')
        engine.say('Теперь тебе нужно говорить для управления мной')
        engine.runAndWait()
        manage_query().manager_func(manage_query().clean_query(records().mic_record()))
        break
    else:
        if try_input != 3:
            print('А тебя ведь нормально спросили\n'
                  '')
            try_input += 1
        continue
