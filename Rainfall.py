import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/kizal/Everything/ETH_local/Semester1/infra_Planning/projectagua/projectagua/rainfall.csv', sep=';')

# Calculate the mean and standard deviation 
mean_rainfall = df['Annual rainfall (mm) '].mean()
std_dev_rainfall = df['Annual rainfall (mm) '].std()

# Calculate the threshold for -2 sigma 
threshold = mean_rainfall - 2 * std_dev_rainfall


# Display the results
print("Mean Rainfall:", mean_rainfall)
print("Standard Deviation:", std_dev_rainfall)
print("Threshold for -2 sigma:", threshold)




plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["Annual rainfall (mm) "], label="Annual Rainfall", marker='o')
plt.axhline(mean_rainfall, color='orange', linestyle='--', label="Mean")
plt.axhline(mean_rainfall +  2 * std_dev_rainfall, color='green', linestyle=':', label="Mean + 1σ")
plt.axhline(mean_rainfall - 2 * std_dev_rainfall, color='green', linestyle=':', label="Mean - 1σ")

# Adding labels and title
plt.xlabel("Year")
plt.ylabel("Annual Rainfall (mm)")
plt.title("Annual Rainfall with Mean and Standard Deviation")
plt.legend()
plt.grid(True)
plt.show()