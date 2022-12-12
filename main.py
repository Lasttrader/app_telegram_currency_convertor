import telebot
#from extensions import APIException, Convertor
from config import TOKEN, symbols
from extensions import APIException, Convertor
import traceback

#подставляем токен в телеграм бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет! \n Это конвертор. \n Введите сообщение в формате: сумма валюты и целевая валюта, например '200 EUR USD'.\n в запросе нужно указывать принятые сокращения валют"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for k,v in symbols.items():
        text = '\n'.join((text, k, v))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    #разделяем на слова строку c запросом
    query_text = message.text.split(' ')
    print(query_text)
    
    #Формируем запрос
    try:
        if len(query_text) != 3:
            raise APIException('Неверное количество параметров!')
        #вызываем функцию из библиотеки extensions            
        answer = Convertor.get_price(query_text[1], query_text[2], query_text[0])
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message, answer)

bot.polling()

