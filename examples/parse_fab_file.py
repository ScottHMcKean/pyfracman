from pyfracman.fab import parse_fab_file

fname = "C:/Users/scott.mckean/Desktop/pest_test_1/Scenario_1/Connected fracs/Connected_Fracs_seismic_1.fab"
fab_info = parse_fab_file(fname)
fracture_length = fab_info['property_df'].FractureLength.sum()
fracture_length