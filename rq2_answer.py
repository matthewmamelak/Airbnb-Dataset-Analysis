import pandas as pd
import matplotlib.pyplot as plt

calendar_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calender2.csv'
listings_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/listings2.csv'

# Load the datasets, addressing the DtypeWarning by using low_memory=False
calendar_df = pd.read_csv(calendar_csv_path, low_memory=False)
listings_df = pd.read_csv(listings_csv_path, low_memory=False)

# Preprocess the price column: remove $ and commas, then convert to float
# Using pd.to_numeric with errors='coerce' to handle non-convertible values
calendar_df['calendar_price'] = pd.to_numeric(calendar_df['price'].astype(str).replace('[$,]', '', regex=True), errors='coerce')
listings_df['listing_price'] = pd.to_numeric(listings_df['price'].astype(str).replace('[$,]', '', regex=True), errors='coerce')

# Drop the original 'price' columns to avoid confusion
calendar_df.drop('price', axis=1, inplace=True)
listings_df.drop('price', axis=1, inplace=True)

# Merge the calendar and listings data on the 'listing_id'/'id' column
merged_df = pd.merge(calendar_df, listings_df, left_on='listing_id', right_on='id', how='left')

# Convert 'date' to datetime type and extract the month
merged_df['date'] = pd.to_datetime(merged_df['date'])
merged_df['month'] = merged_df['date'].dt.month

# Focus on December to calculate price variability by neighbourhood
december_prices = merged_df[merged_df['month'] == 12]

# Drop rows with NaN values in 'calendar_price' to ensure calculations can be performed
december_prices = december_prices.dropna(subset=['calendar_price'])

# Calculate the price variability (standard deviation) by neighbourhood
if 'neighbourhood' in december_prices.columns:
    price_variability_december = december_prices.groupby('neighbourhood')['calendar_price'].std().reset_index()
else:
    print("Column 'neighbourhood' not found. Please check column names in the listings DataFrame.")

# Assuming the previous step was successful and 'neighbourhood' column was found:
if 'neighbourhood' in december_prices.columns:
    price_variability_december = december_prices.groupby('neighbourhood')['calendar_price'].std().reset_index()

    # Sort by standard deviation to get the top 10 neighbourhoods with the highest variability
    top10_neighbourhoods = price_variability_december.nlargest(10, 'calendar_price')

    # Visualize the pricing variability for the top 10 neighbourhoods
    plt.figure(figsize=(12, 8))  # Wider figure for better layout of x-ticks
    plt.bar(top10_neighbourhoods['neighbourhood'], top10_neighbourhoods['calendar_price'], color='red')
    plt.title('Top 10 Neighbourhoods: Price Variability in December')
    plt.xlabel('Neighbourhood')
    plt.ylabel('Standard Deviation of Prices')
    plt.xticks(rotation=45)  # Rotate the x-ticks for better readability
    plt.tight_layout()  # Adjust layout to fit
    plt.show()
else:
    print("Column 'neighbourhood' not found. Please check column names in the listings DataFrame.")