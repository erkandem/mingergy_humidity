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
def calibrate_k():
    """Calibrate the mass transfer coefficient based on observed data."""
    P_sat = saturation_vapor_pressure(avg_temperature)  # Saturation vapor pressure (kPa)
    P_air = avg_humidity * P_sat  # Partial pressure of water vapor in air
    observed_rate_avg = np.mean(observed_vaporization_rates)  # g/h
    # Rearrange to solve for k
    return observed_rate_avg / (A * (P_sat - P_air) * 3600)

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

    # Average conditions from experimental data
    avg_temperature = np.mean(experimental_data["temperature"])
    avg_humidity = np.mean([h / 100 for h in experimental_data["humidity"]])  # Convert % to fraction

    # Recalibrate constant
    A = 1.0  # Surface area of water (arbitrary units)
    k = calibrate_k()  # Calibrate k based on observed data

    # Define ranges for temperature and humidity
    temperature_range = np.linspace(15, 35, 200)  # Temperature range (°C) with finer intervals
    humidity_range = np.linspace(0, 1, 200)  # Relative humidity range (fraction) with finer intervals

    # Create a grid of temperature and humidity
    T, RH = np.meshgrid(temperature_range, humidity_range)

    # Calculate vaporization rates for each combination of temperature and humidity
    vaporization_rates = vaporization_rate_g_per_h(T, RH, k)

    # Convert humidity to percentage for better readability
    RH_percentage = RH * 100

    # Experimental data for overlay
    adjusted_temperatures = experimental_data["temperature"][:-1]  # Exclude the last temperature
    adjusted_humidities = experimental_data["humidity"][:-1]  # Exclude the last humidity
    observed_curve = np.array(observed_vaporization_rates)  # Observed vaporization rates

    # Plot the contour plot
    plt.figure(figsize=(12, 7))
    contour = plt.contourf(T, RH_percentage, vaporization_rates, levels=20, cmap='viridis')
    cbar = plt.colorbar(contour)
    cbar.set_label('Vaporization Rate (g/h)')

    # Overlay the experimental curve in red
    plt.plot(adjusted_temperatures, adjusted_humidities, color='red', linewidth=2, label='Experimental Curve')

    # Add labels, legend, and title
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Relative Humidity (%)')
    plt.title('Vaporization Rate vs. Temperature and Humidity')
    plt.legend()
    plt.grid(True)
    plt.show()
