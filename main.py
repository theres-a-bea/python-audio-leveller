import Modules
import os

inputdir = input("Please define input directory: \n")

fileArray = Modules.getFilesInDir(inputdir)

for file in fileArray:
    inname = os.path.basename(file).split('.')[0]
    ext = os.path.basename(file).split('.')[1]
    folder = os.path.dirname(file)
    tmpout = folder + '/' + inname + str(2) + '.' + ext
    permout = folder + '/' + inname + '.' + ext
    Modules.leveller(permout, tmpout)
    Modules.metaMatch(permout, tmpout)
    print("Renaming file")
    os.rename(tmpout, permout)