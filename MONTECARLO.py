import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
#import ace_tools as tools
sys.path.insert(0, r'C:/Users/kizal/Everything/ETH_local/Semester1/infra_Planning/projectagua/projectagua/functions')
sys.path.insert(0, r'C:/Users/kizal/Everything/ETH_local/Semester1/infra_Planning/projectagua/projectagua/uncertainties')
print(sys.path)

from environmental_cost import costenv
from inadequate_water_cost import Cwr
from Rainfall_supply import rain_to_reservoir
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater



def find_closest_value(df, year, random_value):
    # Get the column values for the specified year
    values = df[year].values
    # Find indices of values that are less than or equal to random_value
    closest_indices = np.where(values <= random_value)[0]
    # If there are no values less than or equal to random_value, return the first value in the year
    if len(closest_indices) == 0:
        closest_index = 0
    else:
        closest_index = closest_indices[-1]
    return df.index[closest_index]  # Return the population or rainfall value at the found index

def monte_carlo_total_cost(iterations, years, population_df, rainamount_df, Waterpump_capacity, waterleakage, intervention_cost_df, catchment_area):
    initial_water = 144000  # ML, initial water reserve

    total_costs = np.zeros((iterations, years))
    intervention_costs = np.zeros((iterations, years))
    env_costs = np.zeros((iterations, years))
    unmet_demand_costs = np.zeros((iterations, years))

    rainfall_yearly = np.zeros((iterations, years))
    population_yearly = np.zeros((iterations, years))
    total_demand_yearly = np.zeros((iterations, years))
    water_currently_yearly = np.zeros((iterations, years))

    for i in range(iterations):
        random_value_pop = np.random.rand()
        random_value_rain = np.random.rand()
        for year in range(1, years + 1):
            
            #print(random_value_pop, random_value_rain)
            # Find the closest values in pop_df and rainfall_df for the current year
            population = find_closest_value(population_df, year, random_value_pop)
            rainfall = find_closest_value(rainamount_df, year, random_value_rain)
            #print(population, rainfall)
            if year == 1:
                water_currently = initial_water
            else:
                water_currently = water_currently2
            
            # Calculate Annual Variables
            total_demand = totaldemand(population)
            rainfall_volume = rainfall * 0.000001 * catchment_area.at[1, year]
            #print("year:" + str(year) + ", totdemand:" + str(total_demand) + ", " + str(population))
            # Retrieve year-specific values from the DataFrames
            leakage = waterleakage.at[1, year]
            waterpump_capacity = Waterpump_capacity.at[1, year]
            intervention_cost = intervention_cost_df.at[1, year]

            # Compute Water Balance
            water_currently2 = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand)
            
            rainfall_yearly[i, year - 1] = rainfall
            population_yearly[i, year - 1] = population
            total_demand_yearly[i, year - 1] = total_demand
            water_currently_yearly[i, year - 1] = water_currently2

            # Calculate Annual Costs
            env_cost = costenv(water_currently2)
            unmet_demand_cost = Cwr(waterpump_capacity, population, total_demand)
            #print("unmet_demand_cost:" + str(unmet_demand_cost))
            #print("env_cost:" + str(env_cost))
            # Sum Costs for Total Annual Cost
            total_cost = totalcost(intervention_cost, unmet_demand_cost, env_cost)
            total_costs[i, year - 1] = total_cost

            total_costs[i, year - 1] = total_cost
            intervention_costs[i, year - 1] = intervention_cost
            env_costs[i, year - 1] = env_cost
            unmet_demand_costs[i, year - 1] = unmet_demand_cost

    avg_rainfall = rainfall_yearly.mean(axis=0)
    avg_population = population_yearly.mean(axis=0)
    avg_total_demand = total_demand_yearly.mean(axis=0)
    avg_water_currently = water_currently_yearly.mean(axis=0)

    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    intervention_costs_df = pd.DataFrame(intervention_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    env_costs_df = pd.DataFrame(env_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    unmet_demand_costs_df = pd.DataFrame(unmet_demand_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])

    return total_costs_df, intervention_costs_df, env_costs_df, unmet_demand_costs_df, avg_rainfall, avg_population, avg_total_demand, avg_water_currently


