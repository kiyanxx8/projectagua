import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import ace_tools as tools

from environmental_cost import costenv
from inadequate_water_cost import Cwr
from Rainfall_supply import rain_to_reservoir
from TotalCost import totalcost
from TotalDemand import totaldemand
from water_in_reservoir import totwater
from pop import pop_df
from rainfall import rainfall_cdf_df


Waterpump_capacity_nothing = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 1
Waterpump_capacity_intervention1 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 1
increase_year = 1
new_capacity = 17000
Waterpump_capacity_intervention1.loc[:, increase_year:] = new_capacity

Waterpump_capacity_intervention2 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 2
Waterpump_capacity_intervention3 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATERPUMP CAPACITY FOR EACH YEAR IN INTERVENTION 3
increase_year2 = 20
new_capacity2 = 15000
Waterpump_capacity_intervention3.loc[:, increase_year2:] = new_capacity2
increase_year3 = 40
new_capacity3 = 17000
Waterpump_capacity_intervention3.loc[:, increase_year3:] = new_capacity3



i = 50
Waterleakage_nothing = pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))
Waterleakage_intervention1 =pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 1
Waterleakage_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 2
Waterleakage_intervention3 = pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))  #THIS IS A DATAFRAME SHOWING THE WATER LEAKAGE FOR EACH YEAR IN INTERVENTION 3

Cost_nothing = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_intervention1 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 1
Cost_intervention1[1] = 8000000
Cost_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 2
Cost_intervention2[2] = 5000000
Cost_intervention3 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))  #THIS IS A DATAFRAME SHOWING THE COST FOR EACH Intervention in every YEAR IN INTERVENTION 3
Cost_intervention3[20] = 5000000
Cost_intervention3[40] = 4000000

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

def calculate_discounted_total_costs(total_costs_df, discount_rate):
    discounted_total_costs = total_costs_df.apply(
        lambda x: sum(x[f'Year_{y}'] / (1 + discount_rate) ** y for y in range(1, len(x) + 1)),
        axis=1
    )
    return discounted_total_costs

def monte_carlo_total_cost(iterations, years, population_df, rainamount_df, Waterpump_capacity, waterleakage, intervention_cost_df):
    initial_water = 144000  # ML, initial water reserve
    total_costs = np.zeros((iterations, years))
    intervention_costs = np.zeros((iterations, years))
    env_costs = np.zeros((iterations, years))
    unmet_demand_costs = np.zeros((iterations, years))
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
            rainfall_volume = rain_to_reservoir(rainfall)
            #print("year:" + str(year) + ", totdemand:" + str(total_demand) + ", " + str(population))
            # Retrieve year-specific values from the DataFrames
            leakage = waterleakage.at[1, year]
            waterpump_capacity = Waterpump_capacity.at[1, year]
            intervention_cost = intervention_cost_df.at[1, year]

            # Compute Water Balance
            water_currently2 = totwater(water_currently, rainfall_volume, leakage, waterpump_capacity, total_demand)
            
            # Calculate Annual Costs
            env_cost = costenv(water_currently2)
            unmet_demand_cost = Cwr(waterpump_capacity, population, total_demand)
            #print("unmet_demand_cost:" + str(unmet_demand_cost))
            #print("env_cost:" + str(env_cost))
            # Sum Costs for Total Annual Cost
            total_cost = totalcost(intervention_cost, unmet_demand_cost, env_cost)
            total_costs[i, year - 1] = total_cost

    total_costs_df = pd.DataFrame(total_costs, columns=[f'Year_{y}' for y in range(1, years + 1)])
    return total_costs_df




total_costs_example1 = monte_carlo_total_cost(1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_nothing, Waterleakage_nothing, Cost_nothing)
total_costs_example2 = monte_carlo_total_cost(1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention1, Waterleakage_intervention1, Cost_intervention1)
total_costs_example3 = monte_carlo_total_cost(1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention2, Waterleakage_intervention2, Cost_intervention2)
total_costs_example4 = monte_carlo_total_cost(1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention3, Waterleakage_intervention3, Cost_intervention3)
#print(total_costs_example.head())


discount_rate = 0.05
discounted_total_costs_example1 = calculate_discounted_total_costs(total_costs_example1, discount_rate)
discounted_total_costs_example2 = calculate_discounted_total_costs(total_costs_example2, discount_rate)
discounted_total_costs_example3 = calculate_discounted_total_costs(total_costs_example3, discount_rate)
discounted_total_costs_example4 = calculate_discounted_total_costs(total_costs_example4, discount_rate)
# Sort the costs for cumulative distribution for each intervention
sorted_costs1 = np.sort(discounted_total_costs_example1)
cumulative_probs1 = np.linspace(0, 1, len(sorted_costs1))

sorted_costs2 = np.sort(discounted_total_costs_example2)
cumulative_probs2 = np.linspace(0, 1, len(sorted_costs2))

sorted_costs3 = np.sort(discounted_total_costs_example3)
cumulative_probs3 = np.linspace(0, 1, len(sorted_costs3))

sorted_costs4 = np.sort(discounted_total_costs_example4)
cumulative_probs4 = np.linspace(0, 1, len(sorted_costs4))

# Plotting the cumulative distribution for both interventions
plt.figure(figsize=(10, 6))
plt.plot(sorted_costs1, cumulative_probs1, marker='o', linestyle='-', color='blue', label='Intervention 1')
plt.plot(sorted_costs2, cumulative_probs2, marker='x', linestyle='-', color='red', label='Intervention 2')
plt.plot(sorted_costs3, cumulative_probs3, marker='s', linestyle='-', color='green', label='Intervention 3')
plt.plot(sorted_costs4, cumulative_probs4, marker='d', linestyle='-', color='purple', label='Intervention 4')
# Labeling the axes and adding a title
plt.xlabel('Total Discounted Cost')
plt.ylabel('Cumulative Probability')
plt.title('Cumulative Distribution of Total Discounted Costs for Different Interventions')
plt.legend()
plt.grid(True)
plt.show()