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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()