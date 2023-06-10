import telebot
import requests
import json
import os
from config import *


def twitchAPIRequests(streamerName):

    # Getting Oauth token from twitch #
    #
    #
    #

    grant_type = 'client_credentials'

    authRequest = requests.post(
        f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}')
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

    getUsersRequest = requests.get(f'https://api.twitch.tv/helix/users?login={streamerName}', headers={
                                   'Authorization': f'Bearer {authorization}', 'Client-Id': client_id})
    getUsersJsonData = getUsersRequest.json()

    try:
        with open(f'streamersJsons/{streamerName}_info.json', 'w', encoding='utf-8') as file:
            json.dump(getUsersJsonData, file, indent=4, ensure_ascii=False)
    except UnicodeDecodeError:
        pass

    #
    #
    #
    # Getting streamer info from twitch #

    ######################################

    # Getting current stream info (LIVE or not) from twitch #
    #
    #
    #

    getStreamsRequest = requests.get(f'https://api.twitch.tv/helix/streams?user_login={streamerName}', headers={
                                     'Authorization': f'Bearer {authorization}', 'Client-Id': client_id})
    getStreamsJsonData = getStreamsRequest.json()

    try:
        with open(f'streamersJsons/{streamerName}_streamInfo.json', 'w', encoding='utf-8') as file:
            json.dump(getStreamsJsonData, file, indent=4, ensure_ascii=False)
    except UnicodeDecodeError:
        pass

    #
    #
    #
    # Getting current stream info (LIVE or not) from twitch #


def telegramBot():

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def startMessage(message):

        bot.send_message(message.chat.id,
                         f'\n'
                         f'   <b>Welcome to TwitchInfo Bot 🤖</b>\n'
                         f'\n'
                         f'<b>Creator: TYOLY</b>\n'
                         f'<b>Version: 0.0.1</b>\n'
                         f'\n'
                         f'<b>Type /getstreamerinfo or /gsi to start</b>\n', parse_mode="HTML")

    @bot.message_handler(commands=['getstreamerinfo', 'gsi'])
    def streamerInfo(message):

        bot.send_message(message.chat.id, 'Which streamer are interesting you?')
        bot.register_next_step_handler(message, userStreamerInput)

    def userStreamerInput(message):

        streamerName = message.text
        streamerStreamInfo = json.loads(open(f'streamersJsons/{streamerName}_streamInfo.json', encoding='utf-8').read())
        streamerInfo = json.loads(open(f'streamersJsons/{streamerName}_info.json').read())

        twitchAPIRequests(streamerName)

        try:
            try:
                for i in streamerStreamInfo['data'][0]:
                    if i == 'type':

                        streamerName = streamerInfo['data'][0]['display_name']
                        streamerType = streamerInfo['data'][0]['broadcaster_type']
                        streamViewers = streamerStreamInfo['data'][0]['viewer_count']
                        streamTitle = streamerStreamInfo['data'][0]['title']
                        streamGame = streamerStreamInfo['data'][0]['game_name']

                        bot.send_message(message.chat.id,
                                         f'<b><a href="http://twitch.tv/{streamerName}">{streamerName}</a></b>\n'
                                         f'<b>Status:</b> <i>{streamerType}</i>\n'
                                         f'<b>----------STREAM------------</b>\n'
                                         f'<b>Stream status:</b> <i>Online</i> 🔴\n'
                                         f'<b>Title:</b> <i>{streamTitle}</i>\n'
                                         f'<b>Game:</b> <i>{streamGame}</i>\n'
                                         f'<b>Current Viewers:</b> <i>{streamViewers} 👁</i>\n'
                                         f'<b>---------------------------------</b>\n', parse_mode='HTML')

                        os.remove(f'streamersJsons/{streamerName}_info.json')
                        os.remove(f'streamersJsons/{streamerName}_streamInfo.json')
                        os.remove(f'authToken.json')

                else:
                    pass

            except KeyError:

                bot.send_message(
                    message.chat.id, 'User doesnt exist or nickname is wrong')

        except IndexError or KeyError:

            streamerName = streamerInfo['data'][0]['display_name']
            streamerType = streamerInfo['data'][0]['broadcaster_type']

            bot.send_message(message.chat.id,
                             f'<b><a href="http://twitch.tv/{streamerName}">{streamerName}</a></b>\n'
                             f'<b>Status:</b> <i>{streamerType}</i>\n'
                             f'<b>----------STREAM------------</b>\n'
                             f'<b>Stream status:</b> <i>Offline</i> 🌕\n'
                             f'<b>---------------------------------</b>\n', parse_mode='HTML')

            os.remove(f'streamersJsons/{streamerName}_info.json')
            os.remove(f'streamersJsons/{streamerName}_streamInfo.json')
            os.remove(f'authToken.json')

            pass

    bot.polling(non_stop=True, interval=0)


def main():
    telegramBot()


if __name__ == '__main__':
    main()
