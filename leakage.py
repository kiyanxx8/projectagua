import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Aktueller Wert der Current Leakage
current_leakage = 730  # ml/year

# Annahmen für die Prognose
years_forecast = np.arange(1, 51)  # Prognose für die nächsten 50 Jahre
leakage_range = np.linspace(current_leakage - 3 * current_leakage * 0.15, current_leakage + 3 * current_leakage * 0.15, 100)  # Bereich ±3 Standardabweichungen um den aktuellen Wert

# Unsicherheiten im ersten und letzten Jahr definieren
uncertainty_first_year = 0.05  # 5% im ersten Jahr
uncertainty_last_year = 0.15   # 15% im 50. Jahr

# Berechnung der Standardabweichung für jedes Prognosejahr durch lineare Interpolation
std_dev_per_year = uncertainty_first_year + (uncertainty_last_year - uncertainty_first_year) * (years_forecast - 1) / (years_forecast[-1] - 1)
std_dev_forecast = std_dev_per_year * current_leakage  # Anpassung der Standardabweichung basierend auf dem aktuellen Wert

# DataFrame zur Speicherung der Ergebnisse erstellen
leakage_df = pd.DataFrame(index=leakage_range, columns=years_forecast)

# Wahrscheinlichkeiten für jedes Prognosejahr mit einer Normalverteilung berechnen
for year in years_forecast:
    mean = current_leakage  # Aktueller Mittelwert für die Prognose verwenden
    std_dev = std_dev_forecast[year - 1]  # Jahr-spezifische Standardabweichung
    leakage_df[year] = norm.pdf(leakage_range, loc=mean, scale=std_dev)

print(leakage_df)

# Darstellung der Ergebnisse als Heatmap
plt.figure(figsize=(12, 8))
plt.imshow(leakage_df, aspect='auto', cmap='viridis', origin='lower',
           extent=[years_forecast.min(), years_forecast.max(), leakage_range.min(), leakage_range.max()])
plt.colorbar(label='Probability Density')
plt.title('Probability of Annual Current Leakage Over Next 50 Years with Variable Uncertainty')
plt.xlabel('Year')
plt.ylabel('Annual Current Leakage (ml/year)')
plt.show()
