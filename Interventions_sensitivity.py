import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from MONTECARLO import monte_carlo_total_cost  # Import the monte_carlo function from the other file
from uncertainties.pop import pop_df
from uncertainties.rainfall import rainfall_cdf_df
from All_Parameters import water_min, water_min_constraint, Env_Cost, Wpriv, Wrest, Cpriv, Crest, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase

### Do chasch ahfange

# Set up parameters
years = np.arange(1, 51)
discount_rate = 0.03

# Initial conditions
waterpumpcapacity_zero = 13870  # Initial water pump capacity in ML/year
leakage_zero = 730  # Initial water leakage in ML/year
catchment_area_zero = 6300000  # Initial catchment area in m^2

# Intervention parameters
catchment_area_new_robust = 13000000  # New catchment area after robust intervention in m^2
cost_fixing_leakage = 1000000  # Cost of fixing water leakage in $

# Water pump capacity after interventions
waterpump_increase_robust = 17500  # After robust intervention in ML/year
waterpump_increase_stagewise1 = 15000  # After stagewise intervention (stage 1) in ML/year
waterpump_increase_stagewise2 = 17500  # After stagewise intervention (stage 2) in ML/year

# Catchment area after stagewise interventions
catchment_increase_stagewise1 = 9700000  # After stagewise intervention (stage 1) in m^2
catchment_increase_stagewise2 = 11500000  # After stagewise intervention (stage 2) in m^2
catchment_increase_flexible = 9250000  # After flexible intervention in m^2

# Define intervention-specific DataFrames for water pump capacity
Waterpump_capacity_nothing = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))

Waterpump_capacity_robust = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_robust.loc[:, 1:] = waterpump_increase_robust

Waterpump_capacity_stagewise = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_stagewise.loc[:, 25:] = waterpump_increase_stagewise1 #
Waterpump_capacity_stagewise.loc[:, 33:] = waterpump_increase_stagewise2

Waterpump_capacity_flexible = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))

# Define DataFrames for catchment area
catchment_area_nothing = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))

catchment_area_robust = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_robust.loc[:, 1:] = catchment_area_new_robust

catchment_area_stagewise = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_stagewise.loc[:, 1:] = catchment_increase_stagewise1
catchment_area_stagewise.loc[:, 20:] = catchment_increase_stagewise2

catchment_area_flexible = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_flexible.loc[:, 1:] = catchment_increase_flexible

# Define DataFrames for water leakage
i = 50  # Number of years
Waterleakage_nothing = pd.DataFrame([[leakage_zero + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))

Waterleakage_robust = Waterleakage_nothing.copy()
for year in range(1, i + 1):
    Waterleakage_robust.loc[1, year] = 10 * (year - 1)  # Set to 0 at fix_year and increase by 10 each year

Waterleakage_stagewise = Waterleakage_robust.copy()

Waterleakage_flexible = Waterleakage_robust.copy()


# Define DataFrames for intervention costs
Cost_nothing = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_nothing += operational_cost_waterpump_increase * Waterpump_capacity_nothing

Cost_robust = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_robust[1] = (cost_fixing_leakage + 
                       cost_waterpump_capacity_increase * (waterpump_increase_robust - waterpumpcapacity_zero) + 
                       cost_catchment_area_increase * (catchment_area_new_robust - catchment_area_zero))
Cost_robust += operational_cost_waterpump_increase * Waterpump_capacity_robust

Cost_stagewise = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_stagewise[1] = cost_fixing_leakage + cost_catchment_area_increase * (catchment_increase_stagewise1 - catchment_area_zero)
Cost_stagewise[20] = cost_catchment_area_increase * (catchment_increase_stagewise2 - catchment_increase_stagewise1)
Cost_stagewise[25] = cost_waterpump_capacity_increase * (waterpump_increase_stagewise1 - waterpumpcapacity_zero)
Cost_stagewise[33] = cost_waterpump_capacity_increase * (waterpump_increase_stagewise2 - waterpump_increase_stagewise1)
Cost_stagewise += operational_cost_waterpump_increase * Waterpump_capacity_stagewise

Cost_flexible = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_flexible[1] = cost_fixing_leakage + cost_catchment_area_increase * (catchment_increase_flexible - catchment_area_zero)

# Function to calculate discounted total costs
def calculate_cumulative_distribution(costs_df, discount_rate):
    discounted_costs = costs_df.apply(lambda x: sum(x[f'Year_{y}'] / (1 + discount_rate) ** y for y in range(1, len(x) + 1)), axis=1)
    sorted_costs = np.sort(discounted_costs)
    cumulative_probs = np.linspace(0, 1, len(sorted_costs))
    return sorted_costs, cumulative_probs


### Do chasch ufhöre


# Run Monte Carlo simulations for each intervention
total_costs1, nothing_costs1, env_costs1, unmet_demand_costs1, avg_rainfall1, avg_population1, avg_total_demand1, avg_water_currently1, avg_leakage_nothing, average_total_costs1, _, _, _ = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_nothing, Waterleakage_nothing, Cost_nothing, catchment_area_nothing, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
) # Run Monte Carlo simulation for the zero-case scenario
total_costs2, intervention_costs2, env_costs2, unmet_demand_costs2, _, _, _, avg_water_currently2, avg_leakage_robust , average_total_costs2, _, _, _= monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_robust, Waterleakage_robust, Cost_robust, catchment_area_robust, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
) # Run Monte Carlo simulation for the robust intervention
total_costs3, intervention_costs3, env_costs3, unmet_demand_costs3, _, _, _, avg_water_currently3, avg_leakage_stagewise, average_total_costs3, _, _, _ = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_stagewise, Waterleakage_stagewise, Cost_stagewise, catchment_area_stagewise, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
) # Run Monte Carlo simulation for the stagewise intervention
total_costs4, intervention_costs4, env_costs4, unmet_demand_costs4, _, _, _, avg_water_currently4, avg_leakage_flexible, average_total_costs4, _, _, _ = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_flexible, Waterleakage_flexible, Cost_flexible, catchment_area_flexible, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=True
)

