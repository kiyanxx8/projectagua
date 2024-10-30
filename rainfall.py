import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Beispielhafte historische Daten laden (ersetzen Sie dies durch echte Daten, wenn vorhanden)
# Hier wurden Daten wie im Beispiel verwendet
historical_data = pd.read_csv('C:/Users/linus/OneDrive - ETH Zurich/ETH/1. Semester/Infrastructure Planning/Assignment/Data/Regenfall 2024W.csv', delimiter=';')  # Beispieldatei, ersetzen Sie den Dateinamen

# Berechnung des historischen Mittels und der Standardabweichung des jährlichen Regenfalls
mean_rainfall = historical_data['Annual rainfall (mm) '].mean()
std_dev_rainfall = historical_data['Annual rainfall (mm) '].std()

# Annahmen für die Prognose
years_forecast = np.arange(1, 51)  # Prognose für die nächsten 50 Jahre
rainfall_range = np.linspace(mean_rainfall - 3 * std_dev_rainfall, mean_rainfall + 3 * std_dev_rainfall, 100) # Bereich von 3 Standardabweichungen um das Mittel (99.7% der Daten)

# Unsicherheiten im ersten und letzten Jahr definieren
uncertainty_first_year = 0.05  # 5% im ersten Jahr
uncertainty_last_year = 0.15   # 15% im 50. Jahr

# Berechnung der Standardabweichung für jedes Prognosejahr durch lineare Interpolation
std_dev_per_year = uncertainty_first_year + (uncertainty_last_year - uncertainty_first_year) * (years_forecast - 1) / (years_forecast[-1] - 1)
std_dev_forecast = std_dev_per_year * std_dev_rainfall  # Anpassung der Standardabweichung basierend auf historischen Daten

# DataFrame zur Speicherung der Ergebnisse erstellen
rainfall_df = pd.DataFrame(index=rainfall_range, columns=years_forecast)

# Wahrscheinlichkeiten für jedes Prognosejahr mit einer Normalverteilung berechnen
for year in years_forecast:
    mean = mean_rainfall  # Historisches Mittel für die Prognose verwenden
    std_dev = std_dev_forecast[year - 1]  # Jahr-spezifische Standardabweichung
    rainfall_df[year] = norm.pdf(rainfall_range, loc=mean, scale=std_dev)

print(rainfall_df)

# Darstellung der Ergebnisse als Heatmap
plt.figure(figsize=(12, 8))
plt.imshow(rainfall_df, aspect='auto', cmap='viridis', origin='lower',
           extent=[years_forecast.min(), years_forecast.max(), rainfall_range.min(), rainfall_range.max()])
plt.colorbar(label='Probability Density')
plt.title('Probability of Annual Rainfall Over Next 50 Years with Variable Uncertainty')
plt.xlabel('Year')
plt.ylabel('Annual Rainfall (mm)')
plt.show()
