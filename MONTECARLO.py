import numpy as np
import pandas as pd
from environmental_cost import costenv
from inadequate_water_cost import Cwr
from Rainfall_supply import rain_to_reservoir
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater
from intervention_cost import Cint



def monte_carlo_total_cost(iterations, years, pop_df, rainfall_df):
    # Storage for costs across all iterations and years
    total_costs = np.zeros((iterations, years))
    
    # Constants and parameters
    leakage = 500  # ML, assumed leakage value per year
    waterpump_capacity = 150000  # ML, assumed water pump capacity per year
    initial_water = 140000  # ML, initial water reserve
    intervention_factor = 10000  # Assumed intervention cost factor

    # Monte Carlo simulation
    for i in range(iterations):
        # Reset water amount for each new iteration
        water_currently = initial_water
        
        for year in range(1, years + 1):
            # 1. Population and Rainfall Sampling
            population = np.random.choice(pop_df.index, p=pop_df[year] / pop_df[year].sum())
            rainfall = np.random.choice(rainfall_df.index, p=rainfall_df[year] / rainfall_df[year].sum())
            
            # 2. Calculate Annual Variables
            total_demand = totaldemand(population)
            rainfall_volume = rain_to_reservoir(rainfall)
            
            # 3. Compute Water Balance
            water_currently = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand)
            
            # 4. Calculate Annual Costs
            Cenv = costenv(water_currently)  # Environmental cost
            Cwr = Cwr(waterpump_capacity, population, total_demand)  # Unmet water demand cost
            Cint = Cint(1)  # Intervention cost, simplified to 1 for example purposes
            
            # 5. Sum Costs for Total Annual Cost
            total_cost = totalcost(Cint, Cwr, Cenv)
            total_costs[i, year - 1] = total_cost  # Store total cost for each year

    # Convert results to DataFrame for easier analysis
    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    return total_costs_df

# Placeholder to call monte_carlo_total_cost and show its output structure
# For real application, replace `pop_df` and `rainfall_df` with actual DataFrames
example_pop_df = pd.DataFrame(np.random.rand(100, 50), index=np.linspace(1000, 5000, 100), columns=np.arange(1, 51))
example_rainfall_df = pd.DataFrame(np.random.rand(100, 50), index=np.linspace(800, 1200, 100), columns=np.arange(1, 51))
iterations = 10  # Example with 10 iterations
years = 50  # 50-year forecast

# Run the Monte Carlo simulation with example data
total_costs_example = monte_carlo_total_cost(iterations, years, example_pop_df, example_rainfall_df)
import ace_tools as tools; tools.display_dataframe_to_user(name="Monte Carlo Total Costs Example", dataframe=total_costs_example)