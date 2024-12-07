from flask import Flask, request, jsonify, render_template
import pandas as pd
from humidity import simulate_fixed_intervals

app = Flask(__name__)
@app.route('/')
def index():
    """
    Serve the index page with the input form.
    """
    return render_template('index.html')
@app.route('/simulate', methods=['POST'])
def simulate():
    """
    API endpoint to run the humidity simulation and return results with unit annotations.
    """
    try:
        # Parse input parameters
        data = request.get_json()
        room_volume = data.get('room_volume', 220)
        air_exchange_rate = data.get('air_exchange_rate', 70)
        outside_temp = data.get('outside_temp', 6)
        outside_rh = data.get('outside_rh', 57)
        inside_temp = data.get('inside_temp', 21)
        initial_inside_rh = data.get('initial_inside_rh', 22)
        initial_vaporization_rate = data.get('initial_vaporization_rate', 250)
        total_duration = data.get('total_duration', 24)
        interval_minutes = data.get('interval_minutes', 15)

        # Validate inputs
        if not all(isinstance(value, (int, float)) for value in [room_volume, air_exchange_rate, outside_temp, inside_temp, initial_vaporization_rate, total_duration, interval_minutes]):
            raise ValueError("Numeric fields must be integers or floats.")
        if not all(0 <= value <= 100 for value in [outside_rh, initial_inside_rh]):
            raise ValueError("Relative humidity values must be between 0 and 100.")

        # Run the simulation
        simulation_results = simulate_fixed_intervals(
            room_volume,
            air_exchange_rate,
            outside_temp,
            outside_rh,
            inside_temp,
            initial_inside_rh,
            initial_vaporization_rate,
            total_duration,
            interval_minutes
        )

        # Convert DataFrame to a dictionary of columns
        results = {column: simulation_results[column].tolist() for column in simulation_results.columns}

        # Unit annotations
        units = {
            "time": "hours",
            "current_absolute_humidity": "g/m³",
            "net_humidity_change": "g",
            "air_exchange_loss": "g",
            "humidity_added": "g",
            "humidity_balance": "g",
            "current_relative_humidity": "%"
        }

        # Return results with units
        return jsonify({'columns': results, 'units': units}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
