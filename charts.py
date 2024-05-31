import pandas as pd
from plotly import graph_objects as go
from plotly import io as pio


def create_monthly_active_power_chart(file_path):
    names = [
        'Date/Time',
        'LV ActivePower',
        'Wind Speed',
        'Theoretical_Power_Curve',
        'Wind Direction (deg)',
    ]

    df = pd.read_csv(file_path, sep=",", skiprows=1, names=names)

    # Convert the 'datetime' column to datetime objects
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    # Sort the DataFrame by the 'datetime' column
    df = df.sort_values(by='Date/Time')

    # Extract month from the 'Date/Time'
    if 'Month' not in df:
        df['Month'] = df['Date/Time'].dt.month

    # Group by month and calculate the sum of 'LV ActivePower'
    monthly_data = df.groupby('Month')['LV ActivePower'].sum()

    # Create a bar chart
    fig = go.Figure([go.Bar(x=[f'Month {m}' for m in monthly_data.index], y=monthly_data.values)])

    # Update layout
    fig.update_layout(
        title='Monthly Sum of LV ActivePower',
        xaxis_title='Month',
        yaxis_title='LV ActivePower (kW)',
        plot_bgcolor='white',
        xaxis=dict(showline=True, showgrid=False, linecolor='black'),
        yaxis=dict(showline=True, showgrid=True, gridcolor='gray', linecolor='black')
    )

    config = {
        'scrollZoom': False,
        'showLink': False,
        'displayModeBar': False
    }

    html = pio.to_html(fig, validate=False, include_plotlyjs='cdn', config=config)

    # Save the HTML to a file
    with open('monthly_active_power.html', 'w') as file:
        file.write(html)

    return html

