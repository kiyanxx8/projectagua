def rain_to_reservoir(Rain):

    city_area = 21600000  # m², area of zug which has 73000 inhabitants
    catchment_area = 6300000 # m², assumption from email

     # Convert rain from mm to meters for easier volume calculation (1 mm = 0.001 m)
    rain_meters = Rain / 1000
    
      # Calculate the total volume of rain over the city in cubic meters
    total_rain_volume_m3 = rain_meters * city_area
    
    # Calculate the fraction of rain entering the reservoir based on the catchment area
    fraction_to_reservoir = catchment_area / city_area
    
    # Calculate the reservoir volume in cubic meters
    Rainsupply_ML = total_rain_volume_m3 * fraction_to_reservoir * 0.001
    
    # Convert cubic meters to megaliters (1 cubic meter = 0.001 megaliters)
    
    return Rainsupply_ML