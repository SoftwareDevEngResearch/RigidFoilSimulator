import os
import numpy as np
import matplotlib.pyplot as plt
import motionProfile as mP


def convert_2_txt(file_path):
    """Identifies if file needs to be converted to txt"""
    if (file_path.find(".txt") < 0):
        new_path = file_path + ".txt"
        os.rename(file_path, new_path)
        file_path = new_path
    return file_path 
    
def add_data_columns(file_path, chord, theta, h):
    """Check to see if new columns of rotated data have been added and add if needed"""
    
    file_object = open(file_path,"r")
    headers = file_object.readline()
    variable_names = np.array(headers.replace(",", " ").strip().split())
    var_count = len(variable_names)
    if (headers.find("x-rotated")<0):
        #print("Newly Processed")
        x_wallshear_col = np.where(variable_names == "x-wall-shear")
        y_wallshear_col = np.where(variable_names == "y-wall-shear")
        #If this header column does not exist, it means the data has not yet been processed
        c, s= np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        data = np.empty((0,var_count+3))
        variable_names = [np.append(variable_names, np.array(['x-rotated', 'y-rotated', 'calculated-wallshear']))]
        data = variable_names
        for line in file_object:
            cols = np.array([float(i) for i in line.replace(","," ").strip().split()])
            xyR = np.dot(R, cols[1:3]) + [chord/2, 0]
            #print(xyR)
            top_bottom = int(1 if xyR[1] > 0 else -1)
            #frontal_region = int(1 if xyR[0] < 0.3*chord else -1)
            #if top_bottom * theta > 0: 
            wallshear = cols[x_wallshear_col]*np.cos(theta)-cols[y_wallshear_col]*np.sin(theta)
            cols = np.concatenate((cols, xyR, wallshear))
            data = np.append(data, [cols], axis=0) 
        x_rotated_col = var_count + 1
        set_data = data[1:,:] 
        sorted_data = set_data[set_data[:, x_rotated_col-1].argsort()]
        final_data = np.append(variable_names, sorted_data, axis=0)
        #np.savetxt(file_path, final_data[:-1,:], fmt="%s") 
        #print(data.shape)

    else:
        print("Already Processed")
        final_data = [np.array(variable_names)]
        x_rotated_col = int(np.where(variable_names == "x-rotated")[0])
        for line in file_object:
            cols = np.array([float(i) for i in line.replace(","," ").strip().split()])
            final_data = np.append(final_data, [cols], axis=0)       
    file_object.close()
    
    x_rot = final_data[1:,-3]
    y_rot = final_data[1:,-2]
    avg_y = np.average(np.array([y_rot]).astype(np.float))
    print("Average Y after rotated = %s " % (avg_y))
    print("Average Y + h Shift = %s" % (avg_y+h))
    #plt.plot(x_rot, y_rot)    
    #plt.show()
    
    
def process_wallshear_data(folder_path, foilProfile):
    """Go into wall shear folder and process raw data"""
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    file_names = list(filter(lambda x:(x.find("les") >= 0 or x.find("wallshear") >0), file_names))
    #for x in range(1):
    for x in range(len(file_names)):
        file_path = convert_2_txt(folder_path+"\\"+file_names[x])
        time_step = int(file_names[x].split('-')[-1].split('.')[0])
        theta = foilProfile.theta[time_step]
        print('\n FileName = %s \n Time Step [ct] = % s, Theta [deg] = % s' % (file_names[x], time_step, np.degrees(theta)))
        print("h - h0 = %s" % (foilProfile.h[time_step]-foilProfile.h0))
        if theta != 0:
            add_data_columns(file_path, foilProfile.chord, foilProfile.theta[time_step], foilProfile.h0-foilProfile.h[time_step]) 

if __name__ == "__main__":
    """testing script functionality"""
    folder_path = os.getcwd()+"\\WallShearData"
    foilProfile = mP.FoilProf(1.6,0.15/2,70,0.15,1000)
    process_wallshear_data(folder_path, foilProfile)

