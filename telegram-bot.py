# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 17:18:01 2016

@author: isman7
"""


import sys
import time
import telepot
import random
import datetime



def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

#    if command == '/roll':
#        bot.sendMessage(chat_id, random.randint(1,6))
#    elif command == '/time':
#        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    command = command.split('@')[0]
    
    if command[0] == '/':
        if command == '/start':
            bot.sendMessage(chat_id, 'Hola! Sóc l\'Insta Gramsci Bot un robot creat per l\'Instagram de la JCC.')
        elif command == '/help':
            bot.sendMessage(chat_id, 'Hola! Sóc l\'Insta Gramsci Bot un robot creat per l\'Instagram de la JCC.')
        else:
            bot.sendMessage(chat_id, \
            'Disculpes, sembla que la comanda %s no ha sigut implementada pel soviet.'\
            % command)
    else:
        bot.sendMessage(chat_id, \
        'Disculpes però sembla que \'%s\' és un significant massa buit per mi. Utilitza comandes de Telegram com /help'\
        % command)

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)