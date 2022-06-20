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
    msg = event.message.text
    r = '很抱歉，我無法辨識您的敘述'
    
    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='446',
            sticker_id='2027'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['Hi', 'hi']:
        r = '嗨'
    elif msg == '吃飽了嗎':
        r = '還沒，你呢'
    elif msg == '你是誰':
        r = '菲比尋常御用機器人'
    elif '訂位' in msg:
        r = '您想預訂什麼呢'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()