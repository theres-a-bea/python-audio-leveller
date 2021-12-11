from pathlib import Path
import os
import eyed3

def safeconvert(input):
    output=input.replace(" ","-")
    output=output.replace(',','')
    output=output.replace('(','')
    output=output.replace(')','')
    output=output.encode('ascii', 'xmlcharrefreplace')
    output=output.decode('ascii')
    return output

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

#Applies ffmpeg's loudnorm
def leveller(inputfile, outputfile):
    print("Processing " + str(inputfile))
    #Defines Input/Output Extensions
    exttmp = str(Path(inputfile).suffix)
    extin = exttmp[1:]
    print("Extension in: " + extin)
    exttmp = str(Path(outputfile).suffix)
    extout = exttmp[1:]
    print("Extension out: " + extout)

    print("Temporarily renaming file so FFMpeg doesn't cry")
    safein = safeconvert(inputfile)
    os.rename(inputfile, safein)
    safeout = safeconvert(outputfile)

    #ffmpeg -i input.mp3 -af loudnorm=I=-16:LRA=11:TP=-1.5 output.mp3
    command = "ffmpeg -loglevel error -i " + str(safein) + " -af loudnorm=I=-9:LRA=11:TP=-1.5 " + str(safeout)
    print("Running " + command)
    os.system(command)
    os.rename(safein, inputfile)
    os.rename(safeout, outputfile)


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