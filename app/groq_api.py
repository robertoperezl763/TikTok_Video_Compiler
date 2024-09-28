import json
from groq import Groq
from datetime import timedelta
from app.break_srt import split_json_segments, format_srt_segments
#call groq chatbot and return response from API based on user content prompt
def getPrompt(client_obj: Groq, content: str, sysPrompt: str, temp: float = 0.8):
    
    # sysPrompt= "you are a brilliant horor story teller, and capable of creating short, captivating and immersing stories. Each Story should be unique and new"

    chat_completion = client_obj.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sysPrompt,
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
        temperature= temp
    )
    return chat_completion.choices[0].message.content

def getSubtitles(client: Groq, audioInputFile: str, srtOutputFileName: str, max_words: int):
    
    subtitlesFolder = "media/srtFiles"

    sttPrompt = "keep segments to no more than 1.5 seconds MAX"
    #"You are transcribing a short scary story, the transcription will be used to create subtitles for a video and SHOULD BE KEPT TO 5 WORDS PER SEGMENT. Spelling should be easy to interpret in quick subtitles"
    
    with open(audioInputFile, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audioInputFile, file.read()), # Required audio file
            model="distil-whisper-large-v3-en", # Required model to use for transcription
            prompt= sttPrompt,
            temperature=0.2,
            response_format="verbose_json",  # Optional
            language="en"
            )
        
        #pulling out segments from api reponse
        segments = transcription.segments

        #convert segmet into json data for function use???
        segments = json.dumps(segments)
        segments = json.loads(segments)

        #split segments into more manageable size segments
        segments = split_json_segments(json_data=segments, max_words_per_segment=max_words)

        #generate file location path for srt file
        fileLoc = f"{subtitlesFolder}/{srtOutputFileName}.srt"
            
    #format segments JSON into propper srt format
    return format_srt_segments(segments=segments, fileLocation=fileLoc)



# def getSubtitles(client: Groq, audioInputFile: str, srtOutputFileName: str):
    
#     subtitlesFolder = "media/srtFiles"

#     sttPrompt = "keep segments to no more than 1.5 seconds MAX"
#     #"You are transcribing a short scary story, the transcription will be used to create subtitles for a video and SHOULD BE KEPT TO 5 WORDS PER SEGMENT. Spelling should be easy to interpret in quick subtitles"
    
#     with open(audioInputFile, "rb") as file:
#         transcription = client.audio.transcriptions.create(
#             file=(audioInputFile, file.read()), # Required audio file
#             model="distil-whisper-large-v3-en", # Required model to use for transcription
#             prompt= sttPrompt,
#             temperature=0.2,
#             response_format="verbose_json",  # Optional
#             language="en"
#             )
        
#         # print(transcription)
#         segments = transcription.segments
#         print(type(segments))
#         return json.dumps(segments)
#         # print(transcription.segments)

#         # with open("example_json.txt", "w") as file:
#         #     file.write(str(transcription.segments))
    
#     fileLoc = f"{subtitlesFolder}/{srtOutputFileName}.srt"
    
#     for segment in segments:
#         startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
#         endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
#         text = segment['text']
#         segmentId = segment['id']+1
#         segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

#         with open(fileLoc, 'a', encoding='utf-8') as file:
#             file.write(segment)
        
#     return fileLoc
