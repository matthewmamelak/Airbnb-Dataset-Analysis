import pandas as pd
import matplotlib.pyplot as plt

# Paths to the files
calendar_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calender3.csv'
listings_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/listings3.csv'

# Read the CSV files into DataFrames
calendar_df = pd.read_csv(calendar_csv_path)
listings_df = pd.read_csv(listings_csv_path)

# Convert 'date' to datetime
calendar_df['date'] = pd.to_datetime(calendar_df['date'])

# Ensure 'price' columns are strings and then convert to numeric, handling non-numeric values
calendar_df['price'] = pd.to_numeric(calendar_df['price'].astype(str).str.replace('[$,]', '', regex=True), errors='coerce')
listings_df['price'] = pd.to_numeric(listings_df['price'].astype(str).str.replace('[$,]', '', regex=True), errors='coerce')

# Merge the DataFrames on the id column
merged_df = calendar_df.merge(listings_df, left_on='listing_id', right_on='id')

# Calculate the price difference
merged_df['price_difference'] = merged_df['price_x'] - merged_df['price_y']

# Group by month and calculate the average price difference
merged_df['month'] = merged_df['date'].dt.month
monthly_price_difference = merged_df.groupby('month')['price_difference'].mean()

# Plotting
plt.figure(figsize=(12, 8))
plt.plot(monthly_price_difference.index, monthly_price_difference.values, marker='o')

# Setting x-axis labels to be the month names
plt.xticks(monthly_price_difference.index, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Adding title and labels
plt.title('Average Airbnb Price Difference by Month')
plt.xlabel('Month')
plt.ylabel('Average Price Difference ($)')
plt.grid(True)
plt.tight_layout()
plt.show()
