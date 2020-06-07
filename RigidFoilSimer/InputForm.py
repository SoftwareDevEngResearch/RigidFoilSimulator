##RIGID-FOIL-SIMULATION-GENERATOR-DATA-FORM

## Enter directory folder name to save Simulation Files
sim_path = r"C:\Users\ngov\Desktop"
folder_name = r"RigidFoilSimulation"
project_name = r"k0p08"


## Enter foil geometry details in units of [M]
# Note: Ellipse height must be less than ellipse width

chord_length = 0.15            
leading_edge_height = chord_length*0.15/2
leading_edge_width = leading_edge_height*4
trailing_edge_height = 0.001
trailing_edge_width = trailing_edge_height*6


## Enter dynamic parameter details
# Note: time steps per cycle x number of cycles must be an integer

reduced_frequency = 0.08                #[-]
heaving_frequency = 1.6                 #[Hz]
heaving_amplitude = chord_length*0.5    #[M]
pitching_amplitude = 70                 #[deg]
time_steps_per_cycle = 1000             #[-]
number_of_cycles = 0.020                #[-] 
fluid_density = 1.225                   #[kg/m^3]
