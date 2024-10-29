import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define assumptions
years = np.arange(1, 51)  # Years from 1 to 50
mean_pop_growth = 1000  # Mean population growth rate per year
std_dev_pop_growth = 200  # Standard deviation for the population growth
pop_range = np.linspace(1000, 5000, 100)  # Population sizes from 1000 to 5000 in 100 steps

# Create an empty DataFrame to store the results
pop_df = pd.DataFrame(index=pop_range, columns=years)

# Loop through each year and calculate the probability of each population size using a normal distribution
for year in years:
    mean = mean_pop_growth * year  # Mean population for this year
    std_dev = std_dev_pop_growth * year  # Standard deviation for this year
    
    # Calculate the probability for each population size at this year
    pop_df[year] = norm.pdf(pop_range, loc=mean, scale=std_dev)

# Display the first few rows of the DataFrame
print(pop_df.head())


# Plotting the results as a heatmap
plt.figure(figsize=(10, 6))
plt.imshow(pop_df, aspect='auto', cmap='viridis', origin='lower',
           extent=[years.min(), years.max(), pop_range.min(), pop_range.max()])
plt.colorbar(label='Probability Density')
plt.title('Probability of Population Size Over Time')
plt.xlabel('Year')
plt.ylabel('Population Size')
plt.show()

