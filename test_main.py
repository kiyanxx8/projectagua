

# Import the function from the file `rain_calculator.py`
from Rainfall_supply import rain_to_reservoir

# Define input parameters
rain_mm = 1100  # Annual rainfall in mm


# Call the function and print the result
volume_ml = rain_to_reservoir(rain_mm)
print(f"The volume of water entering the reservoir is {volume_ml:.2f} ML.")