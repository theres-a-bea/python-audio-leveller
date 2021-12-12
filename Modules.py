from pathlib import Path
import os
import eyed3
from datetime import datetime

#Converts input string into parsable by URL/path
def safeconvert(input, type):
    #if a URL, removes broken chars and replaces with URL safe ones
    if type == "url":
        output=input.replace(" ","-")
        output=output.replace(',','')
        output=output.replace('(','')
        output=output.replace(')','')
        output=output.encode('ascii', 'xmlcharrefreplace')
        output=output.decode('ascii')
    
    #if a path, removes bash breaking characters
    if type == "path":
        output=input.replace(" ",r"\ ")
        output=output.replace("(",r"\(")
        output=output.replace(")",r"\)")
        output=output.replace("*",r"\*")
        output=output.replace("&",r"\&")
        output=output.replace("~",r"\~")
        output=output.replace("'",r"\'")
    
    #if unknown, defaults to removing everything
    else:
        output=input.replace(" ","")
        output=output.replace(',',"")
        output=output.replace('(',"")
        output=output.replace(')',"")
        output=output.replace("*","")
        output=output.replace("&","")
        output=output.replace("~","")
        output=output.replace("'","")
        output=output.encode('ascii', 'xmlcharrefreplace')
        output=output.decode('ascii')
    return output

#Gets visable files in directory, returns fileList in array as posixPathes
def getFilesInDir(dir):
    #checks for all files that are .mp3,.wav,.aac or .m4a
    fileList = list(Path(dir).rglob("*.mp3"))
    fileList.append(list(Path(dir).rglob("*.wav")))
    fileList.append(list(Path(dir).rglob("*.aac")))
    fileList.append(list(Path(dir).rglob("*.m4a")))
    return fileList

#Generates Timestamp
def timestamp(var=1):
    if var == 1:
        dateTimeObj = datetime.now()
        timecode = dateTimeObj.strftime("%Y-%m-%d_%H%M%S")
    if var == 2:
        dateTimeObj = datetime.now()
        timecode = dateTimeObj.strftime("%Y%m%d%H%M%S%f")
    return timecode

#Applies ffmpeg's loudnorm
def leveller(inputfile, outputfile, intLoud=-9, LRA=11, TP=-1.5):
    print("Processing " + str(inputfile))

    #Converts input strings into bash-safe pathes
    #safein = safeconvert(inputfile, "path")
    #safeout = safeconvert(outputfile, "path")

    #Defines Loudnorm variables:

    integratedLoudness=str(intLoud)
    #Loudness Target, effectively LUFS

    loudnessRange=str(LRA)
    #Difference between peak and trough

    truePeak=str(TP)
    #True peak of the file


    #Generates & runs ffmpeg command
    command = 'ffmpeg -loglevel error -y -i "' + str(inputfile) + '" -af loudnorm=I='+integratedLoudness+':LRA='+loudnessRange+':TP='+truePeak+' "' + str(outputfile)+'"'
    
    print("Running " + command)
    os.system(command)

#Pulls meta from inputfile, writes to output file
def metaMatch(inputfile, outputfile):
    print ('Writing meta to ' + outputfile)
    
    #loads working files
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
