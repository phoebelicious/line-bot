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

line_bot_api = LineBotApi('RhKM1SSzWKipNj/V7a6an1wL9ieDSudhtcOU4svFbSnupraMUMZkN0t0IuroBIF5+qixUNlOvCPmUQDo18nDv+7ElqOXFLQk4a1gtFh+XjOXBzkrnvTWgmWQCXJhPF/i4xyMW5VFv552nCL8EUXHiAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('48d0f56c9f6650b8d34a7742287b79f5')


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