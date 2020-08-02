import pprint
from wit import Wit

from atlassian import Jira
 
import requests
 
from jira import JIRA
 

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
    
atlassian.set_issue_status("JARVIS-10", "TO DO")


client = Wit('5PA2VEZ7QB7BPVDMXNSY2W3VYPSLT3H6')
user_query = input("Enter the query ")
resp = client.message(user_query) 

#atlassian.set_issue_status("JARVIS-10", "in progress")
pprint.pprint(resp) 
 
 
def update_issue():

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






def create_issue():
	
	
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
	    




def get_issue_information(v):


	
	
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




try:
	if (resp['intents'][0]['name']=="update_issue"):
		up = update_issue()
		print(up)

	if (resp['intents'][0]['name']=="create_new_issue"):
		create_issue()
	
	if (resp['intents'][0]['name']=="issue_get_information"):
		info = get_issue_information(1)
		print (info)
	
	if (resp['intents'][0]['name']=="issue_details"):
		info1 = get_issue_information(0)
		print (info1)
		
except Exception as e:

	if str(e)=="list index out of range":
		print("Intent is not clear")
	else:
		print (e) 
