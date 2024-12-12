import logging
import time
import plotly.graph_objects as go

import dash
from dash import dcc, html, Input, Output
from lib import simulate_fixed_intervals

app = dash.Dash(__name__)
app.title = "Humidity Simulator"
server = app.server
if __name__ != '__main__':
    # quick and not that dirty
    # https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.layout = html.Div(
    [
        html.H1("Humidity Simulation", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("Room Volume (m³):"),
                dcc.Input(id="room_volume", type="number", value=220, step=1),
                html.Label("Air Exchange Rate (%):"),
                dcc.Input(id="air_exchange_rate", type="number", value=70, step=10),
                html.Label("Outside Temperature (°C):"),
                dcc.Input(id="outside_temp", type="number", value=6, step=1),
                html.Label("Outside Relative Humidity (%):"),
                dcc.Input(id="outside_rh", type="number", value=80, step=1),
                html.Label("Inside Temperature (°C):"),
                dcc.Input(id="inside_temp", type="number", value=21, step=1),
                html.Label("Initial Inside RH (%):"),
                dcc.Input(id="initial_inside_rh", type="number", value=22, step=1),
                html.Label("Initial Vaporization Rate (g/h):"),
                dcc.Input(
                    id="initial_vaporization_rate", type="number", value=250, step=10
                ),
                html.Label("Total Duration (hours):"),
                dcc.Input(id="total_duration", type="number", value=24, step=1),
                html.Label("Interval (minutes):"),
                dcc.Input(id="interval_minutes", type="number", value=60, step=1),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "10px",
                "margin": "20px",
            },
        ),
        dcc.Graph(id="humidity_plot"),
    ]
)



@app.callback(
    Output("humidity_plot", "figure"),
    [
        Input("room_volume", "value"),
        Input("air_exchange_rate", "value"),
        Input("outside_temp", "value"),
        Input("outside_rh", "value"),
        Input("inside_temp", "value"),
        Input("initial_inside_rh", "value"),
        Input("initial_vaporization_rate", "value"),
        Input("total_duration", "value"),
        Input("interval_minutes", "value"),
    ],
)
def update_plot(
    room_volume,
    air_exchange_rate,
    outside_temp,
    outside_rh,
    inside_temp,
    initial_inside_rh,
    initial_vaporization_rate,
    total_duration,
    interval_minutes,
):
    start = time.time()
    results = simulate_fixed_intervals(
        room_volume=room_volume,
        air_exchange_rate=air_exchange_rate,
        outside_temp=outside_temp,
        outside_rh=outside_rh,
        inside_temp=inside_temp,
        initial_inside_rh=initial_inside_rh,
        initial_vaporization_rate=initial_vaporization_rate,
        total_duration=total_duration,
        interval_minutes=interval_minutes,
    )
    app.logger.info("Time elapsed: %s seconds", time.time() - start)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=results["time"],
            y=results["current_relative_humidity"],
            mode="lines",
            name="Relative Humidity (%)",
            line=dict(color="blue"),
        )
    )

    fig.update_layout(
        title="Relative Humidity Over Time",
        xaxis_title="Time (hours)",
        yaxis_title="Relative Humidity (%)",
        yaxis=dict(range=[0, 100]),
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
