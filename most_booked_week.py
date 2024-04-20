import pandas as pd
import matplotlib.pyplot as plt

# Paths to the files
calendar_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calender.csv'
listings_csv_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/listings.csv'

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

# Define the start and end of each week in the most booked month
# We assume that each month has at least 28 days and that weeks start on day 1, 8, 15, and 22
weeks = {
    'Week 1': ((most_booked_month_data['date'].dt.day >= 1) & (most_booked_month_data['date'].dt.day < 8)),
    'Week 2': ((most_booked_month_data['date'].dt.day >= 8) & (most_booked_month_data['date'].dt.day < 15)),
    'Week 3': ((most_booked_month_data['date'].dt.day >= 15) & (most_booked_month_data['date'].dt.day < 22)),
    'Week 4': (most_booked_month_data['date'].dt.day >= 22)
}

# Count the number of bookings for each week
weekly_bookings = {week: most_booked_month_data[condition].shape[0] for week, condition in weeks.items()}

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(weekly_bookings.keys(), weekly_bookings.values(), color='skyblue')

# Adding the total number on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, str(yval), ha='center', va='bottom')

# Adding title and labels
plt.title(f'Number of Bookings per Week in the Most Booked Month ({most_booked_month}) of 2024')
plt.xlabel('Week of the Month')
plt.ylabel('Number of Bookings')
plt.tight_layout()
plt.show()
