import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calender3.csv'

# Read the CSV file into a DataFrame
# Convert 'price' and 'adjusted_price' columns to strings to avoid mixed types warnings
df = pd.read_csv(csv_file_path, dtype={'price': str, 'adjusted_price': str}, low_memory=False)

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter rows for the year 2024
df_2024 = df[df['date'].dt.year == 2024]

# Select only the bookings (where 'available' is 'f')
bookings = df_2024[df_2024['available'] == 'f']

# Count the number of bookings for each month
monthly_bookings = bookings['date'].dt.month.value_counts().sort_index()

# Generate month names (ensuring that we have all months even if some months have no bookings)
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Create a list of month names that aligns with the months present in monthly_bookings
month_labels = [month_names[i-1] for i in monthly_bookings.index]

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(month_labels, monthly_bookings.values, color='skyblue')

# Adding the total number on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, yval, ha='center', va='bottom')

# Adding title and labels
plt.title('Number of Airbnb Bookings Per Month in 2024')
plt.xlabel('Month')
plt.ylabel('Number of Bookings')
plt.show()
