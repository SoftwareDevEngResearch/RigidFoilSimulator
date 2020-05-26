import os
import numpy as np
from os import listdir
from os.path import isfile, join


def convert_2_txt(file_path):
    """Identifies if file needs to be converted to txt"""
    if (file_path.find(".txt") < 0):
        new_path = file_path + ".txt"
        os.rename(file_path, new_path)
        file_path = new_path
    return file_path 

    
def add_data_columns(file_path, theta):
    """Check to see if new columns of rotated data have been added and add if needed"""
    
    file_object = open(file_path,"r+")
    headers = file_object.readline()
    variable_names = headers.strip().split()
    x_wallshear_col = variable_names.index('x-wall-shear')
    
    if (headers.find("top1_bottom0") <0):
        #If this header column does not exist, it means the data has not yet been processed
        data = []
        for line in file_object:
            cols = line.strip().split()
            data.append(cols)
    file_object.close()
    data = np.array(data)
    coord = data[:,[1,2]]
    c, s= np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    print(len(coord))
    #xyR = np.dot(R, np.array(  
    

def process_wallshear_data():
    """Go into wall shear folder and process raw data"""
    theta0 = np.radians(70)
    steps_per_cycle = 1000
    
    folder_path = os.getcwd()+"\\WallShearData"
    file_names = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    file_names = list(filter(lambda x:(x.find("wallshear") >= 0), file_names))

    for x in range(1):
    #for x in range(len(file_names)):
        time_step = float(file_names[x].split('-')[-1].split('.')[0]) % steps_per_cycle
        theta = -theta0*np.sin(2*np.pi*time_step/steps_per_cycle)
        
        file_path = convert_2_txt(folder_path+"\\"+file_names[x])
        add_data_columns(file_path, theta)


if __name__ == "__main__":
    """testing script functionality"""
    process_wallshear_data()