from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    questions_answers = {
        "台北美食": "蚵仔煎、大腸包小腸、滷肉飯、鹽酥雞、牛肉面、小籠包、割包、芋圆、豆花、鳳梨酥",
        "西門町美食": "阿宗麵線、天天利美食坊、藍家割包、金峰滷肉飯、雪王冰淇淋、芋頭大王、HANA香雞排、三媽臭臭鍋、大墩夜市火鍋、燒肉工房
",
        "台南美食": "担仔面、蝦卷、碗粿、棺材板、牛肉湯、芋頭西米露、台南蜜餞",
        "花蓮美食": "炸蛋葱油餅、扁食、麻薯、海鲜粥、五霸焦糖包心粉圆、炸弹猪血糕",
        "台中美食": "太陽餅、大甲芋頭酥、肉圆、米糕",
        "台北夜市": "士林夜市、饒河夜市、寧夏夜市",
        "台南夜市": "花園夜市、大東夜市",
        "花蓮夜市": "自强夜市",
        "台中夜市": "逢甲夜市、中美街夜市、一中街夜市",
    }
    if msg in questions_answers:
        #print(f"{english_word} 的中文翻譯是：{words_dict[english_word]}")
    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(questions_answers[msg]))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
       
         

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
