import Modules
import os


inputdir = input("Please define input directory: \n")

fileArray = Modules.getFilesInDir(inputdir)


for file in fileArray:
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
        print("Renaming file")
        os.rename(tmpfile,permout)

    except:
        #if above fails, log for investigation
        print("Exception found - logging")
        os.chdir(startwd)
        stamp = Modules.timestamp()
        f = open("error.log", 'a')
        exception = "\n" + stamp + ": File " + permout + " failed"
        print(exception)
        f.write(exception)
        f.close()

    #if we're not in the main dir, change back to it
    if os.getcwd() != startwd:
        os.chdir(startwd)