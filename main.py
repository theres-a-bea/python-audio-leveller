import Modules
import os


inputdir = input("Please define input directory: \n")

fileArray = Modules.getFilesInDir(inputdir)


for file in fileArray:
    inname, ext = os.path.splitext(file)
    tmpfile = "foo" + ext
    folder = os.path.dirname(file)
    print("Changing Directory to " + folder)
    startwd = os.getcwd()
    os.chdir(folder)

    try:
        permout = os.path.basename(file)
        Modules.leveller(permout,tmpfile)
        Modules.metaMatch(permout,tmpfile)
        print("Renaming file")
        os.rename(tmpfile,permout)

    except:
        print("Exception found - logging")
        os.chdir(startwd)
        stamp = Modules.timestamp()
        f = open("error.log", 'a')
        exception = "\n" + stamp + ": File " + permout + " failed"
        print(exception)
        f.write(exception)
        f.close()

    os.chdir(startwd)