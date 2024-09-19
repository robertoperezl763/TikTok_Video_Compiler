import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from datetime import timedelta
from srt_transcription import createSRT

#print(os.getenv("OPENAI_API_KEY"))
load_dotenv()
#######################################
base_dir = "C:/Users/Roberto Perez/Desktop/Projects/TikTok_Compiler"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def groq_startupTest():


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "in no more than 10 words, Explain the importance of fast language models",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

def groq_ttsTest():
        # Specify the path to the audio file         docs_assets_example_ref
    filename = base_dir + "/media/testAudio.mp3" # Replace with your audio file!

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()), # Required audio file
            model="distil-whisper-large-v3-en", # Required model to use for transcription
            prompt="transcribe this audio file and provide output as srt file",  # Optional
            response_format="verbose_json",  # Optional
            language="en",  # 
            # temperature=0.0  # Optional
            )

        segments = transcription.segments
        print(segments)
        createSRT(baseDir=base_dir, segmentDict=segments, fileName="testingsrtstuff")



    return "this shit works?!?!?!"

# prompt = groq_startupTest()
# print(prompt)
# with open("test.txt", "w") as file:
#     file.write(prompt)

subtitles = groq_ttsTest()
# with open("testsubs.srt", "w") as file:
#     file.write(subtitles)