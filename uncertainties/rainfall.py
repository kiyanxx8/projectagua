import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import norm

# Erhalte den Pfad des aktuellen Skripts
base_dir = os.path.dirname(os.path.abspath(__file__))

# Navigiere zum übergeordneten Verzeichnis und dann in den Ordner 'csvs'
csv_path = os.path.join(base_dir, '..', 'csvs', 'rainfall.csv')  # '..' navigiert eine Ebene nach oben
csv_path = os.path.abspath(csv_path)  # Wandelt den relativen Pfad in einen absoluten Pfad um

# Lade die CSV-Datei
historical_data = pd.read_csv(csv_path, delimiter=';')

# Berechnung des durchschnittlichen jährlichen Niederschlags und der Standardabweichung der letzten 100 Jahre
mean_rainfall_100yrs = historical_data['Annual rainfall (mm) '].tail(100).mean()
std_dev_rainfall_100yrs = historical_data['Annual rainfall (mm) '].tail(100).std()

# Berechnung der durchschnittlichen jährlichen Veränderung der letzten 50 Jahre
# Filtern der Daten für den Zeitraum 1966 bis 2016
historical_data['Year'] = pd.to_numeric(historical_data['Year'], errors='coerce')  # Konvertieren Sie das Jahr in numerisches Format, falls es als Text gespeichert ist
filtered_data = historical_data[(historical_data['Year'] >= 1971) & (historical_data['Year'] <= 2016)]
# print(filtered_data)
# Berechnung der durchschnittlichen jährlichen Veränderung von 1966 bis 2016
mean_rainfall_change = filtered_data['Annual rainfall (mm) '].diff().mean()
#print("Durchschnittliche jährliche Veränderung von 1966 bis 2016:", mean_rainfall_change)
std_dev_rainfall_45yrs = filtered_data['Annual rainfall (mm) '].std()
#print("Standardabweichung der jährlichen Veränderung von 1966 bis 2016:", std_dev_rainfall_45yrs)
mean_rainfall_45yrs = filtered_data['Annual rainfall (mm) '].mean()
#print("Durchschnittlicher Niederschlag von 1966 bis 2016:", mean_rainfall_45yrs)
std_uns_rainfall_45yrs = std_dev_rainfall_45yrs / mean_rainfall_45yrs
#print(std_uns_rainfall_45yrs)

# Annahmen für die Prognose
years_forecast = np.arange(1, 51)  # Prognose für die nächsten 50 Jahre
rainfall_range = np.linspace(500, 3000, 1000)  # Niederschlagsmengen von 500 bis 2000 mm in 1000 Schritten

# Unsicherheiten im ersten und letzten Jahr definieren
uncertainty_first_year = std_uns_rainfall_45yrs  # Unsciherheit ist die der letzen Jahre
uncertainty_last_year = std_uns_rainfall_45yrs * 2  # doppelt so gross im letzten Jahr

# Berechnung der Standardabweichung für jedes Prognosejahr durch lineare Interpolation der Unsicherheit
std_dev_per_year = uncertainty_first_year + (uncertainty_last_year - uncertainty_first_year) * (years_forecast - 1) / (years_forecast[-1] - 1)
std_dev_forecast = std_dev_per_year * std_dev_rainfall_100yrs  # Unsicherheit basierend auf der historischen Standardabweichung der letzten 100 Jahre
# print("Standardabweichung pro Jahr (Vorhersage):", std_dev_forecast)

# DataFrame zur Speicherung der kumulativen Wahrscheinlichkeiten erstellen
rainfall_cdf_df = pd.DataFrame(index=rainfall_range, columns=years_forecast)

# Kumulative Wahrscheinlichkeiten (CDF) für jede Regenmenge und jedes Prognosejahr berechnen
for year in years_forecast:
    # Jährliche Veränderung wird auf den Durchschnittswert der letzten 100 Jahre addiert
    mean = mean_rainfall_45yrs + mean_rainfall_change * (year - 1)
    std_dev = std_dev_per_year[year - 1] * mean  # Jahr-spezifische Standardabweichung
    #print("Jahr:", year, "Mittelwert:", mean, "Standardabweichung:", std_dev)

    # Kumulative Wahrscheinlichkeit berechnen, dass der Niederschlag diesen Wert nicht überschreitet
    rainfall_cdf_df[year] = norm.cdf(rainfall_range, loc=mean, scale=std_dev)


#rainfall_cdf_df.to_csv('rainfall_cdf_df.csv')

# Darstellung der Ergebnisse als Heatmap
"""plt.figure(figsize=(12, 8))
plt.imshow(rainfall_cdf_df, aspect='auto', cmap='viridis', origin='lower',
           extent=[years_forecast.min(), years_forecast.max(), rainfall_range.min(), rainfall_range.max()])
plt.colorbar(label='Cumulative Probability')
plt.title('Cumulative Probability of Annual Rainfall Over Next 50 Years')
plt.xlabel('Year')
plt.ylabel('Annual Rainfall (mm)')
plt.show()"""
