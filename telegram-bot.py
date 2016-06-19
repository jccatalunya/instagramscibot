# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 17:18:01 2016

@author: isman7
"""


import sys
import csv
import time
import telepot
import datetime
from dateutil.tz import tzlocal
import pytz
from instagram.client import InstagramAPI
import numpy as np
try:
    from matplotlib import pyplot as plt
    GRAPH = True
except ImportError:
    print('There is no tkinter aviable.')    
    GRAPH = False


#"Handmade" API
import json
import requests

telegram_token = sys.argv[1]  # get token from command-line
insta_access_token = sys.argv[2]
insta_client_id = sys.argv[3]
insta_client_secret = sys.argv[4]

url = "https://api.instagram.com/v1/users/self/?access_token={0}".format(insta_access_token)

insta_api = InstagramAPI(access_token=insta_access_token,  
                    client_ips=insta_client_id,
                    client_secret=insta_client_secret)

def get_insta_follows():
    user = insta_api.user('self')
    return user.counts['followed_by']
#    response = requests.get(url)
#    j = json.loads(response.text)
#    return j['data']['counts']['followed_by']

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Got command: %s' % command)
    command = command.split('@')[0]
    
    if command[0] == '/':
        if command == '/start':
            bot.sendMessage(chat_id, 'Hola! Sóc l\'Insta Gramsci Bot un robot creat per l\'Instagram de la JCC. Prova /followers o /graph.')
        elif command == '/help':
            bot.sendMessage(chat_id, 'Hola! Sóc l\'Insta Gramsci Bot un robot creat per l\'Instagram de la JCC. Prova /followers o /graph.')
        elif command == '/followers':
            followers = get_insta_follows()
            bot.sendMessage(chat_id, \
            'El compte [@joventutcomunistacat](https://www.instagram.com/joventutcomunistacat/) té actualment *{0}* persones com a seguidores!'\
            .format(followers), parse_mode='Markdown')
        elif '/graph' in command:
            if GRAPH:
                timestamp = []
                followers = []
                with open('followers.log', 'r') as f_log:
                    logreader = csv.reader(f_log, delimiter=';')
                    for row in logreader:
                        timestamp.append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
                        followers.append(int(row[1]))
                f_log.close()
                timestamp_ticks = np.array([date.strftime('%H:%M') if not index%24 else '' for index, date in enumerate(timestamp)])
                timestamp_decim = np.array([date.day + date.hour/24 + date.minute/60/24 for date in timestamp])
                
                plt.xticks(timestamp_decim, timestamp_ticks)
                locs, labels = plt.xticks()
                plt.setp(labels, rotation=45)
                plt.plot(timestamp_decim, followers, 'r.-', label='@joventutcomunistacat followers')
                if ' fit' in command:
                    try:
                        pol_order = int(command.split(' ')[-1])
                    except:
                        pol_order = 1
                    
                    fitted_coeff = np.polyfit(timestamp_decim, followers, pol_order)
                    fitted_followers = np.polyval(fitted_coeff, timestamp_decim) 
                    
                    plt.plot(timestamp_decim, fitted_followers, 'g--', label='pol. fitted followers (ord. {0})'.format(pol_order))
                #plt.show()
                ax = list(plt.axis())
                plt.axis([round(ax[0]), round(ax[1])+1, round(ax[2], -1)-10, round(ax[3], -1)+30]), 
                plt.xlabel('Hour'), plt.ylabel('Followers')
                #plt.grid()
                plt.legend()
                plt.savefig('temp_record_graph.png')
                bot.sendPhoto(chat_id, open('temp_record_graph.png', 'rb'))
                plt.close()
            else:
                bot.sendMessage(chat_id, \
                'Disculpes, la comanda /graph no està habilitada en aquest moement. El soviet treballarà per arreglar-la.')
                
        else:
            bot.sendMessage(chat_id, \
            'Disculpes, sembla que la comanda %s no ha sigut implementada pel soviet.'\
            % command)
    else:
        bot.sendMessage(chat_id, \
        'Disculpes però sembla que \'%s\' és un significant massa buit per mi. Utilitza comandes de Telegram com /help'\
        % command)

bot = telepot.Bot(telegram_token)
bot.message_loop(handle)
print('Listening ...')

captured = False

# Keep the program running.
while 1:
    
    actual_time = datetime.datetime.now()
    local = tzlocal()
    actual_time = actual_time.replace(tzinfo = local)
    tz = pytz.timezone('Europe/Madrid')
    actual_time = actual_time.astimezone(tz)
    if not actual_time.minute % 5:
        if not captured:
            followers = get_insta_follows()
            with open('followers.log', 'a') as f_log:
                f_log.write('{0};{1}\n'.format(str(actual_time)[:-6], followers))
            print('Revisió cada 5 min! La JCC té {0} seguidores'.format(followers))
            captured = True
    else:
        captured = False
    time.sleep(10)