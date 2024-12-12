import matplotlib.pyplot as plt

from lib import simulate_fixed_intervals


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
    OUTSIDE_RELATIVE_HUMIDITY = 57  # [%]
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
