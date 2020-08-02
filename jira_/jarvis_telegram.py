import pprint
from wit import Wit

from atlassian import Jira
 
import requests
 
from jira import JIRA
 

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











requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
 
options = {
 
        'server':'https://jarvis2.atlassian.net',
 
        'verify':False
 
    }
 

client = Wit('5PA2VEZ7QB7BPVDMXNSY2W3VYPSLT3H6')






jir = JIRA(options, basic_auth=('pvczero@gmail.com', '48GCD07xfciUeR2n2qLj2C03'))
 
 
atlassian = Jira(
    url='https://jarvis2.atlassian.net',
    username='pvczero@gmail.com',
    password='48GCD07xfciUeR2n2qLj2C03')




def voice(text_data):
    import os
    import uuid
    audio_name= str(uuid.uuid1())
    #espeak -v female3  -g 01ms -a 10 -p 45 -s 130
    #espeak -ven+f4 -s150

    s = "espeak -v female3  -g 01ms -a 10 -p 45 -s 130 '{}' --stdout > '{}'.mp3".format(text_data,audio_name)
    
    os.system(s)
    
    return audio_name

 
def update_issue(resp):

	try:

		En = "entities"
	
	
		
		j="issue_name:issue_name"	
		if resp[En][j]:
		
			i_name= resp[En][j][0]['value']
		
			if "issue" in i_name:
				i_name= i_name.replace("issue ","")	
	
			
	
	
		for j in resp[En]:
		
			if j=="project_name:project_name":	
			#if resp[En][j]:
		
				p_name= resp[En][j][0]['value']
		
				if "project" in p_name:
					p_name= p_name.replace("project ","")
				
				

			if j=="update_status:update_status":
			#if resp[En][j]:
		
				u_stat= resp[En][j][0]['value']
		
				print (u_stat)
				print (i_name)
				
				if u_stat=="To-Do":
					u_stat="To Do"
					
				if u_stat=="in-progress":
					u_stat="in progress"				
				
				atlassian.set_issue_status(i_name,u_stat)
			
				
		
		

			if j=="update_priority:update_priority":	
			#if resp[En][j]:
		
				u_prio= resp[En][j][0]['value']
		
				atlassian.issue_update(issue_key= i_name, fields={

				'priority': {'name': u_prio}

				})
			
				print (u_prio)
	
			if j=="issue_type:issue_type":	
			#if resp[En][j]:
		
				u_type= resp[En][j][0]['value']
		
				atlassian.issue_update(issue_key= i_name, fields={

				'issuetype': { "name": u_type}

				})	
			
				print (u_type)	
	
			if j=="issue_summary:issue_summary":
			#if resp[En][j]:
			
				u_sum= resp[En][j][0]['value']
		
				atlassian.issue_update(issue_key= i_name, fields={

					'summary': u_sum 

				})
			
				print (u_sum)
		
		ans="update done as per stated in the issue " + i_name
		return (ans)
		
	except Exception as e:
		
		
		ans="I think you have missed something or made a mistake for values please try again " + "\n Error - "
		return (e)






def create_issue(resp):
	
	
	i_sum= "default"
	p_name="wrong"
	i_type="not"

	i="entities"
	
	try:	
	
		
		for j in resp[i]:
	
			if j=="issue_summary:issue_summary":
		
				i_sum= resp[i][j][0]['value']
	
			if j=="issue_type:issue_type":
		
				i_type= resp[i][j][0]['value']
	
			if j=="project_name:project_name":
		
				p_name= resp[i][j][0]['value']
				p_name= p_name.replace("project ","")
			
		
		print (i_sum)
	 
		print (i_type)
	 	
		print (p_name)
	 
		atlassian.issue_create(fields={
	 
		    'project': {'key': p_name },
	 
		    'issuetype': {
	 
		    'name': i_type
	 
		    },
	 
		    'summary': i_sum,
	 
		    'description': 'nahi ahe ',
	 
		})
		
		ans = "yeah sure anything for you ! created the issue "
		
		return ans
    
	except Exception as e:
	
		print (e)
		#ans="update can not be done please review your request " + "\n Error - " + e
		return e
	    




