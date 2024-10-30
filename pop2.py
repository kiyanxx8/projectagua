import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define assumptions
initial_pop = 54000  # Starting population
growth_per_year = 800  # Population growth per year
years = np.arange(1, 51)  # Years from 1 to 50
pop_range = np.linspace(50000, 100000, 100)  # Population sizes from 50,000 to 100,000 in 100 steps

# Define the uncertainty/standard deviation in the first and last year
uncertainty_first_year = 0.05  # 5% in the first year
uncertainty_last_year = 0.30  # 30% in the 50th year

# Calculate the standard deviation for each year by linearly interpolating between the first and last year uncertainties
std_dev_per_year = uncertainty_first_year + (uncertainty_last_year - uncertainty_first_year) * (years - 1) / (years[-1] - 1)
std_dev_pop_growth = std_dev_per_year * growth_per_year  # Standard deviation in terms of population size growth

# Create an empty DataFrame to store the results
pop_df = pd.DataFrame(index=pop_range, columns=years)

# Loop through each year and calculate the probability of each population size using a normal distribution
for year in years:
    mean = initial_pop + growth_per_year * (year - 1)  # Mean population for this year (grows by 800 each year)
    std_dev = std_dev_pop_growth[year - 1]  # Standard deviation for the population size growth at this year
    
    # Calculate the probability for each population size at this year
    pop_df[year] = norm.pdf(pop_range, loc=mean, scale=std_dev)

# Display the first few rows of the DataFrame
print(pop_df.head())

# Plotting the results as a heatmap
plt.figure(figsize=(10, 6))
plt.imshow(pop_df, aspect='auto', cmap='viridis', origin='lower',
           extent=[years.min(), years.max(), pop_range.min(), pop_range.max()])
plt.colorbar(label='Probability Density')
plt.title('Probability of Population Size Over Time with Variable Uncertainty')
plt.xlabel('Year')
plt.ylabel('Population Size')
plt.show()
