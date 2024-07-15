import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Function to calculate velocity from acceleration data
def calculate_velocity(acceleration, time_intervals):
    velocity = [0]  # Initial velocity is zero
    for i in range(1, len(acceleration)):
        delta_v = acceleration[i] * time_intervals[i-1]
        velocity.append(velocity[-1] + delta_v)
    return velocity

# Load the CSV file
csv_file = 'data.csv'  
df = pd.read_csv(csv_file)

# Ensure the dataframe has the correct columns
required_columns = ['TIME_STAMPING', 'ALTITUDE', 'PRESSURE', 'ACC_R']
if not all(column in df.columns for column in required_columns):
    raise ValueError(f"CSV file must contain {', '.join(required_columns)} columns.")

# Convert TIME_STAMPING to datetime
try:
    # Attempt to convert assuming it's in a standard datetime format (e.g., 'HH:MM:SS')
    df['TIME_STAMPING'] = pd.to_datetime(df['TIME_STAMPING'], format='%H:%M:%S')
except ValueError as e:
    raise ValueError("TIME_STAMPING column is in an unrecognized format.") from e

# Calculate time intervals based on 1 Hz (1 second intervals)
df['time_intervals'] = 1.0  # Assuming 1 Hz, each interval is 1 second

# Calculate velocity from acceleration data
df['velocity'] = calculate_velocity(df['ACC_R'], df['time_intervals'])

# Set up the plot
plt.ion()  # Turn on interactive plotting

fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.subplots_adjust(hspace=0.4)
fig.suptitle('Telemetry Data Over Time', fontsize=16)

# Labels and titles for the subplots
plot_info = [
    ('PRESSURE', 'Pressure', 'blue', 'o'),
    ('ALTITUDE', 'Altitude', 'green', 's'),
    ('velocity', 'Velocity', 'red', '^')
]

for ax, (column, title, color, marker) in zip(axs, plot_info):
    ax.set_title(title, fontsize=14)
    ax.set_ylabel(title, fontsize=12)
    ax.grid(True)
    ax.legend([title])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=5))  # Set major ticks at 5-second intervals
    ax.xaxis.set_minor_locator(mdates.SecondLocator(interval=1))  # Set minor ticks at 1-second intervals

axs[-1].set_xlabel('Time (HH:MM:SS)', fontsize=12)

# Initialize empty lists for dynamic plotting
time_data = []
pressure_data = []
altitude_data = []
velocity_data = []

# Plotting loop for 30 seconds
for i in range(min(30, len(df))):
    row = df.iloc[i]
    
    time_data.append(row['TIME_STAMPING'])
    pressure_data.append(row['PRESSURE'])
    altitude_data.append(row['ALTITUDE'])
    velocity_data.append(row['velocity'])
    
    for ax, data, color, marker in zip(axs, [pressure_data, altitude_data, velocity_data], ['blue', 'green', 'red'], ['o', 's', '^']):
        ax.plot(time_data, data, color=color, marker=marker, linestyle='-', linewidth=1.5, markersize=5)
    
    plt.draw()  # Update the plots
    plt.pause(1)  # Pause for 1 second

plt.ioff()  # Turn off interactive plotting
plt.show()  # Show the final plot


