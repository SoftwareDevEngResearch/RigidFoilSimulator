# import string
# import tkinter
# import tkFileDialog

# def main():

    # #import tkFileDialog

    # #import re

    # ff = tkFileDialog.askopenfilenames()

    # files = re.findall('{(.*?)}', ff)

    # #import Tkinter,tkFileDialog

    # root = Tkinter.Tk()

    # files = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')

    # #files = raw_input("which files do you want processed?")

    # files = root.tk.splitlist(files)

    # print ("list of filez =",files)
    
# main()

import os
from os import listdir
from os.path import isfile, join
mypath = os.getcwd()+"\\WallShearData"
print(mypath)
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)

# result = list(filter(lambda x:(x.find(".py") >= 0 or x.find(".md") >=0), onlyfiles))
# print(result)
