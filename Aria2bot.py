#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   ____           __    __                                     
#  /\  _`\        /\ \__/\ \                                    
#  \ \ \L\ \__  __\ \ ,_\ \ \___     ___     ___                
#   \ \ ,__/\ \/\ \\ \ \/\ \  _ `\  / __`\ /' _ `\              
#    \ \ \/\ \ \_\ \\ \ \_\ \ \ \ \/\ \L\ \/\ \/\ \             
#     \ \_\ \/`____ \\ \__\\ \_\ \_\ \____/\ \_\ \_\            
#      \/_/  `/___/> \\/__/ \/_/\/_/\/___/  \/_/\/_/            
#               /\___/                                          
#               \/__/                                           
#   ____                                               ___      
#  /\  _`\                                            /\_ \     
#  \ \ \L\ \ __   _ __   ____    ___     ___      __  \//\ \    
#   \ \ ,__/'__`\/\`'__\/',__\  / __`\ /' _ `\  /'__`\  \ \ \   
#    \ \ \/\  __/\ \ \//\__, `\/\ \L\ \/\ \/\ \/\ \L\.\_ \_\ \_ 
#     \ \_\ \____\\ \_\\/\____/\ \____/\ \_\ \_\ \__/.\_\/\____\
#      \/_/\/____/ \/_/ \/___/  \/___/  \/_/\/_/\/__/\/_/\/____/
#                                                               
#                                                               
#   ____            __                                          
#  /\  _`\         /\ \__                                       
#  \ \ \L\ \    ___\ \ ,_\                                      
#   \ \  _ <'  / __`\ \ \/                                      
#    \ \ \L\ \/\ \L\ \ \ \_                                     
#     \ \____/\ \____/\ \__\                                    
#      \/___/  \/___/  \/__/                                    
#   
# Written by : Hamid reza kaveh pishghadam <hamidreza[at]hamidrezakp.ir>
# Date       : 6/5/17 at 17:40
# Version    : 1.1.0B
# License    : Apache License 2.0
#
# 
#Copyright 2017 Hamid reza kaveh pishghadam
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

#bot Token
BotApi = 'BOT API'
#admin name
admin = {} 
admin['name'] = 'Admin name'
admin['uid'] = 'Admin telegram ID'
#list of allowed users telegram id's
users = [] 
users.append(int(admin['uid']))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define some functions and few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

#start function
def start(bot, update, user_data):
    update.message.reply_text('Hi! i am ' + admin['name'] + '\'s personal bot , but i can help people that allowed me :)')    
    if check(bot, update) :
        bot.send_message(update.message.chat_id, 'wow! , i can help you , ' + admin['name'] + ' allowed me to help you :)')
        keyboard(bot, update)
        service(bot, update, user_data)
    else :
        bot.send_message(update.message.chat_id, 'opps! , i cannt help you , ' + admin['name'] + ' not allowed me to help you :(')

#check user permisions
def check(bot, update):
    if update.message.from_user.id in users:
        return True 
    else :
        return False
# message to admin function
def msg_admin(bot, update):
    if not check(bot, update) :
        return
    bot.send_message(admin['uid'], 'Hi ,\n ' + str(update.message.from_user) + ' \nsays : \n' + update.message.text)
# a function to manage all commands and texts
def service(bot, update, user_data):
    if not check(bot, update) :
        return

    if not 'state' in user_data:
        user_data['state'] = 'start'

    if user_data['state'] == 'msgadmin' :
        msg_admin(bot, update)
        user_data['state'] = ''
        return

    if user_data['state'] == 'addLink' and update.message.text.lower() == 'done' : 
        update.message.reply_text('Ok , I inserted your Link(s) to to my List, for check Completed Downloads \'Msg Admin\'')
        user_data['state'] = ''
        return

    if user_data['state'] == 'addLink' :
        add_link(update.message.text)
        return

    if update.message.text == 'Add DWNLD Link' :
        add_link('\n\n\n##Links from ' + str(update.message.from_user.id))
        update.message.reply_text('Ok , Listen carefully :\n+++Send links each one per line \n+++do not send me empty line or wrong things that are not link\n+++Example of correct links : \n    http://hamidrezakp.ir/movie.mkv\n    http://google.com/some/somefile.zip\n    http://somesite.net/something.jpg\n+++when you sent all links , send me "done"\n\nTnx you for using me correctly :)')
        user_data['state'] = 'addLink'
        return

    elif update.message.text == 'Ping' :
        bot.send_message(update.message.chat_id, 'Pong')
        return

    elif update.message.text == 'Msg Admin' :
        bot.send_message(update.message.chat_id, 'Ok , Send me message you want to say to ' + admin['name'])
        user_data['state'] = 'msgadmin'
        return

# a function to save download links
def add_link(text):
    List = open('/home/hamid/Downloads/List', 'a')
    List.write(text + '\n')
    List.close

# telegram replay keyboard maker
def keyboard(bot, update):
    keyboard_ = [['Add DWNLD Link', 'Ping'], ['Msg Admin']]
    reply_markup = ReplyKeyboardMarkup(keyboard_)
    bot.send_message(chat_id=update.message.chat_id, text="How Can i help you ?", reply_markup=reply_markup)

#logging errors
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(BotApi)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_user_data=True))

    # adding handlers to handle text messages
    dp.add_handler(MessageHandler(Filters.text, service, pass_user_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
