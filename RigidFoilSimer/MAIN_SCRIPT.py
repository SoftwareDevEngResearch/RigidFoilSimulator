##RIGID-FOIL-SIMULATION-GENERATOR

## Enter foil geometry details in units of [M]

chord_length = 0.15            
leading_edge_height = 0.00325  
leading_edge_width = chord_length/4
trailing_edge_height = 0.0002  
trailing_edge_width = 0.012

## Enter dynamic parameter details

heaving_frequency = 1.6                 #[Hz]
heaving_amplitude = chord_length*0.5    #[M]
pitching_amplitude = 70                 #[deg]
time_steps_per_cycle = 1000             #[-]
number_of_cycles = 4                    #[-]





import motionProfile as mP

FoilGeo = mP.FoilGeo(chord_length, leading_edge_height, leading_edge_width, trailing_edge_height, trailing_edge_width)
print([FoilGeo])
