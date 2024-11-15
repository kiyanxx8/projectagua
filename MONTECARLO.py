import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Add paths to import custom functions
# Erhalte den aktuellen Pfad der Python-Datei (wo die Datei liegt)
base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(base_dir, 'functions'))
sys.path.insert(0, os.path.join(base_dir, 'uncertainties'))
# Import custom cost and demand functions
from environmental_cost import costenv
from inadequate_water_cost import Cwr
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater
#from All_Parameters import water_min_constraint, water_min, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase

def find_closest_value(df, year, random_value):
    """
    Find the closest value in the DataFrame for a given year and random value.
    
    Parameters:
    df (DataFrame): DataFrame containing values for different years.
    year (int): The year for which to find the closest value.
    random_value (float): Random value to find the closest match.
    
    Returns:
    int: The index of the closest value.
    """
    values = df[year].values
    closest_indices = np.where(values <= random_value)[0]
    closest_index = 0 if len(closest_indices) == 0 else closest_indices[-1]
    return df.index[closest_index]



def monte_carlo_total_cost(iterations, years, population_df, rainamount_df, waterpump_capacities, waterleakage, intervention_cost_df, catchment_area, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False):
    """
    Perform a Monte Carlo simulation to calculate the total cost of water management over a number of years.
    
    Parameters:
    iterations (int): Number of Monte Carlo iterations.
    years (int): Number of years to simulate.
    population_df (DataFrame): DataFrame containing population data for each year.
    rainamount_df (DataFrame): DataFrame containing rainfall data for each year.
    waterpump_capacity (DataFrame): DataFrame containing water pump capacity data.
    waterleakage (DataFrame): DataFrame containing water leakage data.
    intervention_cost_df (DataFrame): DataFrame containing intervention cost data.
    catchment_area (DataFrame): DataFrame containing catchment area data.
    flexible (bool): Whether to apply flexible management strategies.
    
    Returns:
    DataFrames containing total costs, intervention costs, environmental costs, unmet demand costs, and averages for rainfall, population, total demand, water in reservoir, and leakage.
    """
    # Initial parameters
    initial_water = 144000  # ML, initial water reserve
    discount_rate = 0.03  # Discount rate for future costs

    # Initialize arrays to store costs and annual values
    total_costs, intervention_costs, env_costs, unmet_demand_costs = [np.zeros((iterations, years)) for _ in range(4)] # Costs
    rainfall_yearly, population_yearly, total_demand_yearly = [np.zeros((iterations, years)) for _ in range(3)] # Annual values
    water_currently_yearly, leakage_yearly = [np.zeros((iterations, years)) for _ in range(2)] # Annual values

    # Monte Carlo simulation loop
    for i in range(iterations):
        # Generate random values for population and rainfall
        random_value_pop, random_value_rain = np.random.rand(), np.random.rand()
        
        # Copy initial catchment area and water pump capacity
        current_catchment_area = catchment_area.copy()
        current_waterpump_capacity = waterpump_capacities.copy()

        for year in range(1, years + 1):
            # Find the closest values for population and rainfall for the current year
            population = find_closest_value(population_df, year, random_value_pop)
            rainfall = find_closest_value(rainamount_df, year, random_value_rain)
            
            # Set initial water reserve for the first year
            water_currently = initial_water if year == 1 else water_currently2

            # Calculate annual total demand
            total_demand = totaldemand(population, Wpriv, Wrest)

            # Calculate rainfall volume (considering evaporation)
            rainfall_volume = rainfall * 1e-6 * current_catchment_area.at[1, year] * 0.8

            # Retrieve water leakage and water pump capacity for the current year
            leakage = waterleakage.at[1, year]
            waterpump_capacity = current_waterpump_capacity.at[1, year]
            intervention_cost = intervention_cost_df.at[1, year]

            # Compute water amount in reservoir for the current year
            water_currently2 = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand, water_min_constraint)

            # if water reserve is below minimum threshold, set water pump capacity to 0
            if water_currently2 < water_min_constraint:
                waterpump_capacity = 0


            
            # Apply flexible management strategies if enabled
            if flexible:
                # Increase catchment area if water reserve is below minimum threshold and catchment area is below 14,000,000 m^2
                if water_currently2 <= water_min and current_catchment_area.loc[1, year] < 14000000 and year != 1:
                    current_catchment_area.loc[1, year:] += 500000 # Increase catchment area by 500000 m^2
                    intervention_cost += (current_catchment_area.loc[1, year] - current_catchment_area.loc[1, year - 1]) * cost_catchment_area_increase
                # Increase water pump capacity if current capacity is below total demand
                if waterpump_capacity < total_demand:
                    current_waterpump_capacity.loc[1, year:] += 2000 # Increase water pump capacity by 2000 ML/year
                    intervention_cost += (cost_waterpump_capacity_increase * 1000 + operational_cost_waterpump_increase * current_waterpump_capacity.at[1, year])
                    waterpump_capacity = current_waterpump_capacity.at[1, year]
                    # if water reserve is below minimum threshold, set water pump capacity to 0
                    if water_currently2 < water_min_constraint:
                        waterpump_capacity = 0

            # Store annual values
            rainfall_yearly[i, year - 1] = rainfall
            population_yearly[i, year - 1] = population
            total_demand_yearly[i, year - 1] = total_demand
            water_currently_yearly[i, year - 1] = water_currently2
            leakage_yearly[i, year - 1] = leakage

            # Calculate annual costs
            env_cost = costenv(water_currently2, water_min, Env_Cost )  # Environmental cost
            unmet_demand_cost = Cwr(waterpump_capacity, population, total_demand, Wpriv, Wrest, Cpriv, Crest)  # Cost of unmet demand
            total_cost = totalcost(intervention_cost, unmet_demand_cost, env_cost)  # Total cost for the year

            # Store annual costs
            total_costs[i, year - 1] = total_cost
            intervention_costs[i, year - 1] = intervention_cost
            env_costs[i, year - 1] = env_cost
            unmet_demand_costs[i, year - 1] = unmet_demand_cost

    # Calculate present value costs for each iteration
    present_value_costs = np.zeros(iterations)
    present_value_unmet_demand_costs = np.zeros(iterations)
    present_value_envcosts = np.zeros(iterations)
    present_value_intervention_costs = np.zeros(iterations)
    for i in range(iterations):
        for year in range(years):
            present_value_costs[i] += total_costs[i, year] / ((1 + discount_rate) ** year)
            present_value_unmet_demand_costs[i] += unmet_demand_costs[i, year] / ((1 + discount_rate) ** year)
            present_value_envcosts[i] += env_costs[i, year] / ((1 + discount_rate) ** year)
            present_value_intervention_costs[i] += intervention_costs[i, year] / ((1 + discount_rate) ** year)
    
    # Average present value cost across all iterations
    average_present_value_cost = present_value_costs.mean()
    average_present_value_unmet_demand_costs = present_value_unmet_demand_costs.mean()
    average_present_value_envcosts = present_value_envcosts.mean()
    average_present_value_intervention_costs = present_value_intervention_costs.mean()

    # Create DataFrames for the results
    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    intervention_costs_df = pd.DataFrame(intervention_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    env_costs_df = pd.DataFrame(env_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    unmet_demand_costs_df = pd.DataFrame(unmet_demand_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])

    return (
        total_costs_df,
        intervention_costs_df,
        env_costs_df,
        unmet_demand_costs_df,
        rainfall_yearly.mean(axis=0),
        population_yearly.mean(axis=0),
        total_demand_yearly.mean(axis=0),
        water_currently_yearly.mean(axis=0),
        leakage_yearly.mean(axis=0),
        average_present_value_cost,  # New return value for average present value of total cost
        average_present_value_unmet_demand_costs,
        average_present_value_envcosts,
        average_present_value_intervention_costs

    )
