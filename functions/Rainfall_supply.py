def rain_to_reservoir(Rain):

    catchment_area = 6300000 # m², assumption from email

     # Convert rain from mm to meters for easier volume calculation (1 mm = 0.001 m)
    rain_meters = Rain / 1000

    
    # Calculate the reservoir volume in cubic meters
    Rainsupply_ML = rain_meters * catchment_area * 0.001
    
    # Convert cubic meters to megaliters (1 cubic meter = 0.001 megaliters)
    
    return Rainsupply_ML