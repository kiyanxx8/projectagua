import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MONTECARLO import monte_carlo_total_cost
from TotalDemand import totaldemand
from inadequate_water_cost import Cwr
from uncertainties.pop import pop_df
from uncertainties.rainfall import rainfall_cdf_df
from Interventions_sensitivity import Waterpump_capacity_robust, Waterleakage_robust, Cost_robust, catchment_area_robust
from All_Parameters import water_min, water_min_constraint, Env_Cost, Wpriv, Wrest, Cpriv, Crest, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase
# Initial parameters
parameters = {
    "cost_catchment_area_increase": 50,
    "cost_waterpump_capacity_increase": 100,
    "operational_cost_waterpump_increase": 5,
    "Wpriv": 0.089,  # ML/person/year for private water use
    "Cpriv": 730  # CHF/person/year for private cost
}

def calculate_average_cost(params):
    # Update relevant parameters
    cost_catchment_area_increase = params["cost_catchment_area_increase"]
    cost_waterpump_capacity_increase = params["cost_waterpump_capacity_increase"]
    operational_cost_waterpump_increase = params["operational_cost_waterpump_increase"]
    Wpriv = params["Wpriv"]
    Cpriv = params["Cpriv"]

    # Run Monte Carlo simulation with updated parameters
    total_costs, _, _, _, _, _, _, _, _, average_present_value_cost = monte_carlo_total_cost(
        100, 50, pop_df, rainfall_cdf_df,
        Waterpump_capacity_robust, Waterleakage_robust, Cost_robust, catchment_area_robust,
        cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase,
        Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
    )
    print(average_present_value_cost)

    return average_present_value_cost

# Get base cost
base_cost = calculate_average_cost(parameters)
print(f"Base cost: {base_cost}")

# Sensitivity analysis
sensitivity_results = {}
for param in parameters:
    original_value = parameters[param]
    
    # Increase parameter by 50%
    parameters[param] = original_value * 1.5
    increased_cost = calculate_average_cost(parameters)
    
    # Decrease parameter by 50%
    parameters[param] = original_value * 0.5
    decreased_cost = calculate_average_cost(parameters)
    
    # Restore original value
    parameters[param] = original_value
    
    # Calculate change in average cost
    sensitivity_results[param] = {
        "Increased": increased_cost - base_cost,
        "Decreased": decreased_cost - base_cost
    }

# Create a DataFrame for results
sensitivity_df = pd.DataFrame(sensitivity_results).T
sensitivity_df.columns = ["Cost Increase (50%)", "Cost Decrease (50%)"]
print(sensitivity_df)

# Plot a Tornado Diagram
plt.figure(figsize=(10, 6))
sensitivity_df.sort_values(by="Cost Increase (50%)", inplace=True)  # Sort by effect size
sensitivity_df.plot(kind='barh', color=['red', 'green'], alpha=0.7, edgecolor='black')
plt.title('Tornado Diagram of Sensitivity Analysis')
plt.xlabel('Change in Average Cost')
plt.ylabel('Parameter')
plt.grid(axis='x')
plt.show()

