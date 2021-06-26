import bot

# Dummy userobj
class User():
    state = None
    name = None
    
    def __init__(self, name, state=None):
        self.name = name
        self.state = state
    
    def get_state(self):
        return self.state
    
    def set_state(self, name):
        self.state = name

dummyuser = User('John Doe')

speech = bot.Speech()
speech.read_states_json('sample.json')

@speech.greeting()
def greet(user, message):
    print(f'Добрый день, {user.name}!')

@speech.reaction('start', ['начать', 'погнали'])
def begin_order(user, message):
    print('Начинаем ваш заказ!')
    print('Какую пиццу вы будете? Большая/маленькая')
    return 'choose'

@speech.reaction('choose', ['Большая', 'Маленькая'])
def choose_size(user, message):
    print(f'Вы выбрали: {message}')
    print('Оплата наличкой или картой?')
    return 'payment'

@speech.reaction('payment', ['карта', 'наличные'])
def pay(user, message):
    if message == 'карта':
        print ('Вот наши реквизиты: 88005553535')
        print ('Укажите карту для перевода')
        return 'cardinfo'
    else:
        print ('Как ты наличкой собрался по интернету заказывать?')
        return 'payment'

@speech.raw('cardinfo')
def card(user, message):
    print(f'{user.name}, ваш заказ оплатится с карты {message}')
    return 'start'

# When requesting action, valid user object should be provided.
# Dummy dummyuser is used for testing here
while True:
    temp = str(input())
    unknown_phrase = speech.process(dummyuser, temp)

    if unknown_phrase:
        print(f'{unknown_phrase}')
