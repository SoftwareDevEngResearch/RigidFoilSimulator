import os, sys
import numpy as np
from . import Parameters
import matplotlib.pyplot as plt

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
        #If this header column does not exist, it means the data has not yet been processed
        x_wallshear_col = np.where(variable_names == "x-wall-shear")
        y_wallshear_col = np.where(variable_names == "y-wall-shear")
        
        c, s= np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        
        data = np.empty((0,var_count+3))
        variable_names = [np.append(variable_names, np.array(['x-rotated', 'y-rotated', 'calculated-wallshear']))]
        data = variable_names
        
        for line in file_object:
            # Get data from each line and calculate the rotated position
            cols = np.array([float(i) for i in line.replace(","," ").strip().split()])
            cols[2] = cols[2] - h
            xyR = np.dot(R, cols[1:3]) + [chord/2, 0]
            
            # Filter to only collect data for the leading edge of the correct surface
            top_bottom = int(1 if xyR[1] > 0 else -1)
            frontal_region = int(1 if xyR[0] < 0.2*chord else -1)
    
            if top_bottom*theta > 0 and frontal_region == 1: 
                wallshear = cols[x_wallshear_col]*np.cos(theta)-cols[y_wallshear_col]*np.sin(theta)
                cols = np.concatenate((cols, xyR, wallshear))
                data = np.append(data, [cols], axis=0) 
                
        x_rotated_col = var_count
        
        # Sort data 
        set_data = data[1:,:].astype(float)
        sorted_data = set_data[set_data[:, var_count].argsort()]
        final_data = np.append(variable_names, sorted_data, axis=0)
        #np.savetxt(file_path, final_data[:-1,:], fmt="%s") 

    else:
        print("Already Processed")
        final_data = [np.array(variable_names)]
        x_rotated_col = int(np.where(variable_names == "x-rotated")[0])
        for line in file_object:
            cols = np.array([float(i) for i in line.replace(","," ").strip().split()])
            final_data = np.append(final_data, [cols], axis=0)       
    file_object.close()
    return final_data

def wallshearData(Files, FoilDyn):
    """Go into wall shear folder and process raw data"""
    
    data_path = Files.data_path
    
    file_names = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
    file_names = list(filter(lambda x:(x.find("les") >= 0 or x.find("wallshear") >0), file_names))

    if data_path == os.path.dirname(os.path.realpath(__file__)) + r"\Tests\Assets":
        FoilDyn.update_totalCycles(2)
        modfiles = list(filter(lambda x:(x.find("mod-") >= 0), file_names))
        for x in modfiles:
            os.remove(data_path+"\\"+x)
        file_names = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
        file_names = list(filter(lambda x:(x.find("les") >= 0 or x.find("wallshear") >0), file_names))
    
    temp_database = np.empty([0,3])
    ct = 0

    for x in range(len(file_names)):
        file_path = convert_2_txt(data_path+"\\"+file_names[x])
        time_step = int(file_names[x].split('-')[-1].split('.')[0])
        theta = FoilDyn.theta[time_step]

        if round(theta,3) != 0 and time_step > 1000:
            final_data = add_data_columns(file_path, FoilDyn.chord, FoilDyn.theta[time_step], FoilDyn.h[time_step])
            np.savetxt(Files.folder_path+"\\_mod-"+file_names[x], final_data[:-1,:], fmt="%s")
            final_data = final_data[1:,:].astype(float)
            processed_data = np.transpose(np.append([final_data[:,-3]], [final_data[:,-1]], axis=0))
            processed_data2 = np.append(processed_data, np.full((processed_data.shape[0],1), time_step).astype(int) , axis=1)
            temp_database = np.append(temp_database, processed_data2, axis=0)
            x = processed_data[1:,-2].astype(float)/FoilDyn.chord
            wallshear = processed_data[1:,-1].astype(float)
            if np.min(wallshear) < 0 and wallshear[0] > 0 and ct <= 4:
                if ct == 0: 
                    shed_time = time_step
                    shed_x = x
                    shed_wallshear = wallshear
                    x_wallshear = shed_x[np.argmin(wallshear)]
                ct = ct + 1
            elif ct == 4:
                ct = 10
                fig, axs = plt.subplots(3)
                print("Output Results:\nVortex is shed at time step = %s \nVortex Position = %s" % (shed_time,x_wallshear))
                desired_steps = np.unique(temp_database[:,-1]).astype(int)[-9:]
                temp_set = np.empty([0,3])
                filtered_data = np.empty([0,3])
                for step in desired_steps:
                    filtered_data = temp_database[temp_database[:,-1]==step,:]
                    axs[0].plot(filtered_data[:,0]/FoilDyn.chord,filtered_data[:,1], label = step)
                    temp_x = temp_database[temp_database[:, -1] == step,:][np.argmin(temp_database[temp_database[:, -1] == step,1]),0]
                    temp_ws = np.min(temp_database[temp_database[:, -1] == step,1])
                    temp_set = np.append(temp_set, [[step, temp_x, temp_ws]], axis=0)
                #print(temp_set)
                axs[1].plot(temp_set[:,0], temp_set[:,2])
                axs[2].plot(temp_set[:,0], temp_set[:,1]/FoilDyn.chord)
                axs[0].legend()
                axs[0].grid()
                axs[1].grid()
                axs[2].grid()
                fig.suptitle("k = " + str(FoilDyn.reduced_frequency))
                axs[0].set(xlabel='x position along the chord, [x/C]', ylabel='Wall Shear')
                axs[1].set(xlabel='time step [s]', ylabel='Wall Shear')
                axs[2].set(xlabel='time step [s]', ylabel='x position along the chord, [x/C]')
                if Parameters.specialCase() == False:  
                    print("Exit plots to end procedure")
                    plt.show()
    try:
        shed_time
    except NameError:
        sys.exit("Vortex has not shed within the simulated time line.")
      
    return shed_time, x_wallshear
