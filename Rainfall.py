import pandas as pd

# Load the CSV file (replace 'your_file.csv' with your actual file path)
df = pd.read_csv('C:/Users/kizal/Everything/ETH local/1. Semester/infra Planning/projectagua/projectagua/rainfall.csv.csv', sep=';')

# Calculate the mean and standard deviation of the annual rainfall
mean_rainfall = df['Annual rainfall (mm)'].mean()
std_dev_rainfall = df['Annual rainfall (mm)'].std()

# Calculate the threshold for -2 sigma (two standard deviations below the mean)
threshold = mean_rainfall - 2 * std_dev_rainfall

# Filter rainfall values within -2 sigma
rainfall_within_2sigma = df[df['Annual rainfall (mm)'] <= threshold]

# Display the results
print("Mean Rainfall:", mean_rainfall)
print("Standard Deviation:", std_dev_rainfall)
print("Threshold for -2 sigma:", threshold)
print("Rainfall values within -2 sigma:")
print(rainfall_within_2sigma)