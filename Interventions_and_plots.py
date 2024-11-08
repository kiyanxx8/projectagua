import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from MONTECARLO import monte_carlo_total_cost  # Import the monte_carlo function from the other file
from uncertainties.pop import pop_df
from uncertainties.rainfall import rainfall_cdf_df

years = np.arange(1, 51)
discount_rate = 0.03

waterpumpcapacity_zero = 13870  # Initial water pump capacity in ML/year
waterpumpcapacity_new = 19000  # New water pump capacity in ML/year

leakage_zero = 730  # Initial water leakage in ML/year

catchment_area_zero = 6300000  # Initial catchment area in m^2
catchment_area_new_traditional = 12600000  # New catchment area after traditional intervention in m^2

cost_catchment_area_increase = 20  # Cost of increasing catchment area in $/m^2
cost_water_pump_capacity_increase = 1500000  # Rough Cost of new water pump capacity to 19000 ML/year
cost_fixing_leakage = 1000000  # Cost of fixing water leakage in $

fix_year_traditional = 1 # Year at which the traditional intervention is fixed

#INTERVENTIONS
# Define intervention-specific DataFrames for water pump capacity

# no intervention
Waterpump_capacity_nothing = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))

# traditional intervention
Waterpump_capacity_traditional = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_traditional.loc[:, fix_year_traditional:] = waterpumpcapacity_new

# stagewise intervention
Waterpump_capacity_stagewise = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))

# flexible intervention
Waterpump_capacity_flexible = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
increase_year2 = 20
new_capacity2 = 15000
Waterpump_capacity_flexible.loc[:, increase_year2:] = new_capacity2
increase_year3 = 40
new_capacity3 = 17000
Waterpump_capacity_flexible.loc[:, increase_year3:] = new_capacity3


# Define DataFrames for catchment area
# no intervention
catchment_area_nothing = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))

# traditional intervention
catchment_area_traditional = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_traditional.loc[:, fix_year_traditional:] = catchment_area_new_traditional

# stagewise intervention
catchment_area_stagewise = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))

# flexible intervention
catchment_area_flexible = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))



# Define DataFrames for water leakage
i = 50 # Number of years
# no intervention
Waterleakage_nothing = pd.DataFrame([[leakage_zero + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))

# traditional intervention
Waterleakage_traditional = pd.DataFrame([[leakage_zero + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))
for year in range(fix_year_traditional, i + 1):
    Waterleakage_traditional.loc[1, year] = 10 * (year - fix_year_traditional)  # Set to 0 at fix_year and increase by 10 each year after

# stagewise intervention
Waterleakage_stagewise = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))

# flexible intervention
Waterleakage_flexible = pd.DataFrame([[leakage_zero + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))


# Define DataFrames for intervention costs
# no intervention
Cost_nothing = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))

# traditional intervention
Cost_traditional = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_traditional[1] = cost_fixing_leakage + cost_water_pump_capacity_increase + cost_catchment_area_increase * (catchment_area_new_traditional - catchment_area_zero)

# stagewise intervention
Cost_stagewise = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_stagewise[2] = 5000000

# flexible intervention
Cost_flexible = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_flexible[20] = 5000000
Cost_flexible[40] = 4000000






# Function to calculate discounted total costs
def calculate_cumulative_distribution(costs_df, discount_rate):
    discounted_costs = costs_df.apply(lambda x: sum(x[f'Year_{y}'] / (1 + discount_rate) ** y for y in range(1, len(x) + 1)), axis=1)
    sorted_costs = np.sort(discounted_costs)
    cumulative_probs = np.linspace(0, 1, len(sorted_costs))

    return sorted_costs, cumulative_probs




# Run Monte Carlo simulations for each intervention
total_costs1, nothing_costs1, env_costs1, unmet_demand_costs1, avg_rainfall1, avg_population1, avg_total_demand1, avg_water_currently1 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_nothing, Waterleakage_nothing, Cost_nothing, catchment_area_nothing
)
total_costs2, intervention_costs2, env_costs2, unmet_demand_costs2, _, _, _, avg_water_currently2 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_traditional, Waterleakage_traditional, Cost_traditional, catchment_area_traditional
)
total_costs3, intervention_costs3, env_costs3, unmet_demand_costs3, _, _, _, avg_water_currently3 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_stagewise, Waterleakage_stagewise, Cost_stagewise, catchment_area_stagewise
)
total_costs4, intervention_costs4, env_costs4, unmet_demand_costs4, _, _, _, avg_water_currently4 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_flexible, Waterleakage_flexible, Cost_flexible, catchment_area_flexible
)

with PdfPages('all_interventions_costs.pdf') as pdf:
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label) in enumerate(zip([total_costs1, total_costs2, total_costs3, total_costs4], 
                                            ['Zero-Case', 'Traditional', 'stagewise', 'Flexible'])):
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
    for i, (cost_df, label) in enumerate(zip([nothing_costs1, intervention_costs2, intervention_costs3, intervention_costs4], 
                                            ['Zero-Case', 'Traditional', 'stagewise', 'Flexible'])):
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
                                            ['Zero-Case', 'Traditional', 'stagewise', 'Flexible'])):
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
                                            ['Zero-Case', 'Traditional', 'stagewise', 'Flexible'])):
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
    plt.plot(years, avg_water_currently1, label='nothing', color='skyblue')
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


