import os
from google.cloud import texttospeech

def createAudio(client:texttospeech.TextToSpeechClient, prompt: str, outputFileName: str):
    
    audioFolder = 'media/audio'
    
    synthesis_input = texttospeech.SynthesisInput(text=prompt)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    ) 
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audioFileLoc =f'{audioFolder}/{outputFileName}.mp3' 
    with open(audioFileLoc, "wb") as out:
        out.write(response.audio_content)
    
    print("Audio creation success!")
    return audioFileLoc