# Dev RAD - @R_AFX  Telegram Channls : @radfx2 
from pyrogram import Client, filters, types 
from requests import get
import json
import asyncio 

# bot helpers 
BOT_MESSAGE = {
    'JOIN_CHANLL':
                u'عذرن عزيزي عليك الاشترك بي قناة البوت اولان لي استخدام البوت 🧩💬.'
                u'\n\n Channl : @{} 💭🔰.'
                u'\n\n  👇 قم بي الاشترك من ثم اضغط علا زر تحقق 🔱🔗 .'
                u'',
    'DONE_JOIN_CHANNL':
                    u'شكرأ لك على الاشتراك في قنات البوت 〽️🧩.'
                    u'\n\n الان فم بي ارسال ( /start ) لي تشغيل البوت ♻️🔱.'
                    u'\n\n اتمنة لك تجربا ممتعة ✅🤍'
                    u'\n معا تحيات 𝗗𝗘𝗩 RAD - @R_AFX 💬👨‍💻'
                    u''
}

def CHECK_JOIN_KEYBOARD(Channl: str):
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text='قناة البوت 〽️💭.', url=f't.me/{Channl}'),
            types.InlineKeyboardButton(text='تحقق ♻️.', callback_data='checkjoin')
        ]
    ])
def REDRESH_LANSHER(text: str):
    return types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(text=text, callback_data='NOT')
        ]
    ])
    
## api chack member join from channls
async def CHECK_USER_JOIN(api_key, channls_join: list, user_id : int):
    c ,r = None ,False
    statues = ['administrator','creator','member','restricted']
    for channl in channls_join:
        url =f"https://api.telegram.org/bot{api_key}/getChatMember?chat_id=@{channl}&user_id={str(user_id)}"
        respons = get(url)
        JSObj = json.loads(respons.text) 
        user_state = JSObj['result']['status']
        if user_state in statues:
            r = True 
        else : 
            r = False
            c = channl
            return r,c
    return r,c

API_KEY = '6615093788:AAEb6Ti5PtfaJ46c17ps2vmoaiP-S_jMXnQ'
BOT_CHANNL = ['radfx2']
app = Client(
    'rad',
    bot_token=API_KEY, 
    api_id=22119881 , # userbot api id  
    api_hash='95f5f60466a696e33a34f297c734d048' # userbot api hash
)

@app.on_message(filters.regex('^/start$') & filters.private)
async def START_BOT(_, message: types.Message):
    chat_id, message_id, user_id = message.chat.id, message.id, message.from_user.id
    join_, channl = await CHECK_USER_JOIN(API_KEY,BOT_CHANNL, user_id)
    if not join_:
        await app.send_message(chat_id=chat_id, text=BOT_MESSAGE['JOIN_CHANLL'].format(channl), reply_markup=CHECK_JOIN_KEYBOARD(channl))
        return 
    await app.send_message(chat_id, 'Welcome to bot .')


@app.on_callback_query(filters.regex('^checkjoin$'))
async def CHAECK_JOIN(_, query: types.CallbackQuery):
    await app.edit_message_text(text='انتضر جاري التحقق من الاشتراك ⚙️.', reply_markup=REDRESH_LANSHER('تحقق من الاشتراك♻️⚙️.'), chat_id=query.message.chat.id, message_id=query.message.id)
    await asyncio.sleep(0.3)
    join_, channl = await CHECK_USER_JOIN(API_KEY, BOT_CHANNL, query.from_user.id)
    if not join_:
        await app.edit_message_text(text=BOT_MESSAGE['JOIN_CHANLL'].format(channl), reply_markup=CHECK_JOIN_KEYBOARD(channl) ,chat_id= query.message.chat.id, message_id=query.message.id)    
        await app.answer_callback_query(query.id, 'تأكد من اشتراك في القناة و اعد المحاولا ✅〽️.', show_alert=True)  
        return
    await app.edit_message_text(text=BOT_MESSAGE['DONE_JOIN_CHANNL'], chat_id= query.message.chat.id, message_id=query.message.id)



asyncio.run(app.run())