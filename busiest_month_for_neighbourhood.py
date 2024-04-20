import pandas as pd
import matplotlib.pyplot as plt

# Paths to the files
calendar_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calender1.csv'
listings_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/listings1.csv'

# Read the CSV files into DataFrames
calendar_df = pd.read_csv(calendar_csv_path, dtype={'price': str, 'adjusted_price': str}, low_memory=False)
listings_df = pd.read_csv(listings_csv_path)

# Convert the 'date' column in calendar_df to datetime
calendar_df['date'] = pd.to_datetime(calendar_df['date'])

# Filter for bookings in the year 2024 and where 'available' is 'f'
bookings_2024 = calendar_df[(calendar_df['date'].dt.year == 2024) & (calendar_df['available'] == 'f')]

# Find the most booked month in 2024
most_booked_month = bookings_2024['date'].dt.month.value_counts().idxmax()

# Filter the bookings for the most booked month
most_booked_month_data = bookings_2024[bookings_2024['date'].dt.month == most_booked_month]

# Merge the most_booked_month_data with listings on the 'id' column
merged_df = most_booked_month_data.merge(listings_df, left_on='listing_id', right_on='id')

# Group by neighbourhood_group and count the number of bookings
neighbourhood_bookings = merged_df['neighbourhood_group'].value_counts()

# Plotting the number of bookings in each neighbourhood for the most booked month
plt.figure(figsize=(12, 8))
bars = plt.bar(neighbourhood_bookings.index, neighbourhood_bookings.values, color='skyblue')

# Adding the total number on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, yval, ha='center', va='bottom')

# Adding title and labels
plt.title(f'Number of Bookings in Each Neighbourhood Group for the Most Booked Month ({most_booked_month}) in 2024')
plt.xlabel('Neighbourhood Group')
plt.ylabel('Number of Bookings')
plt.xticks(rotation=45) # Rotate the x labels if they are too long

# Display the plot
plt.tight_layout()  # Adjust layout to fit
plt.show()
