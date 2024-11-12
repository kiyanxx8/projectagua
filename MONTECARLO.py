import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Add paths to import custom functions
sys.path.insert(0, r'C:/Users/kizal/Everything/ETH_local/Semester1/infra_Planning/projectagua/projectagua/functions')
sys.path.insert(0, r'C:/Users/kizal/Everything/ETH_local/Semester1/infra_Planning/projectagua/projectagua/uncertainties')

# Import custom cost and demand functions
from environmental_cost import costenv
from inadequate_water_cost import Cwr
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater

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

### Do afach de montecarlo ahluege eb det alles sinn macht, vorallem de " if flexible" part wo flexibli intervention cost berechnet wird

def monte_carlo_total_cost(iterations, years, population_df, rainamount_df, waterpump_capacities, waterleakage, intervention_cost_df, catchment_area, flexible=False):
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
    water_min = 136800  # ML, minimum water threshold for intervention
    water_min_constraint = 72000  # ML, critical minimum water level
    cost_catchment_area_increase = 50  # Cost per unit increase in catchment area
    cost_waterpump_capacity_increase = 100  # Cost per unit increase in water pump capacity
    operational_cost_waterpump_increase = 5  # Operational cost per unit increase in water pump capacity

    # Initialize arrays to store costs and annual values
    total_costs, intervention_costs, env_costs, unmet_demand_costs = [np.zeros((iterations, years)) for _ in range(4)]
    rainfall_yearly, population_yearly, total_demand_yearly = [np.zeros((iterations, years)) for _ in range(3)]
    water_currently_yearly, leakage_yearly = [np.zeros((iterations, years)) for _ in range(2)]

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
            total_demand = totaldemand(population)

            # Calculate rainfall volume (considering evaporation)
            rainfall_volume = rainfall * 1e-6 * current_catchment_area.at[1, year] * 0.8

            # Retrieve water leakage and water pump capacity for the current year
            leakage = waterleakage.at[1, year]
            waterpump_capacity = current_waterpump_capacity.at[1, year]
            intervention_cost = intervention_cost_df.at[1, year]

            # Compute water balance for the current year
            water_currently2 = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand)

            # if water reserve is below minimum threshold, set water pump capacity to 0
            if water_currently2 < water_min_constraint:
                waterpump_capacity = 0


            ### de au ahluege
            # Apply flexible management strategies if enabled
            if flexible:
                # Increase catchment area if water reserve is below minimum threshold
                if water_currently2 <= water_min and current_catchment_area.loc[1, year] < 14000000:
                    current_catchment_area.loc[1, year:] += 500000
                    intervention_cost += (current_catchment_area.loc[1, year] - current_catchment_area.loc[1, year - 1]) * cost_catchment_area_increase
                # Increase water pump capacity if current capacity is below total demand
                if waterpump_capacity < total_demand:
                    current_waterpump_capacity.loc[1, year:] += 2000
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
            env_cost = costenv(water_currently2)  # Environmental cost
            unmet_demand_cost = Cwr(waterpump_capacity, population, total_demand)  # Cost of unmet demand
            total_cost = totalcost(intervention_cost, unmet_demand_cost, env_cost)  # Total cost for the year

            # Store annual costs
            total_costs[i, year - 1] = total_cost
            intervention_costs[i, year - 1] = intervention_cost
            env_costs[i, year - 1] = env_cost
            unmet_demand_costs[i, year - 1] = unmet_demand_cost

    # Create DataFrames for the results
    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    intervention_costs_df = pd.DataFrame(intervention_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    env_costs_df = pd.DataFrame(env_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    unmet_demand_costs_df = pd.DataFrame(unmet_demand_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])

    return total_costs_df, intervention_costs_df, env_costs_df, unmet_demand_costs_df, rainfall_yearly.mean(axis=0), population_yearly.mean(axis=0), total_demand_yearly.mean(axis=0), water_currently_yearly.mean(axis=0), leakage_yearly.mean(axis=0)
