import Modules
import os
import threading
import multiprocessing

def processfile(file):
    #splits input file into name and extension
    inname, ext = os.path.splitext(file)
    #generates tmp file with same ext
    #finds directory of input file and changes directory to it (look, it makes ffmpeg cry less, fuck off)
    folder = os.path.dirname(file)
    stamp = Modules.timestamp(2)
    tmpfile = folder + "\\" + stamp + ext
    #print("Changing Directory to " + folder)
    #startwd = os.getcwd()
    #os.chdir(folder)

    try:
        #once we have the basename of the file, run the leveller and metamatcher
        Modules.leveller(file,tmpfile)
        Modules.metaMatch(file,tmpfile)
        print("Renaming file " + tmpfile)
        os.remove(file)
        os.rename(tmpfile,file)

    except:
        #if above fails, log for investigation
        print("Exception found at " + str(file) + " - logging")
        stamp = Modules.timestamp()
        f = open("error.log", 'a')
        exception = "\n" + str(stamp) + ": File " + str(file) + " failed"
        print(exception)
        f.write(exception)
        f.close()
        return False

    processedFiles.append(file)
    return True

inputdir = input("Please define input directory: \n")

fileArray = Modules.getFilesInDir(inputdir)

processedFiles = []

nextFile = 0

while len(processedFiles)<=len(fileArray):
    if threading.active_count()<multiprocessing.cpu_count():
        fileToProcess = fileArray[nextFile]
        newThread = threading.Thread(target=processfile, args=(fileToProcess,), daemon=True)
        newThread.start()
        print("Beginning process " + str(nextFile) + " of " + str(len(fileArray)))
        nextFile = nextFile + 1
    else:
        nextFile = nextFile