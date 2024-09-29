import os
from dotenv import load_dotenv
from groq import Groq
from google.cloud import texttospeech

from app.google_api import createAudio
from app.groq_api import getPrompt, getSubtitles, write_file
from app.video_edit import generateFinalVideo
import uuid
import re

#load envirnment variables from .env file
load_dotenv(override=True)

#loads google api auth credentials into env.
os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

#start groq client
groqClient = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
#start GoogleAPI Client
googleClient = texttospeech.TextToSpeechClient()

#Generate videoId for all pieces of this video
videoID = str(uuid.uuid4())

#initiate required variables
prompt = "in no more than 175 words, generate a short and scary story that would translate well for a quick youtube video. this should not be repeated from previous api calls. Response should ONLY include the story and nothing else."
titleGenPrompt = "generate a short and concise title for a youtube video created based on the following script coming from a chat responce from a previous API call. Your answer should include nothing more than the provided title with no special characters. here is the script: "
sysPromptStory = "you are a brilliant horor story teller, and capable of creating short, captivating and immersing stories. Each Story should be unique and new"
sysPromptTitle = "write a short engaging and original title for this story"
max_words_for_subs = 3


#get script from groq chat API - returns str value with script
script = getPrompt(client_obj=groqClient, 
                   content=prompt,
                   sysPrompt=sysPromptStory,
                   temp=1.2)

videoTitle = getPrompt(client_obj=groqClient,
                  content=f"{titleGenPrompt} {script}",
                  sysPrompt=sysPromptTitle,
                  temp=0.8)

videoTitle = re.sub(r'[^A-Za-z0-9\s]','' ,videoTitle) #strip any special charactrs to avoid error on append title to final video name

fileData = videoTitle + "\n\n" + script

rawScriptFile = write_file(fileName=videoID, 
                           data=fileData, 
                           folderLoc="media/rawScript")
print(f"Script.txt File Created Siccessfully at: {rawScriptFile}")

#Create Audio file from script using Google TTS API - returns audio file location
audioFileLoc = createAudio(client=googleClient, 
                           prompt=script, 
                           outputFileName= videoID)
print(f"Audio File Created Successfully at: {audioFileLoc}")

#get subtitles file from Groq speech -> text API
#returns subtitle file location
subtitleFileLoc = getSubtitles(client=groqClient,
                               audioInputFile=audioFileLoc,
                               srtOutputFileName=videoID,
                               max_words=max_words_for_subs)

print(f"Subtitles File Created Successfully at: {subtitleFileLoc}")

# get background video clip
#Generate subtitles video and merge with background video clip
#merge audio clip with video/subtitles

finalVidLoc = generateFinalVideo(subtitleFileLoc=subtitleFileLoc,
                   audioFileLoc=audioFileLoc,
                   backgroundClipLoc="media/background_video/minecraft_30.mp4",
                   finalVideoName=f"{videoTitle}_{videoID}"
                   )

print(f'Final Video saved at: {finalVidLoc}')
