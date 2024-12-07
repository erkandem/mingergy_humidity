import math
import pandas as pd
import matplotlib.pyplot as plt

# Fundamental Constants
UNIVERSAL_GAS_CONSTANT_R = 8.314  # J/(mol·K)
MOLECULAR_WEIGHT_WATER = 0.018  # kg/mol
SPECIFIC_GAS_CONSTANT_WATER = UNIVERSAL_GAS_CONSTANT_R / MOLECULAR_WEIGHT_WATER  # J/(kg·K)
MAGNUS_A = 17.625
MAGNUS_B = 243.04

# Magnus Equation to Calculate Saturated Vapor Pressure
def calculate_saturated_vapor_pressure(temperature_celsius):
    return 610.94 * math.exp((MAGNUS_A * temperature_celsius) / (temperature_celsius + MAGNUS_B))

# Calculate Absolute Humidity
def calculate_absolute_humidity(temperature_celsius, relative_humidity):
    saturated_pressure = calculate_saturated_vapor_pressure(temperature_celsius)
    actual_vapor_pressure = saturated_pressure * (relative_humidity / 100)
    absolute_humidity = actual_vapor_pressure / (SPECIFIC_GAS_CONSTANT_WATER * (temperature_celsius + 273.15))
    return absolute_humidity * 1000  # Convert to [g/m³]



# Simulate Humidity Dynamics in Fixed Intervals
def simulate_fixed_intervals(
    room_volume,
    air_exchange_rate,
    outside_temp,
    outside_rh,
    inside_temp,
    initial_inside_rh,
    vaporization_rate,
    total_duration,
    interval_minutes
):
    interval_hours = interval_minutes / 60.0
    outside_abs_humidity = calculate_absolute_humidity(outside_temp, outside_rh)
    current_inside_abs_humidity = calculate_absolute_humidity(inside_temp, initial_inside_rh)
    results = []
    iterations = int(total_duration / interval_hours)

    for step in range(iterations):
        time = step * interval_hours
        air_exchange_loss = (current_inside_abs_humidity - outside_abs_humidity) * air_exchange_rate * interval_hours
        net_humidity_change = (vaporization_rate * interval_hours) - air_exchange_loss
        current_inside_abs_humidity += net_humidity_change / room_volume

        results.append({
            'time': time,
            'current_absolute_humidity': current_inside_abs_humidity,
            'net_humidity_change': net_humidity_change,
            'air_exchange_loss': air_exchange_loss,
            'humidity_added': vaporization_rate * interval_hours,
            'humidity_balance': (vaporization_rate * interval_hours) - air_exchange_loss,
            'current_relative_humidity': (current_inside_abs_humidity /
                calculate_absolute_humidity(inside_temp, 100)) * 100
        })

    return pd.DataFrame(results)

# Visualize Results
def plot_humidity_dynamics(data):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel('Current Relative Humidity (%)', color='tab:blue')
    ax1.plot(data['time'], data['current_relative_humidity'], label='Relative Humidity (%)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Humidity Changes (g)', color='tab:orange')
    ax2.plot(data['time'], data['humidity_added'], label='Humidity Added (g)', color='tab:green', linestyle='--')
    ax2.plot(data['time'], data['air_exchange_loss'], label='Air Exchange Loss (g)', color='tab:red', linestyle='--')
    ax2.plot(data['time'], data['humidity_balance'], label='Humidity Balance (g)', color='tab:orange', linestyle='-')
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax2.legend(loc='upper right')

    plt.title('Time Series of Humidity Dynamics')
    fig.tight_layout()
    plt.show()

# Main Script
if __name__ == "__main__":
    # Define Parameters
    ROOM_VOLUME = 220  # [m³]
    AIR_EXCHANGE_RATE = 70  # [m³/h]
    OUTSIDE_TEMPERATURE = 6  # [°C]
    OUTSIDE_RELATIVE_HUMIDITY = 90  # [%]
    INSIDE_TEMPERATURE = 21  # [°C]
    INITIAL_INSIDE_RELATIVE_HUMIDITY = 22  # [%]
    VAPORIZATION_RATE = 250  # [g/h]
    TOTAL_DURATION = 24  # Total duration in hours
    INTERVAL_MINUTES = 15  # Interval in minutes

    # Run Simulation
    simulation_results = simulate_fixed_intervals(
        ROOM_VOLUME,
        AIR_EXCHANGE_RATE,
        OUTSIDE_TEMPERATURE,
        OUTSIDE_RELATIVE_HUMIDITY,
        INSIDE_TEMPERATURE,
        INITIAL_INSIDE_RELATIVE_HUMIDITY,
        VAPORIZATION_RATE,
        TOTAL_DURATION,
        INTERVAL_MINUTES
    )

    # Display Results and Plot
    print(simulation_results)
    plot_humidity_dynamics(simulation_results)
