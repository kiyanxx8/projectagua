import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from MONTECARLO import monte_carlo_total_cost
from TotalDemand import totaldemand
from inadequate_water_cost import Cwr
from uncertainties.pop import pop_df
from uncertainties.rainfall import rainfall_cdf_df
from Interventions_sensitivity import Waterpump_capacity_stagewise, Waterleakage_stagewise, Cost_stagewise, catchment_area_stagewise
from All_Parameters import water_min, water_min_constraint, Env_Cost, Wpriv, Wrest, Cpriv, Crest, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase
from Interventions_and_plots import cost_fixing_leakage, waterpump_increase_stagewise1, waterpump_increase_stagewise2, waterpumpcapacity_zero, catchment_increase_stagewise1, catchment_increase_stagewise2, catchment_area_zero

print(Cost_stagewise)
# Initial parameters
parameters = {
    "Private residence Cost per person": 730,  # CHF/person/year for private cost
    "Cost Catchment Area increase": 50,
    "Cost Waterpumpcapacity increase": 100,
    "Cost Operational Waterpump increase": 5,
    "Demand per person": 0.089  # ML/person/year for private water use
    
}

def calculate_average_cost(params, Cost_stagewise):
    # Update relevant parameters
    cost_catchment_area_increase = params["Cost Catchment Area increase"]
    cost_waterpump_capacity_increase = params["Cost Waterpumpcapacity increase"]
    operational_cost_waterpump_increase = params["Cost Operational Waterpump increase"]
    Cost_stagewise2 = Cost_stagewise.copy()


    Cost_stagewise2[1] = cost_fixing_leakage + cost_catchment_area_increase * (catchment_increase_stagewise1 - catchment_area_zero)
    Cost_stagewise2[20] = cost_catchment_area_increase * (catchment_increase_stagewise2 - catchment_increase_stagewise1)
    Cost_stagewise2[25] = cost_waterpump_capacity_increase * (waterpump_increase_stagewise1 - waterpumpcapacity_zero)
    Cost_stagewise2[33] = cost_waterpump_capacity_increase * (waterpump_increase_stagewise2 - waterpump_increase_stagewise1)
    Cost_stagewise2 += operational_cost_waterpump_increase * Waterpump_capacity_stagewise

    Wpriv = params["Demand per person"]
    Cpriv = params["Private residence Cost per person"]
    np.random.seed(42)
    # Run Monte Carlo simulation with updated parameters
    total_costs, _, _, _, _, _, _, _, _, average_present_value_cost, _, _, _ = monte_carlo_total_cost(
        5000, 50, pop_df, rainfall_cdf_df,
        Waterpump_capacity_stagewise, Waterleakage_stagewise, Cost_stagewise2, catchment_area_stagewise, 
        cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase,
        Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
    )
    print(average_present_value_cost)

    return average_present_value_cost

# Get base cost
base_cost = calculate_average_cost(parameters, Cost_stagewise)
print(f"Base cost: {base_cost}")

# Sensitivity analysis
sensitivity_results = {}
for param in parameters:
    
    original_value = parameters[param]
    
    # Increase parameter by 50%
    parameters[param] = original_value * 1.5
    increased_cost = calculate_average_cost(parameters, Cost_stagewise)
    print(increased_cost)
    # Decrease parameter by 50%
    parameters[param] = original_value * 0.5
    decreased_cost = calculate_average_cost(parameters, Cost_stagewise)
    print(decreased_cost)
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

def improved_tornado_plot_centered_swap(sensitivity_df):
    # Calculate the max absolute value across both increase and decrease columns for dynamic scaling
    max_value = sensitivity_df[['Cost Increase (50%)', 'Cost Decrease (50%)']].abs().max().max()
    x_min, x_max = -1.1 * max_value, 1.1 * max_value

    # Wrap long labels to fit in two lines
    sensitivity_df.index = [textwrap.fill(label, width=20) for label in sensitivity_df.index]
    
    # Calculate the absolute impact by adding the absolute values of both columns
    sensitivity_df['Abs Impact'] = sensitivity_df['Cost Increase (50%)'].abs() + sensitivity_df['Cost Decrease (50%)'].abs()
    
    # Sort by absolute impact in descending order for tornado effect
    sensitivity_df.sort_values(by='Abs Impact', ascending=True, inplace=True)
    sensitivity_df.drop(columns=['Abs Impact'], inplace=True)

    # Plot tornado diagram with specified figure size
    ax = sensitivity_df.plot(kind='barh', figsize=(12, 8), color=['red', 'blue'], alpha=0.7, edgecolor='black', width=0.8)

    # Title and labels
    plt.title('', fontsize=18, weight='bold', pad=20)
    # plt.suptitle('The Robust Intervention', fontsize=16, style='italic', y=1.05)
    plt.xlabel('Change in Average Cost', fontsize=14, labelpad=15)
    plt.ylabel('Parameter', fontsize=14)

    # Apply fixed x-axis limits between -425M and 425M
    ax.set_xlim(-500e6, 500e6)  # 425 million in scientific notation

    # Grid adjustments
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Move legend inside the plot area
    ax.legend(loc='lower right', frameon=True, framealpha=0.9, title='Sensitivity', fontsize=12)

    # Simplify x-axis number formatting for readability
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.0f}M'))

    # Adjust layout to center plot and make it balanced
    plt.tight_layout(pad=2.0)

    # Save the figure in high resolution
    plt.savefig("Stagewise Analysis.png", format="png", dpi=300, bbox_inches="tight")
    plt.show()
    
# Assuming 'sensitivity_df' is your DataFrame with relevant data
improved_tornado_plot_centered_swap(sensitivity_df)
