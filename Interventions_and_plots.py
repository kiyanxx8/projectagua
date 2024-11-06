import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from MONTECARLO import monte_carlo_total_cost  # Import the monte_carlo function from the other file
from uncertainties.pop import pop_df
from uncertainties.rainfall import rainfall_cdf_df

years = np.arange(1, 51)
discount_rate = 0.05


#INTERVENTIONS
# Define intervention-specific DataFrames for water pump capacity
Waterpump_capacity_nothing = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_intervention1 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))
increase_year = 1
new_capacity = 17000
Waterpump_capacity_intervention1.loc[:, increase_year:] = new_capacity

catchment_area_nothing = pd.DataFrame(6300000, index=[1], columns=np.arange(1, 51))
catchment_area_intervention1 = pd.DataFrame(12000000, index=[1], columns=np.arange(1, 51))
catchment_area_intervention2 = pd.DataFrame(6300000, index=[1], columns=np.arange(1, 51))
catchment_area_intervention3 = pd.DataFrame(6300000, index=[1], columns=np.arange(1, 51))


Waterpump_capacity_intervention2 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_intervention3 = pd.DataFrame(13870, index=[1], columns=np.arange(1, 51))
increase_year2 = 20
new_capacity2 = 15000
Waterpump_capacity_intervention3.loc[:, increase_year2:] = new_capacity2
increase_year3 = 40
new_capacity3 = 17000
Waterpump_capacity_intervention3.loc[:, increase_year3:] = new_capacity3

# Define DataFrames for water leakage
i = 50
Waterleakage_nothing = pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))
Waterleakage_intervention1 = pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))
Waterleakage_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Waterleakage_intervention3 = pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))

# Define DataFrames for intervention costs
Cost_nothing = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_intervention1 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_intervention1[1] = 8000000
Cost_intervention2 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_intervention2[2] = 5000000
Cost_intervention3 = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_intervention3[20] = 5000000
Cost_intervention3[40] = 4000000






# Function to calculate discounted total costs
def calculate_cumulative_distribution(costs_df, discount_rate):
    discounted_costs = costs_df.apply(lambda x: sum(x[f'Year_{y}'] / (1 + discount_rate) ** y for y in range(1, len(x) + 1)), axis=1)
    sorted_costs = np.sort(discounted_costs)
    cumulative_probs = np.linspace(0, 1, len(sorted_costs))

    return sorted_costs, cumulative_probs




# Run Monte Carlo simulations for each intervention
total_costs1, intervention_costs1, env_costs1, unmet_demand_costs1, avg_rainfall1, avg_population1, avg_total_demand1, avg_water_currently1 = monte_carlo_total_cost(
    1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_nothing, Waterleakage_nothing, Cost_nothing, catchment_area_nothing
)
total_costs2, intervention_costs2, env_costs2, unmet_demand_costs2, _, _, _, avg_water_currently2 = monte_carlo_total_cost(
    1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention1, Waterleakage_intervention1, Cost_intervention1, catchment_area_intervention1
)
total_costs3, intervention_costs3, env_costs3, unmet_demand_costs3, _, _, _, avg_water_currently3 = monte_carlo_total_cost(
    1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention2, Waterleakage_intervention2, Cost_intervention2, catchment_area_intervention2
)
total_costs4, intervention_costs4, env_costs4, unmet_demand_costs4, _, _, _, avg_water_currently4 = monte_carlo_total_cost(
    1000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_intervention3, Waterleakage_intervention3, Cost_intervention3, catchment_area_intervention3
)

with PdfPages('all_interventions_costs.pdf') as pdf:
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([total_costs1, total_costs2, total_costs3, total_costs4], 
                                            ['Intervention 1', 'Intervention 2', 'Intervention 3', 'Intervention 4'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Total Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Total Discounted Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Intervention Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([intervention_costs1, intervention_costs2, intervention_costs3, intervention_costs4], 
                                            ['Intervention 1', 'Intervention 2', 'Intervention 3', 'Intervention 4'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Intervention Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Intervention Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Environmental Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([env_costs1, env_costs2, env_costs3, env_costs4], 
                                            ['Intervention 1', 'Intervention 2', 'Intervention 3', 'Intervention 4'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Environmental Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Environmental Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Unmet Demand Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([unmet_demand_costs1, unmet_demand_costs2, unmet_demand_costs3, unmet_demand_costs4], 
                                            ['Intervention 1', 'Intervention 2', 'Intervention 3', 'Intervention 4'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Unmet Demand Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Unmet Demand Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure


    # Plot Intervention 1 parameters over the years
    # Average Rainfall
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_rainfall1, label='Average Rainfall', color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Rainfall Amount')
    plt.title('Average Rainfall over Years for Intervention 1')
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Average Population
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_population1, label='Average Population', color='orange')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title('Average Population over Years for Intervention 1')
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Average Total Demand
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_total_demand1, label='Average Total Demand', color='green')
    plt.xlabel('Year')
    plt.ylabel('Total Demand')
    plt.title('Average Total Demand over Years for Intervention 1')
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Plot 4: Average Water Currently in Reservoir over Years for all Interventions
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_water_currently1, label='Intervention 1', color='skyblue')
    plt.plot(years, avg_water_currently2, label='Intervention 2', color='orange')
    plt.plot(years, avg_water_currently3, label='Intervention 3', color='green')
    plt.plot(years, avg_water_currently4, label='Intervention 4', color='purple')
    plt.xlabel('Year')
    plt.ylabel('Water Currently in Reservoir')
    plt.title('Average Water Currently in Reservoir over Years for All Interventions')
    plt.legend()
    plt.grid(True)
    #plt.show()
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure


