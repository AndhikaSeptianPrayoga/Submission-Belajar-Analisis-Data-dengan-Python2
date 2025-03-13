import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Basic Streamlit configuration
st.set_page_config(page_title="Bike Rental Analysis Dashboard", layout="wide")

# Function to load data with caching for efficiency
@st.cache_data
def load_data():
    day_df = pd.read_csv('../data/day.csv')
    hour_df = pd.read_csv('../data/hour.csv')
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# SIDEBAR
with st.sidebar:
    st.image("../logo.png", use_container_width=True, caption="Bike Rental Analysis", output_format="PNG")
    st.markdown(
        """
        <style>
        .sidebar .stImage img {
            border-radius: 50%;
            width: 150px;
            margin: 0 auto;
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("## Dashboard Information")
    st.write("This dashboard displays bike rental data analysis based on various factors.")
    
    # Get minimum and maximum dates from the dataset
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    
    # Sidebar for selecting date range
    st.markdown("### Date Range Filter")
    start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
    
    # Validate user input
    if start_date > end_date:
        st.error("Start date cannot be later than end date!")
        filtered_df = day_df  
    else:
        # Apply filter to data
        filtered_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & 
                             (day_df["dteday"] <= pd.to_datetime(end_date))]

# DASHBOARD
st.title("Bike Rental Analysis Dashboard")
st.markdown("### Data Summary")
st.write(f"Total records: {filtered_df.shape[0]} days")
st.write(f"Data period: {filtered_df['dteday'].min().date()} - {filtered_df['dteday'].max().date()}")

# Main Statistics Cards
st.markdown("### Key Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{filtered_df['cnt'].sum():,}")
col2.metric("Daily Average", f"{filtered_df['cnt'].mean():,.0f}")
col3.metric("Maximum Rentals", f"{filtered_df['cnt'].max():,}")

# VISUALIZATION
st.markdown("## Data Visualization")

## Weather Impact on Bike Rentals
st.markdown("### Weather Impact on Bike Rentals")
weather_labels = {1: "Clear", 2: "Cloudy", 3: "Light Rain", 4: "Heavy Rain"}
filtered_df["weather_label"] = filtered_df["weathersit"].map(weather_labels)

# Dropdown to select rental metric
metric_mapping = {
    "Total": "cnt",
    "Registered": "registered",
    "Casual": "casual"
}

selected_label = st.selectbox("Select rental metric:", list(metric_mapping.keys()), index=0)
selected_metric = metric_mapping[selected_label]

weather_agg = filtered_df.groupby("weather_label")[selected_metric].mean().reset_index()

# Use Plotly for interactive visualization
fig = px.bar(
    weather_agg,
    x="weather_label",
    y=selected_metric,
    color="weather_label",
    text=selected_metric,
    labels={"weather_label": "Weather Condition", selected_metric: f"Average {selected_label} Rentals"},
    title=f"Weather Impact on {selected_label} Bike Rentals",
    color_discrete_sequence=px.colors.sequential.Teal
)

# Add text above bars
fig.update_traces(texttemplate='%{text:.0f}', textposition="outside")

# Adjust Y-axis range for better proportion
y_max = weather_agg[selected_metric].max() * 1.2  
fig.update_layout(
    xaxis_title="Weather Condition",
    yaxis_title=f"Average {selected_label} Bike Rentals",
    yaxis=dict(range=[0, y_max]),  
    showlegend=False
)

st.plotly_chart(fig)

## Bike Rentals by Season
st.markdown("### Bike Rentals by Season")
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
filtered_df["season_label"] = filtered_df["season"].map(season_map)

selected_label = st.selectbox(
    "Select rental metric:",
    list(metric_mapping.keys()),
    index=0,
    key="season_metric_select"
)
selected_metric = metric_mapping[selected_label]

# Aggregate data by season
season_agg = filtered_df.groupby("season_label")[selected_metric].mean().reset_index()

# Interactive plot using Plotly
fig = px.bar(
    season_agg,
    x="season_label",
    y=selected_metric,
    color="season_label",
    text=selected_metric,
    labels={"season_label": "Season", selected_metric: f"Average {selected_label} Rentals"},
    title=f"Bike Rentals by Season ({selected_label})",
    color_discrete_sequence=px.colors.sequential.Teal
)

# Add text above bars
fig.update_traces(texttemplate='%{text:.0f}', textposition="outside")

# Adjust Y-axis range for better proportion
y_max = season_agg[selected_metric].max() * 1.2
fig.update_layout(
    xaxis_title="Season",
    yaxis_title=f"Average {selected_label} Bike Rentals",
    yaxis=dict(range=[0, y_max]),
    showlegend=False
)

# Display interactive plot
st.plotly_chart(fig)

## Bike Rentals on Weekdays vs Weekends
st.markdown("### Bike Rentals on Weekdays vs Weekends")
selected_label = st.selectbox(
    "Select rental metric:", 
    list(metric_mapping.keys()), 
    index=0, 
    key="workday_metric_select"  
)
selected_metric = metric_mapping[selected_label]

filtered_df["is_weekend"] = filtered_df["weekday"].apply(lambda x: "Weekend" if x in [5, 6] else "Weekday")
workday_agg = filtered_df.groupby("is_weekend")[selected_metric].mean().reset_index()

fig = px.bar(
    workday_agg,
    x="is_weekend",
    y=selected_metric,
    color="is_weekend",
    text=selected_metric,
    labels={"is_weekend": "Day Category", selected_metric: "Average Rentals"},
    title="Comparison of Bike Rentals on Weekdays vs Weekends",
    color_discrete_sequence=px.colors.sequential.Teal
)

fig.update_traces(texttemplate='%{text:.0f}', textposition="outside")
fig.update_layout(
    xaxis_title="Day Category",
    yaxis_title="Average Bike Rentals",
    showlegend=False,
    margin=dict(t=80, b=40, l=40, r=40),  
    title=dict(
        text="Comparison of Bike Rentals on Weekdays vs Weekends",
        font=dict(size=18), 
        x=0.5,  
        y=0.95  
    )
)

st.plotly_chart(fig)

## Hourly Bike Rental Trends
st.markdown("### Hourly Bike Rental Trends")
selected_label = st.selectbox(
    "Select rental metric:", 
    list(metric_mapping.keys()), 
    index=0, 
    key="hourly_metric"
)
selected_metric = metric_mapping[selected_label]

start_hour, end_hour = st.slider(
    "Select hour range:", 
    min_value=0, max_value=23, 
    value=(0, 23),  
    step=1
)

hourly_agg = hour_df.groupby("hr")[selected_metric].mean().reset_index()
filtered_data = hourly_agg[(hourly_agg["hr"] >= start_hour) & (hourly_agg["hr"] <= end_hour)]

fig = px.line(
    filtered_data, 
    x="hr", 
    y=selected_metric, 
    markers=True,
    labels={"hr": "Hour", selected_metric: "Number of Rentals"},
    title="Hourly Bike Rental Trends",
    color_discrete_sequence=["#1f77b4"]  
)

fig.update_traces(
    hoverinfo="x+y",
    mode="lines+markers",
    marker=dict(size=6, symbol="circle", line=dict(width=1.5, color="black"))
)

fig.update_layout(
    xaxis=dict(
        title="Hour", 
        tickmode="linear", 
        dtick=1,  
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title="Number of Rentals",
        showgrid=True,
        gridcolor="lightgray"
    ),
    margin=dict(t=50, b=50, l=50, r=50),
    title=dict(
        font=dict(size=18), 
        x=0.5,  
        y=0.95  
    ),
    hovermode="x unified",  
)

st.plotly_chart(fig)

## Most Influential Factors on Bike Rentals
st.markdown("### Most Influential Factors on Bike Rentals")
all_features = ["temp", "hum", "windspeed", "registered", "casual"]
selected_features = st.multiselect(
    "Select factors to analyze:", 
    all_features, 
    default=all_features
)

if selected_features:
    correlation_matrix = day_df[selected_features + ["cnt"]].corr()
    correlation_sorted = correlation_matrix["cnt"].drop("cnt").sort_values(ascending=True)  
    
    fig = px.bar(
        x=correlation_sorted.values, 
        y=correlation_sorted.index,
        orientation="h",
        labels={"x": "Correlation Coefficient", "y": "Factor"},
        title="Most Influential Factors on Bike Rentals",
        text=correlation_sorted.values,
        color=correlation_sorted.values, 
        color_continuous_scale=px.colors.sequential.Teal
    )

    fig.update_traces(
        texttemplate='%{text:.2f}', 
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Correlation Coefficient",
        yaxis_title="Factor",
        margin=dict(t=50, b=50, l=50, r=50),
        title=dict(
            font=dict(size=18), 
            x=0.5, 
            y=0.95  
        ),
        hovermode="y unified",
        coloraxis_showscale=False  
    )

    st.plotly_chart(fig)
else:
    st.warning("Select at least one factor to display.")

# Analysis Based on Time Range
st.markdown("### Bike Rental Trends Based on Time Range")
day_range = st.slider(
    "Select number of recent days for analysis:", 
    min_value=10, 
    max_value=len(day_df), 
    value=30, 
    step=5
)

selected_data = day_df.tail(day_range)

fig = px.line(
    selected_data, 
    x="dteday", 
    y="cnt", 
    markers=True,
    labels={"dteday": "Date", "cnt": "Number of Rentals"},
    title=f"Bike Rental Trends in the Last {day_range} Days",
    color_discrete_sequence=["green"]
)

fig.update_traces(
    line=dict(width=2), 
    marker=dict(size=6)
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Rentals",
    margin=dict(t=50, b=50, l=50, r=50),
    title=dict(font=dict(size=18), x=0.5, y=0.95),
    hovermode="x unified"
)

st.plotly_chart(fig)

# FOOTER
st.markdown("---")
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: #333;
    }
    </style>
    <div class="footer">
        &copy; 2025 Andhika Septian Prayoga. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
