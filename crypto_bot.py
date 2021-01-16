import telebot
import requests
import json

API_TOKEN = ''

API_KEY = ''

top_coins_link = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

coin_info_link = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

coin_price_link = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

headers = {
    'X-CMC_PRO_API_KEY': API_KEY
}

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['coin'])
def coins_top_10(message):
    text = message.text.split(" ")
    if len(text) == 1:
        chat_id = message.chat.id
        response = requests.get(top_coins_link, headers=headers)
        top_10_coins = json.loads(response.text)
        top_10 = []
        for coin in top_10_coins['data'][:10]:
            top_10.append(coin)
        for coin in top_10:
            text = 'Name: {}\nSymbol: {}\nPrice in USD: {:.2f}'.format(coin['name'], coin['symbol'], coin['quote']['USD']['price'])
            bot.send_message(chat_id, text)
    else:
        bot.reply_to(message, "You do not have to give me any other details")

@bot.message_handler(commands=['coin_info'])
def coin_info(message):
    text = message.text.split(" ")
    if len(text) != 2:
        bot.reply_to(message, "Provide me with the symbol of a cryptocurrency.")
    else:
        chat_id = message.chat.id
        response = requests.get(coin_info_link + '?symbol={}'.format(text[1]), headers=headers)
        coins = json.loads(response.text)
        text1 = 'Website: {}\n\nTitle: {}\n\nDescription: {}'.format(coins['data'][text[1]]['urls']['website'][0], coins['data'][text[1]]['name'], coins['data'][text[1]]['description'])
        r = requests.get(coins['data'][text[1]]['logo'])
        bot.send_photo(chat_id, r.content)
        bot.send_message(chat_id, text1)

@bot.message_handler(commands=['coin_price'])
def coin_price(message):
    text = message.text.split(" ")
    if len(text) != 2:
        bot.reply_to(message, "Provide me with the symbol of a cryptocurrency.")
    else:
        chat_id = message.chat.id
        response = requests.get(coin_price_link + '?symbol={}'.format(text[1]), headers=headers)
        coin_prices = json.loads(response.text)
        text1 = 'Name: {}\n\nCurrent price: {}\n\nPercent change(1 hour): {}\n\nPercent change(24 hours): {}'.format(coin_prices['data'][text[1]]['name'], coin_prices['data'][text[1]]['quote']['USD']['price'], coin_prices['data'][text[1]]['quote']['USD']['percent_change_1h'], coin_prices['data'][text[1]]['quote']['USD']['percent_change_24h'])
        bot.send_message(chat_id, text1)

bot.polling()