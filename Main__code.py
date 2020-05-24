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
            'общем', 'быть', 'так', 'что', 'самое', 'в', 'сделать', 'пожалуйста', 'может', 'быстро', '.', ',', '?'),
        'weather': (
            'какая погодка', 'расскажи погодку', 'расскажи погоду', "какая погода", "расскажи про погоду",
            "скажи погоду",
            "чё с погодой", "поведай погоду"),
        'utc_offset': {'москва': 3, 'санкт-петербург': 3, 'новосибирск': 7, 'екатеринбург': 5, 'нижний новгород': 3,
                       'казань': 3, 'челябинск': 5, 'омск': 6, 'самара': 4, 'ростов-на-дону': 3, 'уфа': 5,
                       'красноярск': 7, 'воронеж': 3, 'пермь': 5, 'волгоград': 4, 'краснодар': 3, 'калининград': 2,
                       'владивосток': 10, 'спб': 3},
        'what_time_is_it': (
        'который час', 'сколько время', 'расскажи время', 'который сейчас час', 'сколько щас время', 'подскажи время')}

# приветствие
print('''
Я какое-то подобие рабочего ассистента
Зовут меня VVM
Но ты можешь звать меня Валерой
Могу кое-что сделать для тебя
''')


# управление функциями
def manager_func(query):
    if query in data['what_time_is_it']:
        what_time()
    elif query in data['weather']:
        what_weather()


# основные функции
# время
def what_time():
    offset_city = input('Где? ').lower()
    if offset_city in data['utc_offset']:
        city_time = dt.datetime.utcnow() + dt.timedelta(hours=data['utc_offset'][offset_city])
        f_time = city_time.strftime("%H:%M:%S")
        print('Там где ты сказал сейчас', f_time)
    else:
        print('В базе такого города нет, но если попросить разраба, он может и добавит')


# погода
def what_weather():
    city = input('Где? ').lower()
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        print('<сетевая ошибка>')
    if response.status_code == 200:
        print(response.text.strip())
    else:
        print('<ошибка на сервере погоды>')


# убираем всю шелуху
def clean_query(query):
    raw_query = query.split(' ')
    for i in raw_query:
        if i in data['to_be_cleaned']:
            raw_query.remove(i)
    processed_query = ' '.join(raw_query)
    manager_func(processed_query)


# преобразование голоса в текст
def mic_record():
    # проверяем сообщение | выполняется 2
    def check_is_query(user_voice_query):
        if user_voice_query[0] in data['VA_names']:
            clean_query(user_voice_query)
        else:
            print('\n'
                  'Если ты что-то от меня хочешь\n'
                  'Назови моё имя вначале')

    # записываем голосовое сообщение | выполняется 1
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        raw_audio = r.listen(source, phrase_time_limit=3)
        user_audio = r.recognize_google(raw_audio, language='ru').lower()
        check_is_query(user_audio)


# записываем текстовое сообщение
def text_record():
    user_text_query = input().lower()
    clean_query(user_text_query)


# выбор метода ввода
while True:
    print('Как коммандовать будешь? Текст или голос?')
    choice_method_input = input()
    if choice_method_input in data['input_method']['text']:
        print('Хорошо, теперь пиши команду')
        text_record()
        break
    elif choice_method_input in data['input_method']['voice']:
        print('Теперь тебе говорить для управления мной')
        print('Говори что тебе нужно')
        engine.say('Теперь тебе нужно говорить для управления мной')
        engine.say('Говори что тебе нужно')
        engine.runAndWait()
        print('\n'
              'Идёт запись:')
        mic_record()
        break
    else:
        print('А тебя ведь нормально спросили')
        continue
