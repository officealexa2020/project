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



from requests.compat import urljoin

from stackoverflow.utils import *
from stackoverflow.dialogue_manager import DialogueManager




import argparse, os
from sqlnet.dbengine import DBEngine
from sqlova.utils.utils_wikisql import *
from train import construct_hyper_param, get_models


import argparse, csv, json

from sqlalchemy import Column, create_engine, Integer, MetaData, String, Table
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, mapper

import subprocess



import sqlite3
from sqlite3 import Error




import telegram

from telegram.error import NetworkError, Unauthorized
update_id = None
# update_id =751829615
import sys
from time import sleep
import logging
import re



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_filewh
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        

    return conn

def select_all_tasks(conn,sqlquery):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
  
    cur = conn.cursor()
    try:
    	cur.execute(sqlquery)
    except Error as e:
    	print(e)
    	return ("I didn't get you. Please be more specific and try again")
    	
    rows = cur.fetchall()
    #rows=re.sub(r'\W', '', rows)
    print(rows)
    if rows == None:
    	return ("I didn't get you. Please be more specific and try again")
    		
    return rows
        
        
        
        
        
def question_to_json(table_id, question, json_file_name):
    record = {
        'phase': 1,
        'table_id': table_id,
        'question': question,
        'sql': {'sel': 0, 'conds': [], 'agg': 0}
    }
    print(record)
    with open(json_file_name, 'wt') as fout:
        json.dump(record, fout)
        fout.write('\n')





def predict(data_loader, data_table, model, model_bert, bert_config, tokenizer,
            max_seq_length,
            num_target_layers, detail=False, st_pos=0, cnt_tot=1, EG=False, beam_size=4,
            path_db=None, dset_name='test'):

    model.eval()
    model_bert.eval()

    engine = DBEngine(os.path.join(path_db, f"{dset_name}.db"))
    results = []
    for iB, t in enumerate(data_loader):
        #print(t)
        nlu, nlu_t, sql_i, sql_q, sql_t, tb, hs_t, hds = get_fields(t, data_table, no_hs_t=True, no_sql_t=True)
        
        
        g_sc, g_sa, g_wn, g_wc, g_wo, g_wv = get_g(sql_i)
        
        g_wvi_corenlp = get_g_wvi_corenlp(t)
        wemb_n, wemb_h, l_n, l_hpu, l_hs, \
        nlu_tt, t_to_tt_idx, tt_to_t_idx \
            = get_wemb_bert(bert_config, model_bert, tokenizer, nlu_t, hds, max_seq_length,
                            num_out_layers_n=num_target_layers, num_out_layers_h=num_target_layers)
        if not EG:
            # No Execution guided decoding
            s_sc, s_sa, s_wn, s_wc, s_wo, s_wv = model(wemb_n, l_n, wemb_h, l_hpu, l_hs)
            pr_sc, pr_sa, pr_wn, pr_wc, pr_wo, pr_wvi = pred_sw_se(s_sc, s_sa, s_wn, s_wc, s_wo, s_wv, )
            pr_wv_str, pr_wv_str_wp = convert_pr_wvi_to_string(pr_wvi, nlu_t, nlu_tt, tt_to_t_idx, nlu)
            pr_sql_i = generate_sql_i(pr_sc, pr_sa, pr_wn, pr_wc, pr_wo, pr_wv_str, nlu)
        else:
            # Execution guided decoding
            prob_sca, prob_w, prob_wn_w, pr_sc, pr_sa, pr_wn, pr_sql_i = model.beam_forward(wemb_n, l_n, wemb_h, l_hpu,
                                                                                            l_hs, engine, tb,
                                                                                            nlu_t, nlu_tt,
                                                                                            tt_to_t_idx, nlu,
                                                                                            beam_size=beam_size)
            # sort and generate
            pr_wc, pr_wo, pr_wv, pr_sql_i = sort_and_generate_pr_w(pr_sql_i)
            # Following variables are just for consistency with no-EG case.
            pr_wvi = None # not used
            pr_wv_str=None
            pr_wv_str_wp=None

        pr_sql_q = generate_sql_q(pr_sql_i, tb)
        #print(pr_sql_i)

        for b, (pr_sql_i1, pr_sql_q1) in enumerate(zip(pr_sql_i, pr_sql_q)):
            results1 = {}
            results1["query"] = pr_sql_i1
            
            results1["table_id"] = tb[b]["id"]
            results1["nlu"] = nlu[b]
            results1["sql"] = pr_sql_q1
            results.append(results1)
            #print(b)

    return results

