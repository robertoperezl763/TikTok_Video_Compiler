import os
from dotenv import load_dotenv
from groq import Groq
from google.cloud import texttospeech

from app.google_api import createAudio
from app.groq_api import getPrompt, getSubtitles
from app.video_edit import generateFinalVideo
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

#prompt for groq chat api
prompt = "in no more than 25 words, Explain the importance of fast language models"

#get script from groq chat API - returns str value with script
script = getPrompt(client_obj=groqClient, 
                   content=prompt)


#Create Audio file from script using Google TTS API - returns audio file location
audioFileLoc = createAudio(client=googleClient, 
                           prompt=script, 
                           outputFileName='test3')

#get subtitles file from Groq speech -> text API
#returns subtitle file location
subtitleFileLoc = getSubtitles(client=groqClient,
                               audioInputFile=audioFileLoc,
                               srtOutputFileName="test3")


finalVidLoc = generateFinalVideo(subtitleFileLoc=subtitleFileLoc,
                   audioFileLoc=audioFileLoc,
                   backgroundClipLoc="media/background_video/minecraft_short.mp4",
                   finalVideoName='TestFinalVideo3'
                   )

print(f'video saved at: {finalVidLoc}')
#get background video clip


#Generate subtitles video and merge with background video clip


#merge audio clip with video/subtitles




#youtube upload



#############
#automate filename structure rather than hard code
#############
