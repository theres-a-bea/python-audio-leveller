import Modules
import os
import threading
import multiprocessing

def processfile(file):
    #checks if file already processed
    if processedFiles.includes(file):
        return False
    else:
        #splits input file into name and extension
        inname, ext = os.path.splitext(file)
        #generates tmp file with same ext
        tmpfile = "foo" + ext
        #finds directory of input file and changes directory to it (look, it makes ffmpeg cry less, fuck off)
        folder = os.path.dirname(file)
        print("Changing Directory to " + folder)
        startwd = os.getcwd()
        os.chdir(folder)

        try:
            permout = os.path.basename(file)
            #once we have the basename of the file, run the leveller and metamatcher
            Modules.leveller(permout,tmpfile)
            Modules.metaMatch(permout,tmpfile)
            print("Renaming file " + tmpfile)
            os.remove(permout)
            os.rename(tmpfile,permout)

        except:
            #if above fails, log for investigation
            print("Exception found at " + file + " - logging")
            os.chdir(startwd)
            stamp = Modules.timestamp()
            f = open("error.log", 'a')
            exception = "\n" + stamp + ": File " + permout + " failed"
            print(exception)
            f.write(exception)
            f.close()
            return False


        #if we're not in the main dir, change back to it
        if os.getcwd() != startwd:
            os.chdir(startwd)

        processedFiles.append(file)
        return True

inputdir = input("Please define input directory: \n")

fileArray = Modules.getFilesInDir(inputdir)

processedFiles = []

nextFile = 0

while len(processedFiles)<=len(fileArray):
    if threading.active_count()<multiprocessing.cpu_count():
        #***GET NEXT FILE, RUN THROUGH PROCESS FILE***
        fileToProcess = fileArray[nextFile]
        nextFile = nextFile + 1
    else:
        print("Max threads used")