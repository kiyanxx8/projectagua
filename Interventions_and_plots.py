import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FormatStrFormatter
from MONTECARLO import monte_carlo_total_cost  # Import the monte_carlo function from the other file
from uncertainties.pop import pop_df
from uncertainties.rainfall import rainfall_cdf_df
from All_Parameters import water_min_constraint, water_min, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, Env_Cost

# Set up parameters
years = np.arange(1, 51)
discount_rate = 0.03

# Initial conditions
waterpumpcapacity_zero = 13870  # Initial water pump capacity in ML/year
leakage_zero = 730  # Initial water leakage in ML/year, this increases by 10 ML/year
catchment_area_zero = 6300000  # Initial catchment area in m^2

# Intervention Cost parameters
cost_fixing_leakage = 1000000  # Cost of fixing water leakage in $

# Water pump capacity after interventions
waterpump_increase_robust = 17500  # Waterpump capacity after robust intervention in ML/year
waterpump_increase_stagewise1 = 15000  # Waterpump capacity after stagewise intervention (stage 1) in ML/year
waterpump_increase_stagewise2 = 17500  # Waterpump capacity after stagewise intervention (stage 2) in ML/year

# Catchment area after interventions
catchment_area_new_robust = 13000000  # New catchment area after robust intervention in m^2
catchment_increase_stagewise1 = 9700000  # Catchmentarea after stagewise intervention (stage 1) in m^2
catchment_increase_stagewise2 = 11500000  # Catchmentarea after stagewise intervention (stage 2) in m^2
catchment_increase_flexible = 9250000  # Catchmentarea after flexible intervention in m^2


# Define intervention-specific DataFrames 
# Define intervention-specific DataFrames for water pump capacity

#Not fixing the leakage
Waterpump_capacity_nofixleakage = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_nofixleakage.loc[:, 1:] = waterpump_increase_robust #increase to 17500 after year 1

#Zero-Case
Waterpump_capacity_nothing = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))

#Robust
Waterpump_capacity_robust = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_robust.loc[:, 1:] = waterpump_increase_robust #increase to 17500 after year 1

#Stagewise
Waterpump_capacity_stagewise = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))
Waterpump_capacity_stagewise.loc[:, 25:] = waterpump_increase_stagewise1 #increase to 15000 after year 25
Waterpump_capacity_stagewise.loc[:, 33:] = waterpump_increase_stagewise2 #increase to 17500 after year 33

#Flexible
Waterpump_capacity_flexible = pd.DataFrame(waterpumpcapacity_zero, index=[1], columns=np.arange(1, 51))


# Define DataFrames for catchment area

#Not fixing the leakage
catchment_area_nofixleakage = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_nofixleakage.loc[:, 1:] = catchment_area_new_robust #increase to 13000000 after year 1

#Zero-Case
catchment_area_nothing = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))

#Robust
catchment_area_robust = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_robust.loc[:, 1:] = catchment_area_new_robust #increase to 13000000 after year 1

#Stagewise
catchment_area_stagewise = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_stagewise.loc[:, 1:] = catchment_increase_stagewise1 #increase to 9700000 after year 1
catchment_area_stagewise.loc[:, 20:] = catchment_increase_stagewise2 #increase to 11500000 after year 20

#Flexible
catchment_area_flexible = pd.DataFrame(catchment_area_zero, index=[1], columns=np.arange(1, 51))
catchment_area_flexible.loc[:, 1:] = catchment_increase_flexible #increase to 9250000 after year 1

# Define DataFrames for water leakage
i = 50  # Number of years

