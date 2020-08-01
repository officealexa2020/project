# Jarvis
## Introduction 

Developing a conversational Chatbot to assist user with programming queries on StackOverflow using Speech to text, Text to speech algorithms for better user interactions.
 We have integrated the Chatbot with Telegram messenger @Jarvis_Sih_Chat_Bot
***Data description for queries on StackOverflow***
•	tagged_posts.tsv — StackOverflow posts, tagged with one programming language (positive samples).
•	dialogues.tsv — dialogue phrases from movie subtitles (negative samples).
•	word_embeddings.tsv — word embeddings trained earlier with StarSpace on StackOverflow query data earlier.

***Models Description***

TF-IDF is used for training of the model
Steps for execution of Chat Bot on Telegram 

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
Run the main.py 
python main.py
Following can be used to visualize the code  log.
TelegramBot = telepot.Bot(token)
print( TelegramBot.getMe()) 
TelegramBot.getUpdates()

***The following steps makes the code run without the telegram dependency.***

Uncomment the following last 4 lines in main.py
#question="how to install pycharm"

#dialogue_manager = DialogueManager(RESOURCE_PATH)

#answer=dialogue_manager.generate_answer(msg)

#print(answer)
Commenting 5th last line in main.py
 TelegramMain()

Transcription.py has the Speech-to -text implementation