## Set up hyper parameters and paths
parser = argparse.ArgumentParser()

args = construct_hyper_param(parser)

BERT_PT_PATH = "annotated_wikisql_and_PyTorch_bert_param"


path_save_for_evaluation = "result"
split="playground"
data_path = "data_and_model"




# Load pre-trained models
path_model_bert = "model_bert_best.pt"
path_model = "model_best.pt" 
args.no_pretraining = True  # counterintuitive, but avoids loading unused models
model, model_bert, tokenizer, bert_config = get_models(args, BERT_PT_PATH, trained=True, path_model_bert=path_model_bert, path_model=path_model)



#connection to db

db_file=r"data_and_model/playground.db"
conn=create_connection(db_file)



def main_work(question):
		
	
	
	din="data_and_model"
	table_id="company"
	#"what state has iso us"
	json_file_name = os.path.join(din, split)+'.jsonl'

	question_to_json(table_id,question, json_file_name)
	print("Added question (with dummy label) to {}".format(json_file_name))

	command = 'python3 annotate_ws.py '

	subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)




	# Load data
	dev_data, dev_table = load_wikisql_data(data_path, mode=split, toy_model=args.toy_model, toy_size=args.toy_size, no_hs_tok=True)
	dev_loader = torch.utils.data.DataLoader(
	    batch_size=args.bS,
	    dataset=dev_data,
	    shuffle=False,
	    num_workers=1,
	    collate_fn=lambda x: x  # now dictionary values are not merged!
	)







	#print("dev_loader",dev_loader)
	# Run prediction
	with torch.no_grad():
	    results = predict(dev_loader,
			      dev_table,
			      model,
			      model_bert,
			      bert_config,
			      tokenizer,
			      args.max_seq_length,
			      args.num_target_layers,
			      detail=False,
			      path_db=data_path,
			      st_pos=0,
			      dset_name=split, EG=args.EG)

	# Save results
	
	sqlquery=str(results[0]['sql'])
	
	a=sqlquery.split(' ')
	for i in range(len(a)):
		if a[i] == "=" :
			a[i+1] = '"'+a[i+1]+'"'
	sqlquery=" ".join(a)
	
	print(sqlquery)
	
	
	
	answer = select_all_tasks(conn,sqlquery)  
	#save_for_evaluation(path_save_for_evaluation, results, split)
	#answer = 'sql query :' + str(sqlquery) + '\n Data fetched from database :' + answer
	print(answer)
	return answer
		
		






















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
			print(i_name)		
			if "-" not in i_name:
				i_name= i_name.replace(" ","-")
				print(i_name)

	
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
					if (resp['intents'][0]['name']=="stackoverflow"):
						dialogue_manager = DialogueManager(RESOURCE_PATH)
						answer=dialogue_manager.generate_answer(msg)
						answer = "You said :" + msg + "\n" + answer
					if (resp['intents'][0]['name']=="database"):
						print("in database")	
						answer=main_work(msg)							
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
					if (resp['intents'][0]['name']=="stackoverflow"):
						dialogue_manager = DialogueManager(RESOURCE_PATH)
						answer=dialogue_manager.generate_answer(msg)
						answer = "You said :" + msg + "\n" + answer
					if (resp['intents'][0]['name']=="database"):
						print("in database")	
						answer=main_work(msg)
						
						print(answer)										
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


