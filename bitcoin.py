import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load and preprocess data
df = pd.read_csv('BTC-USD.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Feature engineering
df['Year'] = df.index.year
df['Month'] = df.index.month
df['Day'] = df.index.day
df['DayOfWeek'] = df.index.dayofweek

X = df[['Open', 'High', 'Low', 'Volume', 'Year', 'Month', 'Day', 'DayOfWeek']]
y = df['Close']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

# Evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

# Plotting - Office Presentation Style
plt.figure(figsize=(16, 8))
plt.plot(y_test.index, y_test, label='Actual Price', color='#1f77b4', linewidth=2)
plt.plot(y_test.index, y_pred, label='Predicted Price', color='#ff7f0e', linestyle='--', linewidth=2)

# Optional: fill area between lines to show prediction error
plt.fill_between(y_test.index, y_test, y_pred, color='gray', alpha=0.2, label='Error Region')

# Stylish grid and labels
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.title('BTC Closing Price: Actual vs Predicted', fontsize=20, fontweight='bold')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Close Price (USD)', fontsize=14)
plt.legend(fontsize=12)
plt.xticks(rotation=45)

# Add evaluation metrics on the plot
plt.text(0.01, 0.95, f'MAE: {mae:.2f}\nMSE: {mse:.2f}\nR²: {r2:.4f}', 
         transform=plt.gca().transAxes,
         fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

plt.tight_layout()
plt.show()
