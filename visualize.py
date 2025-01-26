import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Ereignisliste erstellen
events = [
    {"date": "2019-05-26", "description": "Europawahl 2019"},
    {"date": "2020-01-31", "description": "Brexit"},
    {"date": "2021-11-12", "description": "COP26 in Glasgow"},
    {"date": "2022-02-24", "description": "Beginn des Ukraine-Konflikts"},
    {"date": "2022-11-18", "description": "COP27 in Sharm El-Sheikh"},
    {"date": "2023-12-12", "description": "COP28 in Dubai"},
    {"date": "2024-05-26", "description": "Europawahl 2024"},
    {"date": "2024-12-12", "description": "COP29 in Baku"},
]

def load_data():
    # Beispiel-Daten laden (ersetzt durch tatsächliche Datenquelle)
    df = pd.read_csv("green_deal_data.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    return df

def plot_with_events(df, events, aggregation):
    # Daten aggregieren
    df = df.set_index("datetime").resample(aggregation).sum().reset_index()

    # Plot erstellen
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["datetime"], df["Article Count"], label="Artikelanzahl", color="blue")

    # Ereignisse einfügen
    for i, event in enumerate(events):
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        if df["datetime"].min() <= event_date <= df["datetime"].max():
            ax.axvline(event_date, color="red", linestyle="--", alpha=0.7)
            ax.text(event_date, df["Article Count"].max() * 0.9, str(i + 1), color="red", fontsize=10, ha="center")

    ax.set_title("Artikelanzahl mit Ereignissen")
    ax.set_xlabel("Datum")
    ax.set_ylabel("Artikelanzahl")
    ax.legend()
    ax.grid(True)

    return fig

def display_event_table(events):
    # Ereignistabelle anzeigen
    event_df = pd.DataFrame(events)
    st.write("### Ereignisse")
    st.dataframe(event_df, use_container_width=True)

# Streamlit App
st.title("Green Deal Dashboard")
st.sidebar.header("Einstellungen")

# Aggregationseinstellung
aggregation = st.sidebar.selectbox("Aggregationsintervall", ["D", "7D", "30D", "365D"], index=1)

# Ereignisse an-/abschalten
show_events = st.sidebar.checkbox("Ereignisse anzeigen", value=True)

# Daten laden
df = load_data()

# Zeitrahmenfilter
st.sidebar.header("Zeitraum filtern")
min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()
date_range = st.sidebar.date_input("Zeitraum", [min_date, max_date], min_value=min_date, max_value=max_date)

# Daten filtern
df_filtered = df[(df["datetime"] >= pd.to_datetime(date_range[0])) & (df["datetime"] <= pd.to_datetime(date_range[1]))]

# Plot anzeigen
if not df_filtered.empty:
    st.write("### Artikelanzahl im Zeitverlauf")
    fig = plot_with_events(df_filtered, events if show_events else [], aggregation)
    st.pyplot(fig)

    # Ereignistabelle anzeigen
    if show_events:
        display_event_table(events)
else:
    st.warning("Keine Daten im ausgewählten Zeitraum verfügbar.")