# Generate plots and save to PDF

# Hole den Namen der aktuellen Datei (ohne den Pfad) und ändere die Endung auf '.pdf'
pdf_filename = os.path.splitext(os.path.basename(__file__))[0] + '.pdf'

# Generiere das PDF mit dem erstellten Dateinamen
with PdfPages(pdf_filename) as pdf:
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([total_costs1, total_costs2, total_costs3, total_costs4], 
                                            ['Zero-Case', 'robust', 'Stagewise', 'Flexible'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Total Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Total Discounted Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Intervention Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([nothing_costs1, intervention_costs2, intervention_costs3, intervention_costs4], 
                                            ['Zero-Case', 'robust', 'Stagewise', 'Flexible'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Intervention Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Intervention Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Environmental Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([env_costs1, env_costs2, env_costs3, env_costs4], 
                                            ['Zero-Case', 'robust', 'Stagewise', 'Flexible'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Environmental Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Environmental Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Unmet Demand Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([unmet_demand_costs1, unmet_demand_costs2, unmet_demand_costs3, unmet_demand_costs4], 
                                            ['Zero-Case', 'robust', 'Stagewise', 'Flexible'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Unmet Demand Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Unmet Demand Costs for All Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Plot average parameters over the years
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_rainfall1, label='Average Rainfall', color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Rainfall Amount')
    plt.title('Average Rainfall over Years for Intervention 1')
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_population1, label='Average Population', color='orange')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title('Average Population over Years for Intervention 1')
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_total_demand1, label='Average Total Demand', color='green')
    plt.xlabel('Year')
    plt.ylabel('Total Demand')
    plt.title('Average Total Demand over Years for Intervention 1')
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Average Water Currently in Reservoir over Years for all Interventions
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_water_currently1, label='Nothing', color='skyblue')
    plt.plot(years, avg_water_currently2, label='robust', color='orange')
    plt.plot(years, avg_water_currently3, label='Stagewise', color='green')
    plt.plot(years, avg_water_currently4, label='Flexible', color='purple')
    plt.xlabel('Year')
    plt.ylabel('Water Currently in Reservoir')
    plt.title('Average Water Currently in Reservoir over Years for All Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Average Water Leakage over Years for all Interventions
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_leakage_nothing, label='Nothing', color='skyblue')
    plt.plot(years, avg_leakage_robust, label='robust', color='orange')
    plt.plot(years, avg_leakage_stagewise, label='Stagewise', color='green')
    plt.plot(years, avg_leakage_flexible, label='Flexible', color='purple')
    plt.xlabel('Year')
    plt.ylabel('Water Leakage')
    plt.title('Average Water Leakage over Years for All Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure

    # Cumulative Distribution of Total Discounted Costs for Selected Interventions
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([total_costs2, total_costs3, total_costs4], 
                                            ['robust', 'Stagewise', 'Flexible'])):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label)
    plt.xlabel('Total Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Total Discounted Costs for Selected Interventions')
    plt.legend()
    plt.grid(True)
    pdf.savefig()  # Save the current plot to the PDF
    plt.close()    # Close the figure
