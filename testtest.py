# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define assumptions
initial_pop = 10000  # Starting population
growth_per_year = 800  # Population growth per year
years = np.arange(1, 51)  # Years from 1 to 50

# Define population ranges for both density and cumulative plots
pop_range = np.linspace(8000, 80000, 1000)  # Population sizes for original density plot
pop_growth_range = np.linspace(0, growth_per_year * 50, 1000)  # Population growth for cumulative plot

# Define the uncertainty/standard deviation in the first and last year
uncertainty_first_year = 0.05  # 5% in the first year
uncertainty_last_year = 0.30  # 30% in the 50th year

# Calculate the standard deviation for each year by linearly interpolating between the first and last year uncertainties
std_dev_per_year = uncertainty_first_year + (uncertainty_last_year - uncertainty_first_year) * (years - 1) / (years[-1] - 1)
std_dev_pop_growth = std_dev_per_year * growth_per_year  # Standard deviation in terms of population size growth

# Original probability density calculation
pop_df = pd.DataFrame(index=pop_range, columns=years)
for year in years:
    mean = initial_pop + growth_per_year * (year - 1)  # Mean population for this year
    std_dev = std_dev_pop_growth[year - 1]  # Standard deviation for the population size growth at this year
    pop_df[year] = norm.pdf(pop_range, loc=mean, scale=std_dev)
    
    # Print mean and range of one standard deviation (mean ± std_dev) for each year
    print(f"Year {year}: Mean = {mean}, Range = [{mean - std_dev}, {mean + std_dev}]")

# Cumulative Standard Deviation for each year to accumulate uncertainty
cumulative_std_dev_per_year = np.zeros(len(years))
for i, year in enumerate(years):
    # Sum the variances up to this year and take the square root to get the cumulative standard deviation
    cumulative_std_dev_per_year[i] = np.sqrt(np.sum(std_dev_pop_growth[:i+1] ** 2))

# Cumulative probability calculation for cumulative population growth with accumulated uncertainty
cum_pop_growth_df = pd.DataFrame(index=years, columns=pop_growth_range)
for i, year in enumerate(years):
    mean_growth = growth_per_year * (year - 1)  # Mean cumulative population growth by this year
    cumulative_std_dev = cumulative_std_dev_per_year[i]  # Cumulative standard deviation up to this year
    
    # Print mean and cumulative standard deviation for each year in cumulative distribution
    print(f"Cumulative Year {year}: Mean Population Growth = {mean_growth}, Cumulative Std Dev = {cumulative_std_dev}")
    
    # Calculate the cumulative probability for each cumulative population growth level with accumulated uncertainty
    cum_pop_growth_df.loc[year] = norm.cdf(pop_growth_range, loc=mean_growth, scale=cumulative_std_dev)

# Convert cumulative DataFrame to numeric for plotting compatibility
cum_pop_growth_df = cum_pop_growth_df.apply(pd.to_numeric)

# Plotting both the probability density and cumulative distribution with correct accumulated uncertainty
fig, axes = plt.subplots(2, 1, figsize=(14, 16))

# Probability Density Plot (Top)
axes[0].imshow(pop_df, aspect='auto', cmap='viridis', origin='lower',
               extent=[years.min(), years.max(), pop_range.min(), pop_range.max()])
axes[0].set_title('Probability Density of Population Size Over Time with Variable Uncertainty')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Population Size')
axes[0].colorbar = fig.colorbar(axes[0].images[0], ax=axes[0], label='Probability Density')

# Cumulative Distribution Plot (Bottom) with Year on x-axis and Cumulative Population Growth on y-axis
axes[1].imshow(cum_pop_growth_df.values.T, aspect='auto', cmap='coolwarm', origin='lower',
               extent=[years.min(), years.max(), pop_growth_range.min(), pop_growth_range.max()])
axes[1].set_title('Cumulative Distribution of Population Growth Over Time with Accumulated Uncertainty')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Cumulative Population Growth')
axes[1].colorbar = fig.colorbar(axes[1].images[0], ax=axes[1], label='Cumulative Probability')

plt.tight_layout()
plt.show()
