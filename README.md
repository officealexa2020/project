# Team Shunya
# Jarvis
## Introduction 

Developing a conversational Chatbot based on Al/ML application to be host within a corporate/organization intranet with complete access to corporate/organization resources like JIRA. Confluence. bitbucket, custom web resources, CRM, SAP, etc. Deeveloped an algorithm to assist user with programming queries on StackOverflow using Speech to text, Text to speech algorithms for better user interactions.

 We have integrated the Chatbot with Telegram messenger @Jarvis_Sih_Chat_Bot
 
 ## Architecture


[
![pic1](https://user-images.githubusercontent.com/68907952/89121804-de43c400-d4df-11ea-92bc-410072679d19.png)
](url)



 ## Input Output Interface
 
 ![pic5](https://user-images.githubusercontent.com/68907952/89122104-3f6c9700-d4e2-11ea-81d5-3f127c139f96.png)
 
 ## Component diagram
 ![pic4](https://user-images.githubusercontent.com/68907952/89122090-29f76d00-d4e2-11ea-916a-4f59b1613bad.png)
 
***Data description for queries on StackOverflow***

•	tagged_posts.tsv — StackOverflow posts, tagged with one programming language (positive samples).

•	dialogues.tsv — dialogue phrases from movie subtitles (negative samples).

•	word_embeddings.tsv — word embeddings trained earlier with StarSpace on StackOverflow query data earlier.


***Models Description***

TF-IDF is used for training of the model

## Steps for execution of Chat Bot on Telegram ##

***Creating a Telegram Bot***

First of all in order to create a telegram bot you have to have a Telegram account. If you do, then go ahead and open your telegram app (mobile or desktop) and follow the steps:

•	Add to your contact list BotFather

•	Start a conversation with BotFather by clicking Start button. You will see a command list immediately.

•	In order to create a new telegram bot, you have to type /newbot command and follow the instructions. Be careful, your bot's username has to end with bot. For example, DjangoBot or Django_bot.

•	I decided to choose PlanetPythonBot, which is pretty straightforward considering its functionality.
  
If everything is okay, you will see bot's token or API access key at the end.
 
By the way, BotFather is also able to perform following actions for you:

•	Put description to your bot

•	Upload avatar

•	Change access token

•	Delete your bot etc.


***Do the following installations:***

pip install telepot

pip install telegram or git clone https://github.com/python-telegram-bot/python-telegram-bot 

Sudo apt-get install espeak

pip install SpeechRecognition

***Run the main.py***

***python main.py***

Following can be used to visualize the code  log.
TelegramBot = telepot.Bot(token)
print( TelegramBot.getMe()) 
TelegramBot.getUpdates()

***The following steps makes the code run without the telegram dependency.***

***Uncomment the following last 4 lines in main.py***
#question="how to install pycharm"

#dialogue_manager = DialogueManager(RESOURCE_PATH)

#answer=dialogue_manager.generate_answer(msg)

#print(answer)

***Commenting 5th last line in main.py***

 TelegramMain()
 

***Speech-to-text implementation is done Transcription.py.***

***Text-to-speech is integrated inside the main.py file***

##Intent classification

Inherently linked to Natural Language Processing (NLP), intent classification automatically finds purpose and goals in text

“Hi, I’m a photographer and work with a significant amount of raw files. What kind of storage do you offer? Is it a lifetime membership? For the right price, I’d love to purchase cloud storage.”

With an intent classifier, you could easily locate this query among the numerous user interactions you receive on a daily basis, and automatically categorize it as a clear Purchase intent.
***BIO scheme for intent classifiaction***

![pic2](https://user-images.githubusercontent.com/68907952/89122101-3b407980-d4e2-11ea-9dcb-562eca449f47.png)

***Project by***
***Team- Shunya***

***College- MIT Academy OF Engineering***

***Team members:***

Prajwal Chirde 
Namrata Kumar
Rushikesh Bhadage
Shubham Joshi
Tejas Dhakad
Suprit Gaikwad




