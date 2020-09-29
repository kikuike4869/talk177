from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pya3rt

app = Flask(__name__)

line_bot_api = LineBotApi(
    "J/NdqjOP9XsFGi/HwpPUjr8zYG/67R8muQ7SP0Unh1lVGZWnVje/vQOJ7IRuxi6et0p65kemHrddp3zd50miz2Wcog5/gYPMOHduv/ZE/bd/nwlytCaQ7BKI1ZclyVC+YzUlxc839BuPt58+gxo7qQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("82e521a6827593de9fdba188f3de8207")


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ai_message = talk_ai(event.message.text)
    if event.reply_token == "00000000000000000000000000000000":
        return
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=ai_message))


def talk_ai(word):
    apikey = 'DZZQASf79FgCb3DWhdXs7QtkWdHcy6Lz'
    client = pya3rt.TalkClient(apikey)
    reply_message = client.talk(word)

    return reply_message['results'][0]['reply']


if __name__ == "__main__":
    #    app.run()
    app.run()
