import telebot
import requests
import json
from config import *


def twitchAPIRequests(streamerName):
            # Getting Oauth token from twitch #
            #
            #
            #
            grant_type = 'client_credentials'

            authRequest = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}')
            jsonData = authRequest.json()

            with open(f'authToken.json', 'w') as file:
                json.dump(jsonData, file, indent=4, ensure_ascii=False)
            #
            #
            #
            # Getting Oauth token from twitch #

            ######################################

            # Getting streamer info from twitch #
            #
            #
            #
            authorizationJson = open('authToken.json')
            authorization = json.load(authorizationJson)
            authorization = authorization['access_token']

            getUsersRequest = requests.get(f'https://api.twitch.tv/helix/users?login={streamerName}', headers={'Authorization':f'Bearer {authorization}', 'Client-Id':client_id})
            getUsersJsonData = getUsersRequest.json()

            with open(f'{streamerName}_info.json', 'w', encoding='utf-8') as file:
                json.dump(getUsersJsonData, file, indent=4, ensure_ascii=False)
            #
            #
            #
            # Getting streamer info from twitch #
            
            ######################################

            # Getting current stream info (LIVE or not) from twitch #
            #
            #
            #
            getStreamsRequest = requests.get(f'https://api.twitch.tv/helix/streams?user_login={streamerName}', headers={'Authorization':f'Bearer {authorization}', 'Client-Id':client_id})
            getStreamsJsonData = getStreamsRequest.json()

            with open(f'{streamerName}_streamInfo.json', 'w', encoding='utf-8') as file:
                 json.dump(getStreamsJsonData, file, indent=4, ensure_ascii=False)
            #
            #
            #
            # Getting current stream info (LIVE or not) from twitch #    


def telegramBot():
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=['start'])
    def startMessage(message):
        bot.send_message(message.chat.id, 'Hello')

    @bot.message_handler(commands=['getstreamerinfo'])
    def streamerInfo(message):
        bot.send_message(message.chat.id, 'Which streamer are interesting you?')
        bot.register_next_step_handler(message, userStreamerInput)
        
    def userStreamerInput(message):
        
        streamerName = message.text
        twitchAPIRequests(streamerName)
        streamerStreamInfo = json.loads(open(f'{streamerName}_streamInfo.json').read())
        streamerLive = False

        sSI = streamerStreamInfo['data'][0]
        for key in sSI.keys():
            if key == 'type':
                print(key)
                streamerLive = True
                print(f'{streamerLive} in for loop')
                break
            elif key != 'type' or key not in sSI.keys():
                streamerLive = False
                continue
        print(f'{streamerLive} after for loop')
        if streamerLive == True:
            print('Online')
        else:
            streamerLive = False
            print('Offline')
             
                 
        
    bot.polling(non_stop=True, interval=0)

    

def main():
    telegramBot()

if __name__ == '__main__':
    main()