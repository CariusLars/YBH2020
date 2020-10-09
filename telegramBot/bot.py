import requests
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

customerServiceBot = BotHandler("1263413055:AAFXursJGPtJ3KSVUqio9A3ns05NzvhF4uM")
crmBot = BotHandler("1267709076:AAGJiap5x2-204WSb2P9nmUeMAz4jWqdQgY")
crmAgents=["266433173"]#, "84983156"] # Lars, Jan

greetings = ('hallo', 'guten tag', 'guten morgen', 'guten nachmittag', 'hi', 'servus', 'grüzi', 'gruezi','guten abend')
responses = ('ok', 'danke', 'alles klar', 'super')
now = datetime.datetime.now()

def main():
    new_offset = None
    today = now.day
    hour = now.hour
    readableDateTime = now.strftime("%d.%m.%Y, %H:%M")

    while True:
        customerServiceBot.get_updates(new_offset)

        last_update = customerServiceBot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        print(last_update['message'])
        #print(last_update.message.from_user.username)

        #print(last_chat_text)

        if last_chat_text.lower() in greetings and 6 <= hour < 12:
            customerServiceBot.send_message(last_chat_id, 'Guten Morgen {}, bitte senden Sie Ihre Anfrage in einer Nachricht, um eine schnellstmögliche Bearbeitung zu ermöglichen'.format(last_chat_name))

        elif last_chat_text.lower() in greetings and 12 <= hour < 17:
            customerServiceBot.send_message(last_chat_id, 'Guten Nachmittag {}, bitte senden Sie Ihre Anfrage in einer Nachricht, um eine schnellstmögliche Bearbeitung zu ermöglichen'.format(last_chat_name))

        elif last_chat_text.lower() in greetings and 17 <= hour < 23:
            customerServiceBot.send_message(last_chat_id, 'Guten Abend {}, bitte senden Sie Ihre Anfrage in einer Nachricht, um eine schnellstmögliche Bearbeitung zu ermöglichen'.format(last_chat_name))

        elif last_chat_text.lower() in responses:
            customerServiceBot.send_message(last_chat_id, 'Gerne')

        elif len(last_chat_text.lower()) > 10: #everything shorter is just garbage
            customerServiceBot.send_message(last_chat_id, 'Sehr geehrter {}, vielen Dank für Ihre Nachricht. Ihre Anfrage vom {} wurde an einen Kundenberater weitergegeben.\nIhr ewb Kundenservice'.format(last_chat_name, readableDateTime))
            # Distribute message to one of the agens TODO: include logic here
            # user_link = "[" + last_chat_name + "](tg://user?id=" + str(last_chat_id) + ")" # Markdown link to the user

            for agent in crmAgents:
                crmBot.send_message(agent, 'Kundenanfrage\nZeitstemepel: {}\nKunde: {}\nInhalt: {}'.format(readableDateTime, last_chat_name, last_chat_text))
                #crmBot.send_message(agent, "Antwort an:" + user_link, parse_mode = "Markdown")
        else:
            customerServiceBot.send_message(last_chat_id,
                                            'Bitte senden Sie Ihre Anfrage in einer Nachricht, um eine schnellstmögliche Bearbeitung zu ermöglichen')
        new_offset = last_update_id + 1

        #print(last_chat_id)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()