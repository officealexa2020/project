import pprint
from wit import Wit

from atlassian import Jira
 
import requests
 
from jira import JIRA


import imaplib
import email

import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time







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



requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
 
options = {
 
        'server':'https://jarvis2.atlassian.net',
 
        'verify':False
 
    }
 
  
jir = JIRA(options, basic_auth=('pvczero@gmail.com', '48GCD07xfciUeR2n2qLj2C03'))
 
 
atlassian = Jira(
 
    url='https://jarvis2.atlassian.net',
 
    username='pvczero@gmail.com',
 
    password='48GCD07xfciUeR2n2qLj2C03')


client = Wit('5PA2VEZ7QB7BPVDMXNSY2W3VYPSLT3H6')


















def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def read_email_from_gmail(name):
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('officealexa2020@gmail.com','Sih@2020')
	mail.select('inbox')
	name = "(FROM " + '"'+ name + '")' 
	result, data = mail.search(None, name)
	mail_ids = data[0]
	print(mail_ids)

	id_list = mail_ids.split()
	recent_mail=int(id_list[-1])   
	#print(mail_ids)
	result, data = mail.fetch(str(recent_mail), '(RFC822)' )

	for response_part in data:
		if isinstance(response_part, tuple):
			msg = email.message_from_bytes(response_part[1])
			email_subject = msg['subject']
			email_from = msg['from']
			print ('From : ' + email_from + '\n')
			print ('Subject : ' + email_subject + '\n')
			print('Body',str(get_text(msg).decode('utf')))

def read_unseen_email_from_gmail(name):
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('officealexa2020@gmail.com','Sih@2020')
	mail.select('inbox')
	name = "(FROM " + '"'+ name + '")' 
	
	result, data = mail.search(None,'(UNSEEN)', name)
	mail_ids = data[0]
	print(mail_ids)
	
	
	id_list = mail_ids.split()
	recent_mail=int(id_list[-1])   
	#print(mail_ids)
	result, data = mail.fetch(str(recent_mail), '(RFC822)' )

	for response_part in data:
		if isinstance(response_part, tuple):
			msg = email.message_from_bytes(response_part[1])
			email_subject = msg['subject']
			email_from = msg['from']
			print ('From : ' + email_from + '\n')
			print ('Subject : ' + email_subject + '\n')
			print('Body',str(get_text(msg).decode('utf')))

		

def read_all_unseen_email():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('officealexa2020@gmail.com','Sih@2020')
	mail.select('inbox')
	#name = "(FROM " + '"'+ name + '")' 
	while 1:
		mail.select('inbox')
		result, data = mail.search(None,'(UNSEEN)')
		mail_ids = data[0].decode('utf')
		#print(mail_ids)
		id_list = mail_ids.split()
		#print("s",id_list)
	
	
		
		if id_list:
			print("got a  mail")
			for i in range(len(id_list)):
				recent_mail=int(id_list[i])   
				#print(mail_ids)
				result, data = mail.fetch(str(recent_mail), '(RFC822)' )

				for response_part in data:
					if isinstance(response_part, tuple):
						msg = email.message_from_bytes(response_part[1])
						email_subject = msg['subject']
						email_from = msg['from']
						body = str(get_text(msg).decode('utf'))
						print ('From : ' + email_from + '\n')
						print ('Subject : ' + email_subject + '\n')
						#print('Body',body)
						sep='<'
						rest = body.split(sep, 1)[0]
						sep='On'
						body = rest.split(sep, 1)[0]
						print("body :",body)
						resp = client.message(body) 
						
								
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
								answer=str(dialogue_manager.generate_answer(msg))
								answer = str("You said :" + msg + "\n" + answer)
							if (resp['intents'][0]['name']=="database"):
								print("in database")	
								answer=str(main_work(body))				
											
						except Exception as e:

							if str(e)=="list index out of range":
								answer="Intent is not clear"
							else:
								answer=e

						senderemail=email_from.split('<')[1].split('>')[0]
						print("saihcias",answer)
						send_email(answer,senderemail)
						
				for e_id in id_list:
					mail.store(e_id, '+FLAGS', '\Seen')
			time.sleep(5)
		else:	
			print("No recent mail")
			time.sleep(5)



def send_email(body,senderemail):
	subject = "HI , this is jarvis your AI"
	#body = "This is an email with attachment sent from Python"
	sender_email = "officealexa2020@gmail.com"
	receiver_email = senderemail
	password = "Sih@2020"
	# Create a multipart message and set headers
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
	message["Bcc"] = receiver_email  # Recommended for mass emails

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	#filename = "document.pdf"  # In same directory as script

	# Open PDF file in binary mode
	#with open(filename, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
	    #part = MIMEBase("application", "octet-stream")
	    #part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	#encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	#part.add_header(
	   # "Content-Disposition",
	   # f"attachment; filename= {filename}",
	#)

	# Add attachment to message and convert message to string
	#message.attach(part)
	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, text)
				
read_all_unseen_email()

			

