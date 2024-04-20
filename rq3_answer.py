import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# Load the datasets
calendar_csv_path = 'calender3.csv'
listings_csv_path = 'listings3.csv'

calendar_df = pd.read_csv(calendar_csv_path)
listings_df = pd.read_csv(listings_csv_path)

# Rename the 'price' column in calendar_df to avoid conflict
calendar_df.rename(columns={'price': 'calendar_price'}, inplace=True)

# Preprocess the calendar data
calendar_df['date'] = pd.to_datetime(calendar_df['date'])
calendar_df['calendar_price'] = pd.to_numeric(calendar_df['calendar_price'].str.replace('[$,]', '', regex=True), errors='coerce')

# Merge the calendar and listings data on listing ID
merged_df = pd.merge(calendar_df, listings_df, left_on='listing_id', right_on='id', how='left')

# Drop rows with NaN values in 'calendar_price'
merged_df.dropna(subset=['calendar_price'], inplace=True)

# Feature Engineering
merged_df['is_peak_season'] = merged_df['date'].dt.month == 12
merged_df['lead_time'] = 365 - merged_df['availability_365']

# Define the target variable (price) and features
y = merged_df['calendar_price']
X = merged_df[['is_peak_season', 'lead_time', 'date']]

# Sort the values by date to make our time series plots correct
X.sort_values('date', inplace=True)
y = y.loc[X.index]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Initialize models
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree Regressor': DecisionTreeRegressor(random_state=42),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42)
}

results = {}
# Train and evaluate each model
for name, model in models.items():
    model.fit(X_train.drop('date', axis=1), y_train)
    y_pred = model.predict(X_test.drop('date', axis=1))
    mse = mean_squared_error(y_test, y_pred)
    results[name] = mse
    print(f'Mean Squared Error for {name}: {mse}')

# Plot MSE for each model
plt.figure(figsize=(10, 5))
plt.bar(results.keys(), results.values())
plt.xlabel('Model')
plt.ylabel('Mean Squared Error')
plt.title('Comparison of Regression Models')
plt.show()