#Not fixing the leakage
Waterleakage_nofixleakage = pd.DataFrame([[730 + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))

#Zero-Case
Waterleakage_nothing = pd.DataFrame([[leakage_zero + (10 * x) for x in range(i)]], index=[1], columns=np.arange(1, i + 1))

#Robust
Waterleakage_robust = Waterleakage_nothing.copy()
for year in range(1, i + 1):
    Waterleakage_robust.loc[1, year] = 10 * (year - 1)  # Set to 0 at fix_year and increase by 10 each year

#Stagewise
Waterleakage_stagewise = Waterleakage_robust.copy() # Same as robust

#Flexible
Waterleakage_flexible = Waterleakage_robust.copy() # Same as robust


# Define DataFrames for intervention cost
#Not fixing the leakage
Cost_nofixleakage = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_nofixleakage[1] = (
                       cost_waterpump_capacity_increase * (waterpump_increase_robust - waterpumpcapacity_zero) + 
                       cost_catchment_area_increase * (catchment_area_new_robust - catchment_area_zero)) # Cost of robust intervention with leakage, water pump capacity and catchment area increase in year 1
Cost_nofixleakage += operational_cost_waterpump_increase * Waterpump_capacity_robust  # Operational cost of water pump capacity

#Zero-Case
Cost_nothing = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_nothing += operational_cost_waterpump_increase * Waterpump_capacity_nothing # Operational cost of water pump capacity

#Robust
Cost_robust = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_robust[1] = (cost_fixing_leakage + 
                       cost_waterpump_capacity_increase * (waterpump_increase_robust - waterpumpcapacity_zero) + 
                       cost_catchment_area_increase * (catchment_area_new_robust - catchment_area_zero)) # Cost of robust intervention with leakage, water pump capacity and catchment area increase in year 1
Cost_robust += operational_cost_waterpump_increase * Waterpump_capacity_robust  # Operational cost of water pump capacity

#Stagewise
Cost_stagewise = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_stagewise[1] = cost_fixing_leakage + cost_catchment_area_increase * (catchment_increase_stagewise1 - catchment_area_zero)  # Cost of stagewise intervention with leakage and catchment area increase in year 1
Cost_stagewise[20] = cost_catchment_area_increase * (catchment_increase_stagewise2 - catchment_increase_stagewise1) # Cost of stagewise intervention with catchment area increase in year 20
Cost_stagewise[25] = cost_waterpump_capacity_increase * (waterpump_increase_stagewise1 - waterpumpcapacity_zero) # Cost of stagewise intervention with water pump capacity increase in year 25
Cost_stagewise[33] = cost_waterpump_capacity_increase * (waterpump_increase_stagewise2 - waterpump_increase_stagewise1) # Cost of stagewise intervention with water pump capacity increase in year 33
Cost_stagewise += operational_cost_waterpump_increase * Waterpump_capacity_stagewise # Operational cost of water pump capacity

#Flexible
Cost_flexible = pd.DataFrame(0, index=[1], columns=np.arange(1, 51))
Cost_flexible[1] = cost_fixing_leakage + cost_catchment_area_increase * (catchment_increase_flexible - catchment_area_zero) # Cost of flexible intervention with leakage and catchment area increase in year 1



# Function to calculate discounted total costs
def calculate_cumulative_distribution(costs_df, discount_rate):
    discounted_costs = costs_df.apply(lambda x: sum(x[f'Year_{y}'] / (1 + discount_rate) ** y for y in range(1, len(x) + 1)), axis=1)
    sorted_costs = np.sort(discounted_costs)
    cumulative_probs = np.linspace(0, 1, len(sorted_costs))
    return sorted_costs, cumulative_probs



# Run Monte Carlo simulations for each intervention
# Monte Carlo Simulation if we dont fix the leakage
totalcost0, intervention_costs0, env_costs0, unmet_demand_costs0, _, _, _, avg_water_currently0, avg_leakage_nofixleakage, average_total_costs0, average_unmetdemandcost0, average_envcost0, average_interventioncost0  = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_nofixleakage, Waterleakage_nofixleakage, Cost_nofixleakage, catchment_area_nofixleakage, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
)

