import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

# Load the CSV files
d_load_df = pd.read_csv('D_load_fcst_archive.csv')
j_load_df = pd.read_csv('J_load_fcst_archive.csv')

# Function to clean and convert date and time to datetime
def convert_datetime(df):
    df['time'] = df['time'].astype(str).str.zfill(4)  # Ensure time is in HHMM format
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + df['time'].str[:2], format='%Y%m%d%H', errors='coerce')
    return df

# Apply the function to all dataframes
d_load_df = convert_datetime(d_load_df)
j_load_df = convert_datetime(j_load_df)

# Convert the 'revision' column to datetime format
d_load_df['revision'] = pd.to_datetime(d_load_df['revision'], format='%d/%m/%Y %H:%M', errors='coerce')
j_load_df['revision'] = pd.to_datetime(j_load_df['revision'], format='%d/%m/%Y %H:%M', errors='coerce')

# Ensure we only use numeric columns for resampling
d_load_numeric = d_load_df[['datetime', 'load_fcst']].copy()  # Only numeric columns
j_load_numeric = j_load_df[['datetime', 'load_fcst']].copy()  # Only numeric columns

# Resample the data to hourly intervals, filling missing values if necessary
d_load_df_resampled = d_load_numeric.set_index('datetime').resample('H').mean().fillna(method='ffill').reset_index()
j_load_df_resampled = j_load_numeric.set_index('datetime').resample('H').mean().fillna(method='ffill').reset_index()

# Use scattergl for large datasets
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("D Load Forecast", "J Load Forecast"))

# D Load with scattergl for large datasets
fig.add_trace(go.Scattergl(x=d_load_df_resampled['datetime'], y=d_load_df_resampled['load_fcst'], mode='lines', name='D Load Forecast', line=dict(color='green')), row=1, col=1)

# J Load with scattergl for large datasets
fig.add_trace(go.Scattergl(x=j_load_df_resampled['datetime'], y=j_load_df_resampled['load_fcst'], mode='lines', name='J Load Forecast', line=dict(color='red')), row=2, col=1)

# Update layout to add a range slider and selectors for zooming
fig.update_layout(
    height=700, 
    width=1000, 
    title_text="Load Forecasts and Revised Forecasts Over Time", 
    showlegend=True,
    xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1d", step="day", stepmode="backward"),
        dict(count=7, label="1w", step="day", stepmode="backward"),
        dict(step="all")
    ])),
    rangeslider=dict(visible=True),
    type="date"
    ),
    xaxis2=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1d", step="day", stepmode="backward"),
        dict(count=7, label="1w", step="day", stepmode="backward"),
        dict(step="all")
    ])),
    rangeslider=dict(visible=True),
    type="date"
    )
)

# Show plot in browser
pyo.plot(fig)