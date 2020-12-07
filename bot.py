#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters
from bs4 import BeautifulSoup as bs
import os,time
import logging
import requests
import json
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
USERS=[1322746439,487596381,1300119173]
TOKEN="1416260313:AAG6LLlSu7oYi7eZ8DtqEA8LIC3y01v7IgQ"
FIRST= range(1)
# Callback data
EXIT, BACK, PAT, ONE, TWO, THREE= range(6)

def readthingspeakall(n,API,ch):
    msg=[]*n
    for f in range(n):
        URL='https://api.thingspeak.com/'
        CHA='channels/'+ch+'/fields/'+str(f+1)+'/last.json?api_key='
        KEY=API
        ZONE='&timezone=Asia%2FKolkata'
        NEW_URL=URL+CHA+KEY+ZONE
        print(NEW_URL)
        get_data=requests.get(NEW_URL).json()
        time=str(get_data['created_at'])
        msg.append(str(get_data['field'+str(f+1)]))
    return msg,time


def start(update, context):
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.username)
    keyboard = [
        [InlineKeyboardButton("🏥 Patient Status", callback_data=str(PAT))],
        [InlineKeyboardButton("🛑 Quit", callback_data=str(EXIT))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text='Hello @{}\nYou can Check Your Patients Status here'.format(user.username))
    update.message.reply_text(text='   🖥 Main Menu 🖥', reply_markup=reply_markup)
    return FIRST

def start_over(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("🏥 Patient Status", callback_data=str(PAT))],
        [InlineKeyboardButton("🛑 Quit", callback_data=str(EXIT))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="   🖥 Main Menu 🖥", reply_markup=reply_markup)
    return FIRST


def one(update,context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Back", callback_data=str(PAT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    a,time=readthingspeakall(3,'R4Y2EJ903LU3LG6M','1214517')
    if int(a[2]) == 1:
        status='Critical ⚠️'
    else:
        status='Stable ✅'
    moi='❤️ Pulse : {}'.format(a[0])+"\n"+'‍📈 Oxygen level : {}%'.format(a[1])+"\n"+'🤒 Condition : '+status+'\n'+'⌚ Last Updated  : '+time
    query.edit_message_text(
        text=moi,reply_markup=reply_markup
    )
def two(update,context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Back", callback_data=str(PAT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    a,time=readthingspeakall(3,'K5Z9ON9FSY09W810','1214520')
    if int(a[2]) == 1:
        status='Critical ⚠️'
    else:
        status='Stable ✅'
    moi='❤️ Pulse : {}'.format(a[0])+"\n"+'📈 Oxygen level : {}%'.format(a[1])+"\n"+'🤒 Condition : '+status+'\n'+'⌚ Last Updated  : '+time
    query.edit_message_text(
        text=moi,reply_markup=reply_markup
    )

def three(update,context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Back", callback_data=str(PAT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    a,time=readthingspeakall(3,'9KSTC84VSBLWLDIK','1214522')
    if int(a[2]) == 1:
        status='Critical ⚠️'
    else:
        status='Stable ✅'
    moi='❤️ Pulse : {}'.format(a[0])+"\n"+'‍📈 Oxygen level : {}%'.format(a[1])+"\n"+'🤒 Condition : '+status+'\n'+'⌚ Last Updated  : '+time
    query.edit_message_text(
        text=moi,reply_markup=reply_markup
    )

def patdata(update, context):
    userID = update.effective_message.chat_id
    if True:
        if userID == USERS[0]:
            query = update.callback_query
            query.answer()
            keyboard = [
                [
                    InlineKeyboardButton("🧑‍ Sample Patient 1", callback_data=str(ONE))
                ],
                [
                    InlineKeyboardButton("👧 Sample Patient 2", callback_data=str(TWO))
                ],
                [
                    InlineKeyboardButton("⬅️ Back", callback_data=str(BACK))
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            moi='Your Patients List Here'
            query.edit_message_text(text=moi,reply_markup=reply_markup)
            return FIRST
        elif userID == USERS[1]:
            query = update.callback_query
            query.answer()
            keyboard = [
                [
                    InlineKeyboardButton("🧑‍Sample Patient 1", callback_data=str(THREE))
                ],
                [
                    InlineKeyboardButton("⬅️ Back", callback_data=str(BACK))
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            moi='Your Patients List Here'
            query.edit_message_text(text=moi,reply_markup=reply_markup)
            return FIRST
        else:
            query = update.callback_query
            query.answer()
            keyboard = [
                [
                    InlineKeyboardButton("⬅️ Back", callback_data=str(BACK))
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            moi='Not Authorized'
            query.edit_message_text(text=moi,reply_markup=reply_markup)
            return FIRST

def end(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start,filters=Filters.user(USERS))],
        states={
            FIRST: [
                CallbackQueryHandler(end, pattern='^' + str(EXIT) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(patdata, pattern='^' + str(PAT) + '$'),
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
            ]
        },
        fallbacks=[CommandHandler('start', start,filters=Filters.user(USERS))],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
