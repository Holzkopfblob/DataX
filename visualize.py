import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

def load_data():
    """Load and preprocess the data."""
    # Load data
    df = pd.read_csv("green_deal_data.csv")

    # Convert datetime column to datetime format with UTC
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)

    return df

def filter_and_aggregate_data(df, date_range, aggregation):
    """Filter and aggregate data based on user input."""
    # Ensure the date_range is timezone-aware
    start_date = pd.to_datetime(date_range[0]).tz_localize("UTC")
    end_date = pd.to_datetime(date_range[1]).tz_localize("UTC")

    # Filter data by date range
    df_filtered = df[(df["datetime"] >= start_date) & (df["datetime"] <= end_date)]

    # Aggregate data
    df_filtered["datetime"] = df_filtered["datetime"].dt.to_period(f"{aggregation}D").dt.start_time
    df_aggregated = df_filtered.groupby("datetime").sum().reset_index()

    return df_aggregated

def plot_data(df, events, show_trend, show_events):
    """Plot the data with optional trend line and events."""
    # Create base chart
    base = alt.Chart(df).mark_line().encode(
        x="datetime:T",
        y="Article Count:Q",
        tooltip=["datetime:T", "Article Count:Q"]
    ).properties(title="Artikelanzahl im Zeitverlauf")

    # Add trend line if selected
    if show_trend:
        trend = base.transform_regression("datetime", "Article Count").mark_line(color="red")
        base = base + trend

    # Add events as vertical lines if selected
    if show_events:
        events_chart = alt.Chart(pd.DataFrame(events)).mark_rule(color="green").encode(
            x="date:T",
            tooltip=["date:T", "description:N"]
        )
        base = base + events_chart

    return base

def main():
    st.title("Green Deal Media Coverage Dashboard")

    # Load data
    df = load_data()

    # Sidebar options
    st.sidebar.header("Filtereinstellungen")
    date_range = st.sidebar.date_input("Zeitraum auswählen", [df["datetime"].min().date(), df["datetime"].max().date()])
    aggregation = st.sidebar.number_input("Aggregation (in Tagen)", min_value=1, max_value=365, value=7, step=1)
    show_trend = st.sidebar.checkbox("Trendlinie anzeigen", value=True)
    show_events = st.sidebar.checkbox("Ereignisse anzeigen", value=True)

    # Events (example data)
    events = [
        {"date": "2019-12-11", "description": "European Green Deal vorgestellt"},
        {"date": "2020-03-11", "description": "COVID-19 Pandemie ausgerufen"},
        {"date": "2021-11-01", "description": "COP26 Klimakonferenz"},
        {"date": "2023-06-01", "description": "Neues Klimagesetz verabschiedet"},
    ]

    # Filter and aggregate data
    df_aggregated = filter_and_aggregate_data(df, date_range, aggregation)

    # Display data
    st.write("### Gefilterte und aggregierte Daten", df_aggregated)

    # Plot data
    chart = plot_data(df_aggregated, events, show_trend, show_events)
    st.altair_chart(chart, use_container_width=True)

    # Show event legend if events are displayed
    if show_events:
        st.write("### Ereignisse")
        events_df = pd.DataFrame(events)
        st.write(events_df)

if __name__ == "__main__":
    main()
