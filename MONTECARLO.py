import numpy as np
import pandas as pd
from environmental_cost import costenv
from inadequate_water_cost import Cwr
from Rainfall_supply import rain_to_reservoir
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater
from intervention_cost import Cint

Waterpump_capacity_intervention1 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 1
increase_year = 2
new_capacity = 20000
Waterpump_capacity_intervention1.loc[:, increase_year:] = new_capacity

Waterpump_capacity_intervention2 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 2
Waterpump_capacity_intervention3 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 3

Waterleakage_intervention1 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 1
Waterleakage_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 2
Waterleakage_intervention3 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 3

Cost_intervention1 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 1
Cost_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 2
Cost_intervention3 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 3


def monte_carlo_total_cost(iterations, years, pop_df, rainfall_df, Waterpump_capacity, waterleakage, intervention_cost):
    # Storage for costs across all iterations and years
    # Storage for costs across all iterations and years
    total_costs = np.zeros((iterations, years))
    
    # Constants
    initial_water = 140000  # ML, initial water reserve

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
            
            # Retrieve year-specific values from the DataFrames
            leakage = waterleakage.at[1, year]  # Year-specific leakage
            waterpump_capacity = Waterpump_capacity.at[1, year]  # Year-specific pump capacity
            intervention_cost = intervention_cost.at[1, year]  # Year-specific intervention cost
            
            # 3. Compute Water Balance
            water_currently = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand)
            
            # 4. Calculate Annual Costs
            env_cost = costenv(water_currently)  # Environmental cost
            unmet_demand_cost = Cwr(waterpump_capacity, population, total_demand)  # Unmet water demand cost
            
            # 5. Sum Costs for Total Annual Cost
            total_cost = totalcost(intervention_cost, unmet_demand_cost, env_cost)
            total_costs[i, year - 1] = total_cost  # Store total cost for each year

    # Convert results to DataFrame for easier analysis
    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    return total_costs_df