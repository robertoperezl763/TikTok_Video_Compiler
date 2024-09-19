from datetime import timedelta
import os

def createSRT(baseDir, segmentDict, fileName):
    srtFolder = baseDir + "/srtFiles"

    for segment in segmentDict:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join(srtFolder, f"{fileName}_subs.srt")

        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename