from flask import Flask, request, abort

from xfastest_crawler import get_news

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('Enter your key') # please enter your key
handler = WebhookHandler('Enter your webhook key') # please enter your webhook key


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text.lower() == "news":
        url = "https://news.xfastest.com/"
        get_xfastest_news(url)

    if event.message.text.lower() == "amd":
        url = "https://news.xfastest.com/category/amd/"
        get_xfastest_news(url)

    if event.message.text.lower() == "intel":
        url = "https://news.xfastest.com/category/intel/"
        get_xfastest_news(url)

    if event.message.text.lower() == "nvidia":
        url = "https://news.xfastest.com/category/nvidia/"
        get_xfastest_news(url)

    if event.message.text.lower() == "start":
        buttons_template = TemplateSendMessage(
            alt_text='Xfastest News',
            template=ButtonsTemplate(
                title='Xfastest News:',
                text='test',
                thumbnail_image_url='https://news.xfastest.com/wp-content/uploads/2015/07/XFNews-LOGO.png',
                actions=[
                    MessageTemplateAction(
                        label='news',
                        text='news'
                    ),
                    MessageTemplateAction(
                        label='amd',
                        text='amd'
                    ),
                    MessageTemplateAction(
                        label='intel',
                        text='intel'
                    ),
                    MessageTemplateAction(
                        label='nvidia',
                        text='nvidia'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)


def reply_msg(event, msg):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


def push_msg(msg):
    line_bot_api.push_message(
        'Your ID',
        TextSendMessage(text=msg))


def get_xfastest_news(url):
    title = "Xfastest News:\n\n"
    news = get_news(url)
    if news:
        for news in news:
            msg = title
            for item in news:
                msg += (item + "\n")
            push_msg(msg)
    else:
        push_msg(title + "today no news")


if __name__ == "__main__":
    app.run()
