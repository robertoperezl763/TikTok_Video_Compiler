from moviepy.editor import *
from moviepy.video.tools import subtitles
from moviepy.video import fx
from moviepy.video.fx.all import crop
import math
import random

def cropBackgroundVideo(audioFileLoc:str, backgroundClipLoc: str) -> VideoFileClip:
    mainBackground = VideoFileClip(backgroundClipLoc)
    mainAudio = AudioFileClip(audioFileLoc)


    maxClipStart = math.floor(mainBackground.duration) - math.floor(mainAudio.duration) 
    clipStart = random.randint(0,maxClipStart)

    cropBackgroundClip = mainBackground.subclip(clipStart, clipStart + mainAudio.duration)
    (w,h) = cropBackgroundClip.size
    cropBackgroundClip = crop(cropBackgroundClip, width= 480, height= 720, x_center= w/2, y_center = h/2)
    
    print('successfull crop')
    cropBackgroundClip.write_videofile('testing_crop.mp4')
    
    #fixing bug for FFMPEG Error...
    mainAudio.close()

    return cropBackgroundClip


def generateFinalVideo(subtitleFileLoc, audioFileLoc, backgroundClipLoc, finalVideoName):
    finalVideoFolder = 'final_videos'

    #create audioclip for audio file
    mainAudio = AudioFileClip(audioFileLoc)

    #get cropped / shortened background video clip 
    backgroundVideo = cropBackgroundVideo(audioFileLoc=audioFileLoc, 
                                          backgroundClipLoc=backgroundClipLoc)

    #Design for subtitles
    generator = lambda txt: TextClip(
        txt,
        font="./fonts/bold_font.ttf",
        fontsize=25,
        color="#ffffff",
        stroke_color="black",
        stroke_width=3,
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