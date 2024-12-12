import math

UNIVERSAL_GAS_CONSTANT_R = 8.314  # J/(mol·K)
MOLECULAR_WEIGHT_WATER = 0.018  # kg/mol
SPECIFIC_GAS_CONSTANT_WATER = UNIVERSAL_GAS_CONSTANT_R / MOLECULAR_WEIGHT_WATER  # J/(kg·K)
MAGNUS_A = 17.625
MAGNUS_B = 243.04

def calculate_saturated_vapor_pressure(temperature_celsius):
    return 610.94 * math.exp((MAGNUS_A * temperature_celsius) / (temperature_celsius + MAGNUS_B))

def calculate_absolute_humidity(temperature_celsius, relative_humidity):
    saturated_pressure = calculate_saturated_vapor_pressure(temperature_celsius)
    actual_vapor_pressure = saturated_pressure * (relative_humidity / 100)
    absolute_humidity = actual_vapor_pressure / (SPECIFIC_GAS_CONSTANT_WATER * (temperature_celsius + 273.15))
    return absolute_humidity * 1000  # Convert to [g/m³]

def calculate_vaporization_rate(initial_rate, current_relative_humidity):
    """
    Calculate the current vaporization rate based on the current relative humidity.
    Vaporization rate decreases linearly as RH approaches 100%.

    Parameters:
    - initial_rate: Initial vaporization rate in g/h.
    - current_relative_humidity: Current indoor relative humidity in %.

    Returns:
    - Adjusted vaporization rate in g/h.
    """
    if current_relative_humidity >= 100:
        return 0  # Vaporization stops at 100% RH
    current_rate = initial_rate * (1 - current_relative_humidity / 100)
    return current_rate


def transform_to_column_style(list_of_dicts):
    """Compatability to how a pd.Dataframe would be used
    Transforms a list of dictionaries into a column-style dictionary of lists.

    Parameters:
    - list_of_dicts: List of dictionaries where each dictionary represents a data record.

    Returns:
    - A dictionary of lists where each key corresponds to a column.
    """
    column_style = {}
    for record in list_of_dicts:
        for key, value in record.items():
            if key not in column_style:
                column_style[key] = []
            column_style[key].append(value)
    return column_style


def simulate_fixed_intervals(
    room_volume,
    air_exchange_rate,
    outside_temp,
    outside_rh,
    inside_temp,
    initial_inside_rh,
    initial_vaporization_rate,
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

        # Calculate current relative humidity
        current_relative_humidity = (current_inside_abs_humidity /
                                     calculate_absolute_humidity(inside_temp, 100)) * 100

        # Adjust vaporization rate based on current relative humidity
        vaporization_rate = calculate_vaporization_rate(initial_vaporization_rate, current_relative_humidity)
        # Calculate air exchange loss and net humidity change
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
            'current_relative_humidity': current_relative_humidity
        })

    # Returning results as a list of dictionaries
    return transform_to_column_style(results)

