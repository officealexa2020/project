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
								
						except Exception as e:

							if str(e)=="list index out of range":
								answer="Intent is not clear"
							else:
								answer=e

						senderemail=email_from.split('<')[1].split('>')[0]
						
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

			

