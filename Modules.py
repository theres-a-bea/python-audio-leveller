from pathlib import Path
import os
import eyed3
import time
from datetime import datetime

def safeconvert(input, type):
    if type == "url":
        output=input.replace(" ","-")
        output=output.replace(',','')
        output=output.replace('(','')
        output=output.replace(')','')
        output=output.encode('ascii', 'xmlcharrefreplace')
        output=output.decode('ascii')
    if type == "path":
        output=input.replace(" ",r"\ ")
        output=output.replace("(",r"\(")
        output=output.replace(")",r"\)")
        output=output.replace("*",r"\*")
        output=output.replace("&",r"\&")
        output=output.replace("~",r"\~")
        output=output.replace("'",r"\'")
    else:
        output=input.replace(" ","-")
        output=output.replace(',','')
        output=output.replace('(','')
        output=output.replace(')','')

        output=output.encode('ascii', 'xmlcharrefreplace')
        output=output.decode('ascii')
    return output

#Gets visable files in directory, returns fileList in array as posixPathes
def getFilesInDir(dir):
    fileList = list(Path(dir).rglob("*.mp3"))
    fileList.append(list(Path(dir).rglob("*.wav")))
    fileList.append(list(Path(dir).rglob("*.m4a")))
    return fileList

def timestamp():
    dateTimeObj = datetime.now()
    timecode = dateTimeObj.strftime("%Y-%m-%d_%H%M%S")
    return timecode

#Applies ffmpeg's loudnorm
def leveller(inputfile, outputfile):
    print("Processing " + str(inputfile))
    safein = safeconvert(inputfile, "path")
    safeout = safeconvert(outputfile, "path")
    command = "ffmpeg -loglevel error -i " + str(safein) + " -af loudnorm=I=-9:LRA=11:TP=-1.5 " + str(safeout)
    print("Running " + command)
    os.system(command)

def metaMatch(inputfile, outputfile):

    print ('Writing meta to ' + outputfile)
    inmeta = eyed3.load(inputfile)
    outmeta = eyed3.load(outputfile)
    arname = inmeta.tag.artist
    outmeta.tag.artist = arname
    print ('Artist: ' + arname)
    trname = inmeta.tag.title
    outmeta.tag.title = trname
    print ('Track: ' + trname)
    alname = inmeta.tag.album
    outmeta.tag.album = alname
    print ('Album: ' + alname)
    trnum = inmeta.tag.track_num
    outmeta.tag.track_num = trnum[0]
    print ('Track Number: ' + str(trnum[0]))
    outmeta.tag.save()
    print ('Meta Saved.')

