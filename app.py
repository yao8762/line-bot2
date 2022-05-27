from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('t2JstwjclwZnDYjG9hUuB+oBicB2so4FHcS0dvIJKkKOrg3GfdS4BkqTxVwTmq1+/4TkCzUU1MSDOMOkCvxGvrwv0Mok7aUNgsuOEPGX2UcItj6k1iLnhxXEvI0oZ2MFsiXtxK9Gq0r0c6dWeoQj0QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2cbf50d641888ff889bd1498f6d9ee7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，我看不懂'

    if msg in ['hi', 'Hi', 'HI']:
        r = '哈囉'
    elif msg == '你吃飯了嗎?':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()