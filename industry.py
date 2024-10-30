import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Annahmen und Import der populärsten Bevölkerung aus pop2.py
initial_pop = 54000  # Anfangspopulation
growth_per_year = 800  # Populationswachstum pro Jahr
years = np.arange(1, 51)  # Jahre von 1 bis 50
pop_range = np.linspace(50000, 100000, 100)  # Populationen von 50.000 bis 100.000

# Uncertainties in Industry Demand
alpha = 0.05  # Startwert: 5% der Bevölkerung als Nachfrage
uncertainty_industry_first_year = 0.05  # 5% Unsicherheit im ersten Jahr
uncertainty_industry_last_year = 0.15  # 15% Unsicherheit im 50. Jahr
dependency_growth_per_year = 0.0007  # 0,07% jährliches Wachstum der Abhängigkeit

# Standardabweichung der Industrie-Nachfrage pro Jahr berechnen
std_dev_industry_per_year = uncertainty_industry_first_year + (uncertainty_industry_last_year - uncertainty_industry_first_year) * (years - 1) / (years[-1] - 1)

# Wahrscheinlichste Bevölkerungswerte aus pop2.py importieren (Simulation als Beispiel hier)
# In der Realität sollten die wahrscheinlichsten Bevölkerungswerte aus pop2.py eingelesen werden
most_probable_pop = [54000 + growth_per_year * (year - 1) for year in years]  # Nur als Platzhalter für diese Demonstration

# Liste zur Speicherung der Industrie-Wasserbedarfsergebnisse
industry_demand_data = []

# Berechnung des Wasserverbrauchs der Industrie basierend auf der wahrscheinlichsten Population
for year in years:
    population = most_probable_pop[year - 1]
    dependency_factor = alpha + (year - 1) * dependency_growth_per_year
    mean_industry_demand = dependency_factor * population
    std_dev_industry_demand = mean_industry_demand * std_dev_industry_per_year[year - 1]
    
    # Hinzufügen der Ergebnisse zur Liste
    industry_demand_data.append({
        "Year": year,
        "Population": population,
        "Industry Demand Mean": mean_industry_demand,
        "Industry Demand Std Dev": std_dev_industry_demand
    })

# Umwandlung der Liste in ein DataFrame
industry_demand_df = pd.DataFrame(industry_demand_data)

# Ergebnisse anzeigen
print(industry_demand_df)

# Darstellung der Industriemandate als Plot
plt.figure(figsize=(10, 6))
plt.errorbar(industry_demand_df["Year"], industry_demand_df["Industry Demand Mean"], 
             yerr=industry_demand_df["Industry Demand Std Dev"], fmt='-o', capsize=5)
plt.title("Projected Industry Water Demand Over Next 50 Years")
plt.xlabel("Year")
plt.ylabel("Industry Water Demand (ml/year)")
plt.show()
