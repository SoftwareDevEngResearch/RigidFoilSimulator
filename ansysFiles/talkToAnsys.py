import os
import subprocess
import shutil


fluent_path = shutil.which("fluent")

WB_path=fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"

subprocess.Popen([WB_path, '-R', 'testTemplate.wbjn', '-I'])








# worDir = os.getcwd()


# # allCmds = "{}; {}".format(cmd1 cmd2)
# # allCmds = "{}; {}".format(cmd1, cmd2) 
# # https://stackoverflow.com/questions/9649355/python-how-to-run-multiple-commands-in-one-process-using-popen



# This one does not, where the result should be:
#   C:\Program Files\ANSYS Inc\ANSYS Student\v201\Framework\bin\Win64\RunWB2.exe
RunWB2_path = shutil.which("RunWB2")

# This is what I want to put the variable in:
subprocess.Popen([PATH, '-R', 'testTemplate.wbjn', '-I'])



