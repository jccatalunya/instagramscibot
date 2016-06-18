# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 17:18:01 2016

@author: isman7
"""


import sys
import time
import telepot
import datetime

#"Handmade" API
import json
import requests



def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Got command: %s' % command)
    command = command.split('@')[0]
    
    if command[0] == '/':
        if command == '/start':
            bot.sendMessage(chat_id, 'Hola! Sóc l\'Insta Gramsci Bot un robot creat per l\'Instagram de la JCC.')
        elif command == '/help':
            bot.sendMessage(chat_id, 'Hola! Sóc l\'Insta Gramsci Bot un robot creat per l\'Instagram de la JCC.')
        elif command == '/followers':
            response = requests.get(url)
            j = json.loads(response.text)
            followers = str(j['data']['counts']['followed_by'])
            bot.sendMessage(chat_id, \
            'El compte [@joventutcomunistacat](https://www.instagram.com/joventutcomunistacat/) té actualment *%s* persones com a seguidores!'\
            % followers, parse_mode='Markdown')
            
        else:
            bot.sendMessage(chat_id, \
            'Disculpes, sembla que la comanda %s no ha sigut implementada pel soviet.'\
            % command)
    else:
        bot.sendMessage(chat_id, \
        'Disculpes però sembla que \'%s\' és un significant massa buit per mi. Utilitza comandes de Telegram com /help'\
        % command)

telegram_token = sys.argv[1]  # get token from command-line
insta_access_token = sys.argv[2]
insta_client_id = sys.argv[3]
insta_client_secret = sys.argv[4]

url = "https://api.instagram.com/v1/users/self/?access_token={0}".format(insta_access_token)


bot = telepot.Bot(telegram_token)
bot.message_loop(handle)
print('Listening ...')

captured = False

# Keep the program running.
while 1:
    
    actual_time = datetime.datetime.now()
    if not actual_time.minute % 5:
        if not captured:
            response = requests.get(url)
            j = json.loads(response.text)
            followers = str(j['data']['counts']['followed_by'])
            print(followers)
            captured = True
    else:
        captured = False
    time.sleep(10)