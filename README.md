This is my personal project to automate video creation!!!

The project uses the following APIs Currently:
- GroqCloud 
- GoogleCloud

The project utilizes Groq Chat to generate script. Script is then passed to GoogleCloud Text-to-Speech API to generate audio. Audio file is passed into Groq's Transcription API to generate a timestamped subtitles transcription. 

MoviePy is then used to combine the audio, generic background video, and generate subtitles based on timestamped transcription.

Final Videos are currently being manually uploaded due to Google API verification requirements for automatic uploading...

Final product can be found on youtube at:
