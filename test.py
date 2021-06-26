import bot

speech = bot.Speech('start')

@speech.reaction('start', ['начать', 'погнали'])
def begin_order(message):
    print('Начинаем ваш заказ!')
    print('Какую пиццу вы будете? Большая/маленькая')
    return 'choose'

@speech.reaction('choose', ['Большая', 'Маленькая'])
def choose_size(message):
    print(f'Вы выбрали: {message}')
    print('Оплата наличкой или картой?')
    return 'payment'

@speech.reaction('payment', ['карта', 'наличные'])
def pay(message):
    if message == 'карта':
        print ('Вот наши реквизиты: 88005553535')
    else:
        print ('Как ты наличкой собрался по интернету заказывать?')
    return 'start'

while True:
    temp = str(input())
    speech.process(temp)
