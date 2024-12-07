import requests
import json


def run_simulation(
        endpoint_url="http://127.0.0.1:5000/simulate",
        room_volume=220,
        air_exchange_rate=70,
        outside_temp=6,
        outside_rh=57,
        inside_temp=21,
        initial_inside_rh=22,
        initial_vaporization_rate=250,
        total_duration=24,
        interval_minutes=15
):
    """
    Send a POST request to the simulation endpoint and print results.

    Parameters:
    - endpoint_url: URL of the simulation endpoint.
    - room_volume, air_exchange_rate, outside_temp, etc.: Simulation parameters.

    Returns:
    - None. Prints the simulation results or error message.
    """
    payload = {
        "room_volume": room_volume,
        "air_exchange_rate": air_exchange_rate,
        "outside_temp": outside_temp,
        "outside_rh": outside_rh,
        "inside_temp": inside_temp,
        "initial_inside_rh": initial_inside_rh,
        "initial_vaporization_rate": initial_vaporization_rate,
        "total_duration": total_duration,
        "interval_minutes": interval_minutes,
    }

    try:
        # Send POST request
        response = requests.post(endpoint_url, json=payload)

        # Check response status
        if response.status_code == 200:
            data = response.json()

            # Extract columns and units
            columns = data.get("columns", {})
            units = data.get("units", {})

            # Print units for reference
            print("Column Units:")
            for column, unit in units.items():
                print(f"{column}: {unit}")

            # Print data as formatted JSON
            print("\nSimulation Results (columns):")
            print(json.dumps(columns, indent=4))

        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {str(e)}")


if __name__ == "__main__":
    # Run the simulation
    run_simulation()
