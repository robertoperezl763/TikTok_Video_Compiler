from moviepy.editor import *
from moviepy.video.tools import subtitles
from moviepy.video import fx
from moviepy.video.fx.all import crop
import math
import random

def cropBackgroundVideo(audioFileLoc:str, backgroundClipLoc: str) -> VideoFileClip:
    

    mainBackground = VideoFileClip(backgroundClipLoc)
    mainAudio = AudioFileClip(audioFileLoc)
    audioDuration = mainAudio.duration
    mainAudio.close()    #fixing bug for FFMPEG Error...

    maxClipStart = math.floor(mainBackground.duration) - math.floor(audioDuration) 
    clipStart = random.randint(0,maxClipStart)

    cropBackgroundClip = mainBackground.subclip(clipStart, clipStart + audioDuration)
    (w,h) = cropBackgroundClip.size
    cropBackgroundClip = crop(cropBackgroundClip, width= 480, height= 720, x_center= w/2, y_center = h/2)
    
    cropBackgroundClip.write_videofile('media/background_video/cropped_temp_background.mp4')


    return cropBackgroundClip


def generateFinalVideo(subtitleFileLoc: str, audioFileLoc: str, backgroundClipLoc: str, finalVideoName: str):
    finalVideoFolder = 'final_videos'

    #create audioclip for audio file
    mainAudio = AudioFileClip(audioFileLoc)

    #get cropped / shortened background video clip 
    backgroundVideo = cropBackgroundVideo(audioFileLoc=audioFileLoc, 
                                          backgroundClipLoc=backgroundClipLoc)

    #Design for subtitles
    generator = lambda txt: TextClip(
        txt,
        font='Arial-Rounded-MT-Bold', #"./fonts/bold_font.ttf",
        fontsize=32,
        color="#ffffff",
        stroke_color="black",
        stroke_width=1.5,
    )

    #create subtitle video clip
    finalSubs = subtitles.SubtitlesClip(subtitleFileLoc, generator)
    #overlay subtitle clip to background
    result = CompositeVideoClip([
        backgroundVideo,
        finalSubs.set_position(("center", "center"))
    ])

    #add audio to final video
    result = result.set_audio(mainAudio)

    finalVideoLoc = f'{finalVideoFolder}/{finalVideoName}.mp4'
    result.write_videofile(finalVideoLoc)

    #avoids error
    mainAudio.close()

    return finalVideoLoc