#!/usr/bin/env python3

import requests
import time
import argparse
import os
import json

from requests.compat import urljoin

from utils import *
from dialogue_manager import DialogueManager
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pip install telepot
pip install telegram or !git clone https://github.com/python-telegram-bot/python-telegram-bot
# extract info-
import telepot
token = '1316484604:AAGQAmFLWe19zTt4XYP--1e7Q52X6kL7NWE'
TelegramBot = telepot.Bot(token)
print( TelegramBot.getMe())

# get the backend
TelegramBot.getUpdates()

Simple Bot to reply to Telegram messages.
This is built on the API wrapper for communicating with the Telegram Service. Authentication from the bot is done using an auth file with the chatID,
phone number and the name of the approved users, already saved in Admin.json. 

To perfectly run this script, you need to create a bot on Telegram and provide the bot id below (line 27)
"""
import telegram
import telebot
from telegram.error import NetworkError, Unauthorized
update_id = None
# update_id =751829615
import sys
from time import sleep
import logging
import subprocess
BotToken = "1316484604:AAGQAmFLWe19zTt4XYP--1e7Q52X6kL7NWE"
import Transcription as tp

def voice(text_data):
    import os
    import uuid
    audio_name= str(uuid.uuid1())
    #espeak -v female3  -g 01ms -a 10 -p 45 -s 130
    #espeak -ven+f4 -s150

    s = "espeak -v female3  -g 01ms -a 10 -p 45 -s 130 '{}' --stdout > '{}'.mp3".format(text_data,audio_name)
    
    os.system(s)
    
    return audio_name



def TelegramMain():
	"""Run the bot."""
	global update_id
	# Telegram Bot Authorization Token
	bot = telegram.Bot(BotToken)
	bot1 = telebot.TeleBot(BotToken)

	# get the first pending update_id, this is so we can skip over it in case
	# we get an "Unauthorized" exception.
	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	while True:
		try:
			echo(bot,bot1)
		except NetworkError:
			sleep(1)
		except Unauthorized:
			# The user has removed or blocked the bot.
			update_id += 1

def log(message):
	print(message)
	sys.stdout.flush()

			
def echo(bot,bot1):
	''' Function to actually fetch messages from user and send back reply. Bot Token is reqired to run this script'''
	# Request updates after the last update_id
	global update_id
	for update in bot.get_updates(offset=update_id, timeout=10):
		update_id = update.update_id + 1
		try:	
			chat_id = update.message.chat.id
			
			dialogue_manager = DialogueManager(RESOURCE_PATH) #prediction call here
		
			if update.message.voice :
				file_id = bot1.get_file(update.message.voice.file_id)

				file_info=bot1.get_file(update.message.voice.file_id)
				downloaded_file = bot1.download_file(file_info.file_path)
				with open('new_file.ogg', 'wb') as new_file:
	    				new_file.write(downloaded_file)
				src_filename = 'new_file.ogg'
				dest_filename = 'output.wav'
				process = subprocess.run(['ffmpeg','-y' ,'-i', src_filename, dest_filename])
				if process.returncode != 0:
				    raise Exception("Something went wrong")
				print ("\n Request")
				tp.audio_text()
				msg=""
				with open('Results/output.txt', 'r') as reader:
					msg+=reader.read()
				answer=dialogue_manager.generate_answer(msg)
				answer = "You said :" + msg + "\n" + answer
				#log(update.message.voice.file_id)
				
				log(update.message)
			else:
				log(update.message) 		
				msg = update.message.text
				answer=dialogue_manager.generate_answer(msg)
				
			f1 = open("Results/data.txt", "a")
			f1.write(msg)
			f1.close()	
			#voice()				
			#s = voice(text_data) + ".mp3"
			bot.send_message(chat_id=chat_id, text = answer )
			
			#bot.send_audio(chat_id=chat_id, audio=open(s, 'rb'))
			
			#bot.send_message(chat_id=chat_id, text = "\U0001F973 " + voice(text_data))
		except Exception as e:
			print ("ERROR - CHAT ID-", e)
			#log(update.message)
			
			
		
if __name__ == '__main__':
	TelegramMain()
	#question="how to install pycharm"
	#dialogue_manager = DialogueManager(RESOURCE_PATH)
	#answer=dialogue_manager.generate_answer(msg)
	#print(answer)