# Run Monte Carlo simulation for the zero-case scenario
total_costs1, nothing_costs1, env_costs1, unmet_demand_costs1, avg_rainfall1, avg_population1, avg_total_demand1, avg_water_currently1, avg_leakage_nothing, average_total_costs1, average_unmetdemandcost1, average_envcost1, average_interventioncost1 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_nothing, Waterleakage_nothing, Cost_nothing, catchment_area_nothing, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
) # Run Monte Carlo simulation for the robust scenario
total_costs2, intervention_costs2, env_costs2, unmet_demand_costs2, _, _, _, avg_water_currently2, avg_leakage_robust , average_total_costs2, average_unmetdemandcost2, average_envcost2, average_interventioncost2 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_robust, Waterleakage_robust, Cost_robust, catchment_area_robust, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
) # Run Monte Carlo simulation for the stagewise intervention
total_costs3, intervention_costs3, env_costs3, unmet_demand_costs3, _, _, _, avg_water_currently3, avg_leakage_stagewise, average_total_costs3, average_unmetdemandcost3, average_envcost3, average_interventioncost3 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_stagewise, Waterleakage_stagewise, Cost_stagewise, catchment_area_stagewise, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=False
) # Run Monte Carlo simulation for the flexible intervention
total_costs4, intervention_costs4, env_costs4, unmet_demand_costs4, _, _, _, avg_water_currently4, avg_leakage_flexible, average_total_costs4, average_unmetdemandcost4, average_envcost4, average_interventioncost4 = monte_carlo_total_cost(
    5000, 50, pop_df, rainfall_cdf_df, Waterpump_capacity_flexible, Waterleakage_flexible, Cost_flexible, catchment_area_flexible, cost_catchment_area_increase, cost_waterpump_capacity_increase, operational_cost_waterpump_increase, Wpriv, Wrest, Cpriv, Crest, water_min, water_min_constraint, Env_Cost, flexible=True
)





# Generate plots and save to PDF
# Hole den Namen der aktuellen Datei (ohne den Pfad) und ändere die Endung auf '.pdf'
pdf_filename = os.path.splitext(os.path.basename(__file__))[0] + '.pdf'

# Generiere das PDF mit dem erstellten Dateinamen
# Generate plots and save to PDF

