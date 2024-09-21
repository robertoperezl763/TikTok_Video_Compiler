import os
from groq import Groq
from datetime import timedelta

#call groq chatbot and return response from API based on user content prompt
def getPrompt(client_obj: Groq, content: str):
    
    chat_completion = client_obj.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


#Generate subtitles SRT file based on selected audio file
#using groq speech to text API and srt formatting 
def getSubtitles(client: Groq, audioInputFile: str, srtOutputFileName: str):
    
    subtitlesFolder = "media/srtFiles"

    with open(audioInputFile, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audioInputFile, file.read()), # Required audio file
            model="distil-whisper-large-v3-en", # Required model to use for transcription
            response_format="verbose_json",  # Optional
            language="en"
            )
        
        segments = transcription.segments
    
    fileName = f"{subtitlesFolder}/{srtOutputFileName}.srt"
    
    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        with open(fileName, 'a', encoding='utf-8') as file:
            file.write(segment)
        
    return fileName