def get_issue_information(resp,v):


	
	
	try:
	
		try:
			i_name=resp['entities']['issue_name:issue_name'][0]['value']
		
			if "issue" in i_name:
					i_name= i_name.replace("issue ","")
		
	
			i = atlassian.issue(i_name)
		
		except:
		
			return ("issue name is not correct please try again ")
		
		
		ans="Thanks for asking your results are - \n"
		
		if (v):
			for j in resp['entities']:
		
				if j=="get_issue_creator:get_issue_creator":
			
					ans += "Creator Details -: name - " + i['fields']['creator']['displayName'] 
					
					ans += " email -" + (i['fields']['creator']['emailAddress']) + "\n"

				if j=="get_issue_type:get_issue_type":
			 	
			 		ans += "issue type - " +i['fields']['issuetype']['name'] + "\n"
			 		
				if j=="get_issue_description:get_issue_description":
			 		ans += "issue description - " + i['fields']['issuetype']['description'] + "\n"
			 			
				if j=="get_issue_subtask:get_issue_subtask":
					ans += "issue subtask - " + i['fields']['issuetype']['subtask'] + "\n"
			
				if j=="get_issue_labels:get_issue_labels":
					ans += "issue labels - "  + str(i['fields']['labels']) + "\n"
			
				if j=="get_issue_priority:get_issue_priority":
					ans += "issue priority - " + i['fields']['priority']['name'] + "\n"
			
				if j=="get_issue_project:get_issue_project":
					ans += "issue project - " + i['fields']['project']['key'] + "\n"
			
				if j=="get_issue_reporter:get_issue_reporter":
					ans += "issue reporter - " + i['fields']['reporter']['displayName'] + "\n"
			
				if j=="get_issue_status:get_issue_status":
					ans += "issue status - " + i['fields']['status']['name'] + "\n"
			
				if j=="get_issue_summary:get_issue_summary":
					ans += "issue summary - " + i['fields']['summary'] + "\n"
	
			return ans
			
		else:
			
		
			ans += "issue project - " + i['fields']['project']['key'] + "\n"
			ans += "Creator Details -: name - " + i['fields']['creator']['displayName'] 
			ans += " email -" + (i['fields']['creator']['emailAddress']) + "\n"
			ans += "issue status - " + i['fields']['status']['name'] + "\n"
			ans += "issue type - " +i['fields']['issuetype']['name'] + "\n"
			ans += "issue priority - " + i['fields']['priority']['name'] + "\n"
			ans += "issue summary - " + i['fields']['summary'] + "\n"
			
			
			return ans
			
		
		
			
		 	
	except Exception as e:
		 	
		return (e)

	    
		
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
			if update.message.voice :
				file_id = bot1.get_file(update.message.voice.file_id)
				#file_unique_id = update.message.voice.file_unique_id
				#duration = update.message.voice.duration
				#download=telegram.Audio(file_id,file_unique_id,duration)
				#print("sssssssss",download)
				
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
				

				user_query = msg

				resp = client.message(user_query) 

				  

				pprint.pprint(resp)

				try:
					if (resp['intents'][0]['name']=="update_issue"):
						up = update_issue(resp)
						print(up)
						answer=up
						

					if (resp['intents'][0]['name']=="create_new_issue"):
						answer=create_issue(resp)
					
					if (resp['intents'][0]['name']=="issue_get_information"):
						info = get_issue_information(resp,1)
						print (info)
						answer=info
					
					if (resp['intents'][0]['name']=="issue_details"):
						info1 = get_issue_information(resp,0)
						print (info1)
						answer=info1
						
				except Exception as e:

					if str(e)=="list index out of range":
						answer="Intent is not clear"
					else:
						answer=e
				 

				#log(update.message.voice.file_id)
				log(update.message)
			else:
				log(update.message) 		
				msg = update.message.text
				
				user_query= msg
				resp = client.message(user_query) 

				  

				pprint.pprint(resp)
				try:
					if (resp['intents'][0]['name']=="update_issue"):
						up = update_issue(resp)
						print(up)
						answer=up
						

					if (resp['intents'][0]['name']=="create_new_issue"):
						answer=create_issue(resp)
					
					if (resp['intents'][0]['name']=="issue_get_information"):
						info = get_issue_information(resp,1)
						print (info)
						answer=info
					
					if (resp['intents'][0]['name']=="issue_details"):
						info1 = get_issue_information(resp,0)
						print (info1)
						answer=info1
						
				except Exception as e:

					if str(e)=="list index out of range":
						answer="Intent is not clear"
					else:
						answer=e
				 
						
						
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