with PdfPages(pdf_filename) as pdf:
    # Define colors for each intervention
    colors = ['blue', 'orange', 'green', 'purple']  # Customize these colors as needed

    def format_average(value):
        # Format to scientific notation with superscript for exponent
        formatted_value = f"{value:.2e}".replace("e+0", "e").replace("e", "×10^")  # Convert exponent to superscript-friendly format
        base, exponent = formatted_value.split("×10^")
        return f"{base}×10^{exponent} $"

    # Total Cost cumulative plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, avg_cost, label, color) in enumerate(zip(
            [total_costs1, total_costs2, total_costs3, total_costs4],
            [average_total_costs1, average_total_costs2, average_total_costs3, average_total_costs4],
            ['Zero-Case', 'Robust', 'Stagewise', 'Flexible'],
            colors)):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label, color=color)
        plt.axvline(avg_cost, color=color, linestyle='--', alpha=0.5, label=f"{format_average(round(avg_cost, 2))}")
    
    plt.xlabel('Total Discounted Cost ($)')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Total Discounted Costs for All Interventions')

    # Custom legend with smaller font size for average costs
    legend = plt.legend(fontsize='medium')  # Set general font size
    for text in legend.get_texts():
        if " × 10^" in text.get_text():
            text.set_fontsize('small')  # Set smaller font size for averages

    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig("CD_Totalcost.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()

    # Repeat this approach for each plot with cumulative distribution and average lines

    # Leakage impact plot
    plt.figure(figsize=(10, 6))
    for i, (cost_df, avg_cost, label, color) in enumerate(zip(
            [totalcost0, total_costs2], 
            [average_total_costs0, average_total_costs2], 
            ['unfixed leakage', 'robust'],
            colors[:2])):  
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label, color=color)
        plt.axvline(avg_cost, color=color, linestyle='--', alpha=0.5, label=f"{format_average(round(avg_cost, 2))}")
    
    plt.xlabel('Total Discounted Cost')
    plt.ylabel('Cumulative Probability')
    plt.title('Leakage Impact')
    
    legend = plt.legend(fontsize='medium')
    for text in legend.get_texts():
        if " × 10^" in text.get_text():
            text.set_fontsize('small')
    
    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig("CD_nofixleakage.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()

    # Intervention Cost cumulative plot with custom averages
    plt.figure(figsize=(10, 6))
    for i, (cost_df, label, color) in enumerate(zip(
            [nothing_costs1, intervention_costs2, intervention_costs3, intervention_costs4],
            ['Zero-Case', 'Robust', 'Stagewise', 'Flexible'],
            colors)):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs,  label=label, color=color)

    
    plt.xlabel('Intervention Discounted Cost ($)')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Intervention Costs for all Interventions')

    legend = plt.legend(fontsize='medium')
    for text in legend.get_texts():
        if " × 10^" in text.get_text():
            text.set_fontsize('small')

    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig("CD_Interventioncost.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()

    # Environmental Cost cumulative plot with custom averages
    plt.figure(figsize=(10, 6))
    for i, (cost_df, avg_cost, label, color) in enumerate(zip(
            [env_costs1, env_costs2, env_costs3, env_costs4],
            [average_envcost1, average_envcost2, average_envcost3, average_envcost4],
            ['Zero-Case', 'Robust', 'Stagewise', 'Flexible'],
            colors)):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label, color=color)
        plt.axvline(avg_cost, color=color, linestyle='--', alpha=0.5, label=f"{format_average(round(avg_cost, 2))}")
    
    plt.xlabel('Environmental Discounted Cost ($)')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Environmental Costs for All Interventions')
    
    legend = plt.legend(fontsize='medium')
    for text in legend.get_texts():
        if " × 10^" in text.get_text():
            text.set_fontsize('small')
    
    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig("CD_Envcost.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()

    # Unmet Demand Cost cumulative plot with custom averages
    plt.figure(figsize=(10, 6))
    for i, (cost_df, avg_cost, label, color) in enumerate(zip(
            [unmet_demand_costs1, unmet_demand_costs2, unmet_demand_costs3, unmet_demand_costs4],
            [average_unmetdemandcost1, average_unmetdemandcost2, average_unmetdemandcost3, average_unmetdemandcost4],
            ['Zero-Case', 'Robust', 'Stagewise', 'Flexible'],
            colors)):
        sorted_costs, cumulative_probs = calculate_cumulative_distribution(cost_df, discount_rate)
        plt.plot(sorted_costs, cumulative_probs, label=label, color=color)
        plt.axvline(avg_cost, color=color, linestyle='--', alpha=0.5, label=f"{format_average(round(avg_cost, 2))}")
    
    plt.xlabel('Unmet Demand Discounted Cost ($)')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of Unmet Demand Costs for All Interventions')
    
    legend = plt.legend(fontsize='medium')
    for text in legend.get_texts():
        if " × 10^" in text.get_text():
            text.set_fontsize('small')
    
    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig("CD_Unmetdemandcost.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_total_demand1, label='Average Total Demand', color='green')
    plt.xlabel('Year')
    plt.ylabel('Total Demand (ML)')
    plt.title('Average Total Demand over 50 Years')
    plt.legend()
    plt.grid(True)
    plt.savefig("avg_total_demand.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()

    # Average Water Currently in Reservoir over Years for all Interventions
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_water_currently1, label='Zero-Case', color='blue')
    plt.plot(years, avg_water_currently2, label='Robust', color='orange')
    plt.plot(years, avg_water_currently3, label='Stagewise', color='green')
    plt.plot(years, avg_water_currently4, label='Flexible', color='purple')
    plt.xlabel('Year')
    plt.ylabel('Water Currently in Reservoir (ML)')
    plt.title('Average Water Currently in Reservoir over Years for All Interventions')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig("avg_water_currently.png", format="png", dpi=300)
    pdf.savefig()
    plt.close()




print(average_total_costs0, average_total_costs1, average_total_costs2, average_total_costs3, average_total_costs4)  # Print average total costs for each intervention