import os
import subprocess
import shutil

# worDir = os.getcwd()


# # allCmds = "{}; {}".format(cmd1 cmd2)
# # allCmds = "{}; {}".format(cmd1, cmd2) 
# # https://stackoverflow.com/questions/9649355/python-how-to-run-multiple-commands-in-one-process-using-popen

fluent_path = shutil.which("fluent")
version_path=fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"

subprocess.Popen([version_path, '-R', 'testTemplate.wbjn', '-I'])
