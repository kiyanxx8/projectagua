import numpy as np
import pandas as pd
#import ace_tools as tools

from environmental_cost import costenv
from inadequate_water_cost import Cwr
from Rainfall_supply import rain_to_reservoir
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater
from pop2 import pop_df
from rainfall import rainfall_cdf_df

Waterpump_capacity_intervention1 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 1
increase_year = 2
new_capacity = 0
Waterpump_capacity_intervention1.loc[:, increase_year:] = new_capacity

Waterpump_capacity_intervention2 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 2
Waterpump_capacity_intervention3 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 3

Waterleakage_intervention1 = pd.DataFrame(730, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 1
Waterleakage_intervention2 = pd.DataFrame(730, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 2
Waterleakage_intervention3 = pd.DataFrame(800, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 3

Cost_intervention1 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 1
Cost_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 2
Cost_intervention3 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 3

def find_closest_value(df, year, random_value):
    # Get the column values for the specified year
    values = df[year].values
    # Find the index of the closest value in values that is less than or equal to random_value
    closest_index = np.where(values <= random_value)[0][-1]
    return df.index[closest_index]  # Return the population or rainfall value at the found index



def monte_carlo_total_cost(iterations, years, population_df, rainamount_df, Waterpump_capacity, waterleakage, intervention_cost_df):
    initial_water = 144000  # ML, initial water reserve
    total_costs = np.zeros((iterations, years))  # Store total costs for each iteration and year

    for i in range(iterations):
        for year in range(1, years + 1):
            random_value_pop = np.random.rand()
            random_value_rain = np.random.rand()

            # Find the closest values in pop_df and rainfall_df for the current year
            population = find_closest_value(population_df, year, random_value_pop)
            rainfall = find_closest_value(rainamount_df, year, random_value_rain)
            print(population, rainfall)
            if year == 1:
                water_currently = initial_water
            else:
                water_currently = water_currently2
            
            # Calculate Annual Variables
            total_demand = totaldemand(population)
            rainfall_volume = rain_to_reservoir(rainfall)
            
            # Retrieve year-specific values from the DataFrames
            leakage = waterleakage.at[1, year]
            waterpump_capacity = Waterpump_capacity.at[1, year]
            intervention_cost = intervention_cost_df.at[1, year]
            
            # Compute Water Balance
            water_currently2 = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand)
            
            # Calculate Annual Costs
            env_cost = costenv(water_currently2)
            unmet_demand_cost = Cwr(waterpump_capacity, population, total_demand)
            
            # Sum Costs for Total Annual Cost
            total_cost = totalcost(intervention_cost, unmet_demand_cost, env_cost)
            total_costs[i, year - 1] = total_cost

    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    return total_costs_df

total_costs_example = monte_carlo_total_cost(5, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention1, Waterleakage_intervention1, Cost_intervention1)
print(total_costs_example.head())