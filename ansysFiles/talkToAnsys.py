import os
import subprocess

# worDir = os.getcwd()
# ansDir = r'C:\Program Files\ANSYS Inc\ANSYS Student\v201\Framework\bin\Win64'
	
# # os.chdir(ansDir)
# print("Current working directory ", os.getcwd())
subprocess.Popen(["C:/Program Files/ANSYS Inc/ANSYS Student/v201/Framework/bin/Win64/RunWB2.exe", '-R', 'journalTesting.wbjn', '-I'])


# # allCmds = "{}; {}".format(cmd1 cmd2)
# # allCmds = "{}; {}".format(cmd1, cmd2) 
# # https://stackoverflow.com/questions/9649355/python-how-to-run-multiple-commands-in-one-process-using-popen
