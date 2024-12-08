import numpy as np
import matplotlib.pyplot as plt


# Saturation vapor pressure function (Clausius-Clapeyron approximation)
def saturation_vapor_pressure(T):
    """Calculates saturation vapor pressure in kPa given temperature in Celsius."""
    return 0.611 * np.exp((17.27 * T) / (T + 237.3))  # kPa


# Vaporization rate function
def vaporization_rate_g_per_h(T, RH, k):
    """Calculates the vaporization rate based on temperature and relative humidity in g/h."""
    P_sat = saturation_vapor_pressure(T)  # Saturation vapor pressure (kPa)
    P_air = RH * P_sat  # Partial pressure of water vapor in air
    rate = k * A * (P_sat - P_air)  # Rate proportional to pressure difference
    return rate * 3600  # Convert from g/s to g/h


# Calibration function
def calibrate_k(observed_rates, temperatures, humidities):
    """
    Calibrate the mass transfer coefficient based on observed data.

    Args:
    observed_rates (array-like): Observed vaporization rates in g/h
    temperatures (array-like): Corresponding temperatures in °C
    humidities (array-like): Corresponding relative humidities (0-1)

    Returns:
    float: Calibrated mass transfer coefficient
    """
    # Calculate average conditions
    avg_temperature = np.mean(temperatures)
    avg_humidity = np.mean(humidities)

    P_sat = saturation_vapor_pressure(avg_temperature)  # Saturation vapor pressure (kPa)
    P_air = avg_humidity * P_sat  # Partial pressure of water vapor in air
    observed_rate_avg = np.mean(observed_rates)  # g/h

    # Rearrange to solve for k
    return observed_rate_avg / (A * (P_sat - P_air) * 3600)


def plot_vaporization_rates(k, A=1.0):
    """
    Create a single plot to visualize vaporization rates across different humidity levels.

    Args:
    k (float): Mass transfer coefficient
    A (float, optional): Surface area. Defaults to 1.0.
    """
    # Define ranges for temperature and humidity
    temperature_range = np.linspace(15, 35, 200)  # Temperature range (°C)
    humidity_levels = np.arange(0, 1.1, 0.1)  # Humidity levels from 0 to 1 in 0.1 intervals

    # Create the plot with extra space on the right for annotations
    plt.figure(figsize=(14, 7))

    # Plot vaporization rates for each humidity level
    for humidity in humidity_levels:
        # Calculate vaporization rates at constant humidity
        vaporization_rates = vaporization_rate_g_per_h(
            temperature_range,
            np.full_like(temperature_range, humidity),
            k
        )

        # Plot with red color
        plt.plot(temperature_range, vaporization_rates, color='red', linewidth=1)

        # Annotate the last point with humidity level
        plt.text(temperature_range[-1] + 0.5, vaporization_rates[-1],
                 f'{humidity:.1f}',
                 color='red',
                 va='center')

    plt.xlabel('Temperature (°C)')
    plt.ylabel('Vaporization Rate (g/h)')
    plt.title('Vaporization Rates at Different Humidity Levels')
    plt.grid(True, linestyle='--', alpha=0.7)

    # Adjust plot to make room for annotations
    plt.xlim(15, 37)  # Extend x-axis to make room for annotations

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Experimental data
    experimental_data = {
        "time": [0, 10, 20, 30, 40, 50, 60],  # minutes
        "weight": [4834, 4798, 4768, 4740, 4710, 4677, 4648],  # g
        "humidity": [31, 31, 31, 32, 32, 32, 33],  # %
        "temperature": [23.2, 23.1, 23.0, 23.0, 23.0, 22.9, 22.9],  # °C
    }

    # Calculate observed vaporization rate in g/h
    time_intervals = np.diff(experimental_data["time"])  # Time intervals (minutes)
    weight_loss = np.diff(experimental_data["weight"])  # Weight loss (g)
    observed_vaporization_rates = (weight_loss / time_intervals) * 60  # Convert to g/h

    # Prepare data for calibration
    observed_temps = experimental_data["temperature"][:-1]
    observed_humidities = np.array(experimental_data["humidity"][:-1]) / 100  # Convert to fraction

    # Surface area (arbitrary units)
    A = 1.0

    # Calibrate mass transfer coefficient
    k = calibrate_k(observed_vaporization_rates, observed_temps, observed_humidities)

    # Plot the results
    plot_vaporization_rates(k, A)