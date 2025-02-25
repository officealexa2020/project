# SIH 2020 Team Shunya
## Problem statement SM446: Jarvis
## Introduction 

Developed a conversational Chatbot based on Al/ML application to be hosted within a corporate/organization intranet with complete access to corporate/organization resources like JIRA. Confluence. bitbucket, custom web resources, CRM, SAP, etc. Developed an algorithm to assist user with programming queries on StackOverflow using Speech to text and Text to speech algorithms for better user interactions.

 We have integrated the Chatbot with Telegram messenger @Jarvis_Sih_Chat_Bot
 
 ## Architecture Diagram
 
 ![arch2](https://user-images.githubusercontent.com/68907952/89173364-c5034c00-d5a1-11ea-982a-26040abb2a08.png)



***Steps***

- The input from the user can be taken in the form of text or voice input.

- In case of voice the input is converted to text using google api Speech_Recognition.

- The text is fetched to intent classification to understand the user request.
- Here it is classified into stackOverflow query, MOM, task related to JIRA, Confluence. Further classified into kind of task like fetching data, or issue creation, etc.
- Once the intent is recognized the particular function is executed to perform the task.
- If needed the result is converted to speech using espeak function.
- Lastly the output is fetched in summarized form. 

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



## Deployment 
***Steps for execution of Chat Bot on Telegram***

***Creating a Telegram Bot***

First of all in order to create a telegram bot you have to have a Telegram account. If you do, then go ahead and open your telegram app (mobile or desktop) and follow the steps:

•	Add to your contact list BotFather

•	Start a conversation with BotFather by clicking Start button. You will see a command list immediately.

•	In order to create a new telegram bot, you have to type /newbot command and follow the instructions. Be careful, your bot's username has to end with bot. For example, DjangoBot or Django_bot.

•	I decided to choose PlanetPythonBot, which is pretty straightforward considering its functionality.
  
If everything is okay, you will see bot's token or API access key at the end.


![tele2](https://user-images.githubusercontent.com/68907952/89154895-67610680-d585-11ea-94d4-51e985dc6bdf.png)
![tele](https://user-images.githubusercontent.com/68907952/89154844-53b5a000-d585-11ea-84b7-7d9ea03e59ce.png)

 BotFather is also able to perform following actions for you:

•	Put description to your bot

•	Upload avatar

•	Change access token

•	Delete your bot etc.


## Installation guide:

***Run the following commands on terminal***

pip3 install -r requirements.txt

This will install all the dependencies which are required for the project.

you can also use dockerfile to make the needed environment.



you also need to run a StandNLU server for this you can refer:
https://github.com/stanfordnlp/python-stanford-corenlp

How to run the server you can refer this link :
https://stackoverflow.com/questions/32879532/stanford-nlp-for-python

Download link:

https://stanfordnlp.github.io/CoreNLP/

This help to annotate the sentence given by user , for more details you can refer offical link or github link given above.The server will run locally on 9000 port which will be directly accessed by script annotate_ws.py

***Execution***

python3 jarvis_telegram.py 

This will make your book uprunning on telegram server and send you databack.If you want to use telegram you need a key , for that you can refer Deployment given above.  

OR

python3 jarvis_egmail.py

This will talk with STMP gmail server to get all the recent emails and send back reqrested data.



***Following can be used to visualize the code log.***

TelegramBot = telepot.Bot(token)

print( TelegramBot.getMe()) 

TelegramBot.getUpdates()



***Speech-to-text implementation is done in Transcription.py.***

This uses google speech-to-text API , you can refer this link on how to use it : https://realpython.com/python-speech-recognition/


***Text-to-speech is integrated inside the jarvis_telegram.py file***

# Results

![result](https://user-images.githubusercontent.com/68907952/89162011-0f300180-d591-11ea-86de-567bd190a4e7.png)


![res3](https://user-images.githubusercontent.com/68907952/89174104-f2042e80-d5a2-11ea-96f5-d74c71944c37.png)

# Theory
The input from the user can be taken in the fom of 

## Intent classification

Inherently linked to Natural Language Processing (NLP), intent classification automatically finds purpose and goals in text

Example “What’s the status Of my delivery”
Classification automatically categorize it as a clear  delivery status intent.

***BIO scheme for intent classifiaction***

***working***

what we actually get from user is random words.
The first thing you need to do when you get the utterance from the user,
is you need to understand what does the user want,
You should think of it as the following,
which predefined scenario is the user trying to execute?

***Let's look at this Siri example,***
"How long to drive to the nearest Starbucks?",
I asked Siri and the Siri tells me the result.
"The traffic to Starbucks is about average so it should take approximately ten minutes."
And I had such an intent,
I wanted to know how long to drive to the nearest Starbucks and we can
mark it up as the intent: navigation.time.closest.
So, that means that I am interested about time of navigation to the closest thing.
And I can actually ask it in any other way and
because our natural language has a lot of options for that.
But it will still need to understand that this is the same intent.
Okay. So, I can actually ask the Siri a different question,

Example

"Give me directions to Starbucks."

Now, the system doesn't know which Starbucks I want.
And that's when this system initiate the dialogue with
me and because it needs additional information like which Starbucks.
And this is intent: navigation.directions.
And how to think about this dialogue and how our chat bot,
a personal assistant actually tracks what we are saying to it.

***You should think of intent as actually a form that a user needs to fill in.***
Each intent has a set of fields or
so-called slots that must be filled in to execute the user request.
Let's look at the example intent like navigation.directions.

So that the system can build the directions for us,
it needs to know where we want to go and from where we want to go.
So, let's say we have two slots here like FROM and TO,
and the FROM slot is actually optional because
it can default to current geolocation of the user.
And TO slot is required,
we cannot build directions for you if you don't say where you want to go.
And we need a slot tagger to extract slots from the user utterance.
Whenever we get the utterance from the user,
we need to know what slots are there and what intent is there.
And let's look at slot filling example.
The user says, "Show me the way to History Museum."
And what we expect from our slot tagger is to highlight that History Museum part,
and tell us that History Museum is actually a value of a TO slot in our form.
And you should think of it as a sequence tagging and let me
remind you that we solve sequence tagging tasks using 

***BIO Scheme coding.***
Here,

B corresponds to the word of the beginning of the slot,

I corresponds to the word inside the slot,

O corresponds to all other words that are outside of slots.

Example1:

***"Show me the way to History Museum."***
the text that we want to produce for each token are actually the following,
"Show me the way to" are outside of any slots,
that's why they have O,
"History" is actually the beginning of slot TO,
and "Museum" is the inside token in the slot TO,
so that's why it gets that tag.
You train it as a sequence tagging task in BIO scheme and we
have overview that in sequence to sequence in previous week.
Let's say that a slot is considered to be correct if it's range and type are correct.
And then, we can actually calculate
the following metrics: we can calculate the recall of our slot tagging,
we can take all the two slots and find out
which of them are actually correctly found by our system,
and that's how we define a recall.
The precision is the following would take all of
found slots and we find out which of them are correctly classified slots.
And you can actually evaluate your slot tagger with F1 measure,
which is a harmonic mean of precision and recall that we have defined.
Okay. So, let's see how form filling dialog manager can work in a single turn scenario. 


![pic2](https://user-images.githubusercontent.com/68907952/89122101-3b407980-d4e2-11ea-9dcb-562eca449f47.png)


***Referances***


https://stanfordnlp.github.io/CoreNLP/
https://realpython.com/python-speech-recognition/
https://stackoverflow.com/questions/32879532/stanford-nlp-for-python



***Project by***
***Team- Shunya***

***College- MIT Academy OF Engineering***

***Team members:***

***Prajwal Chirde, 
 Namrata Kumar, 
 Rushikesh Bhadage, 
 Shubham Joshi, 
 Tejas Dhakad, 
 Suprit Gaikwad,***




