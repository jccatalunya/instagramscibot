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


"""
$ python2.7 skeleton.py <token>
A skeleton for your telepot programs.
"""

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/help':
        bot.sendMessage(chat_id, 'Hola! Sóc el InstaGramsci Bot un robot creat per l\'Instagram de la JCC.')


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)