import numpy as np
import matplotlib.pyplot as plt

"""
Data collected
"""
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

# Average conditions from experimental data
avg_temperature = np.mean(experimental_data["temperature"])
avg_humidity = np.mean([h / 100 for h in experimental_data["humidity"]])  # Convert % to fraction


def calibrate_k():
    """Calibrate the mass transfer coefficient based on observed data."""
    P_sat = saturation_vapor_pressure(avg_temperature)  # Saturation vapor pressure (kPa)
    P_air = avg_humidity * P_sat  # Partial pressure of water vapor in air
    observed_rate_avg = np.mean(observed_vaporization_rates)  # g/h
    # Rearrange to solve for k
    return observed_rate_avg / (A * (P_sat - P_air) * 3600)


def saturation_vapor_pressure(T):
    """Calculates saturation vapor pressure in kPa given temperature in Celsius."""
    return 0.611 * np.exp((17.27 * T) / (T + 237.3))  # kPa


def vaporization_rate_g_per_h(T, RH, k):
    """Calculates the vaporization rate based on temperature and relative humidity in g/h."""
    P_sat = saturation_vapor_pressure(T)  # Saturation vapor pressure (kPa)
    P_air = RH * P_sat  # Partial pressure of water vapor in air
    rate = k * A * (P_sat - P_air)  # Rate proportional to pressure difference
    return rate * 3600  # Convert from g/s to g/h


def extrapolate_vaporization(temperature_range, humidity_range, k):
    """Extrapolates vaporization rate for temperature and humidity ranges."""
    rates_vs_temperature = [
        vaporization_rate_g_per_h(T, avg_humidity, k) for T in temperature_range
    ]
    rates_vs_humidity = [
        vaporization_rate_g_per_h(avg_temperature, RH, k) for RH in humidity_range
    ]
    return rates_vs_temperature, rates_vs_humidity


if __name__ == "__main__":
    # Calibrate constants
    A = 1.0  # Surface area of water (arbitrary units)
    k = calibrate_k()  # Calibrate mass transfer coefficient based on experimental data

    # Set ranges for extrapolation
    temperature_range = np.linspace(15, 35, 100)  # Temperature range (°C)
    humidity_range = np.linspace(0, 1, 100)  # Relative humidity range (0 to 1)

    # Extrapolate vaporization rates
    rates_vs_temperature, rates_vs_humidity = extrapolate_vaporization(temperature_range, humidity_range, k)

    # Adjust x-values for plotting (midpoints of intervals)
    adjusted_temperatures = experimental_data["temperature"][:-1]  # Exclude the last temperature
    adjusted_humidities = experimental_data["humidity"][:-1]  # Exclude the last humidity

    # Plot: Vaporization rate vs. Temperature
    plt.figure(figsize=(10, 5))
    plt.plot(temperature_range, rates_vs_temperature, label='Extrapolated Rate vs. Temperature (g/h)')
    plt.scatter(
        adjusted_temperatures,  # Adjusted to match observed_vaporization_rates length
        observed_vaporization_rates,
        color='red',
        label='Experimental Data (g/h)'
    )
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Vaporization Rate (g/h)')
    plt.title('Extrapolated Vaporization Rate vs. Temperature')
    plt.legend()
    plt.grid()
    plt.show()

    # Plot: Vaporization rate vs. Humidity
    plt.figure(figsize=(10, 5))
    plt.plot(humidity_range * 100, rates_vs_humidity, label='Extrapolated Rate vs. Humidity (g/h)', color='orange')
    plt.scatter(
        adjusted_humidities,  # Adjusted to match observed_vaporization_rates length
        observed_vaporization_rates,
        color='blue',
        label='Experimental Data (g/h)'
    )
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Vaporization Rate (g/h)')
    plt.title('Extrapolated Vaporization Rate vs. Humidity')
    plt.legend()
    plt.grid()
    plt.show()
