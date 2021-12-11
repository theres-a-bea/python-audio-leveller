from pathlib import Path
import os
from pydub import AudioSegment
from pydub import effects as fx
from pydub import utils as pyutil
import eyed3

#Gets visable files in directory, returns fileList in array as posixPathes
def getFilesInDir(dir):
    fileList = list(Path(dir).rglob("*.*"))
    
    #Defines empty array to store indexes to remove
    toRemove = []
    
    #Runs through fileList index, checks if file starts with . & documents if it does
    for file in fileList:
        filename = os.path.basename(file)
        print(filename)
        if filename.startswith(".") == True:
            print(filename + " is Invisible, adding to list")
            #Stores index to remove in array
            toRemove.append(fileList.index(file))
    
    #runs through array, removes invisibles
    print ("Removing invisibles from array...")
    for i in toRemove:
        del fileList[i]

    #returns array
    return fileList

#Applies gain to get RMS to -6 & applies a 4:1, 1ms attack, 30ms release, -20 thresh compressor
def leveller(inputfile, outputfile):
    print("Processing " + str(inputfile))
    #Defines Input/Output Extensions
    exttmp = str(Path(inputfile).suffix)
    extin = exttmp[1:]
    print("Extension in: " + extin)
    exttmp = str(Path(outputfile).suffix)
    extout = exttmp[1:]
    print("Extension out: " + extout)

    #Defines filein as an AudioSegment for pyDub fuckery :P
    filein = AudioSegment.from_file(inputfile, extin)

    #Defines filein's current RMS
    dB = filein.dBFS

    #Gets difference in RMS before and applies gain to get it to -6
    change_in_dB = -1 * (dB)
    print("Gain at " + str(change_in_dB))
    filein.apply_gain(change_in_dB)
    print("Gain Applied")

    #Normalizes
    print("Applying Normalization")
    fx.normalize(filein)
    print("Normalized")

    print("Writing to " + outputfile)
    filein.export(outputfile, extout)
    print("Write successful")

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

leveller("testOutput/05 Open Road Song.mp3", "open-out.mp3")
leveller("testOutput/1-15 Sheena Is A Punk Rocker (Single Version).mp3", "sheena-out.mp3")