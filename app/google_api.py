from google.cloud import texttospeech
from random import randint
def createAudio(client:texttospeech.TextToSpeechClient, prompt: str, outputFileName: str):
    listVoices= ["en-US-Standard-F","en-US-Standard-D","en-US-Standard-J","en-US-Studio-O"]
    randNum = randint(0, len(listVoices)-1)
    voiceName = listVoices[randNum]
    
    audioFolder = 'media/audio'
    
    synthesis_input = texttospeech.SynthesisInput(text=prompt)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name= voiceName,
        #ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    ) 

    #en-US-Polyglot-1
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audioFileLoc =f'{audioFolder}/{outputFileName}.mp3' 
    with open(audioFileLoc, "wb") as out:
        out.write(response.audio_content)

    return audioFileLoc