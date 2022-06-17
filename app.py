from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('V9cvlKMzF0llRfd1MljhCKPplNW/BxBY10sOljADcIqCTsdGh6K1kFBiEXvlBe6baIBbVWXnXSame+QixUlBH8BbWITyBeEbf5j4g74sKLR0KKRcfrnUrzKP4iehChwk++ZA5Vz0kmN37XuV+MXOxQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0cd143c030cd1e3d3f0e49ada04ae87d')


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
    r = '我看不懂你說什麼'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='6362',
            sticker_id='11087927'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是Amber建立的機器人'
    elif '飲料' in msg:
        r = '我最近喜歡可不可的珍奶'


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()