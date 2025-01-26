import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Funktion zum Laden der Daten
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "green_deal_data.csv")

    if not os.path.exists(csv_path):
        st.error(f"Die Datei 'green_deal_data.csv' wurde nicht gefunden. (Pfad: {csv_path})")
        st.stop()

    df = pd.read_csv(csv_path)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    return df

# Streamlit-Anwendung
st.title("Green Deal Data Dashboard")
st.sidebar.header("Einstellungen")

# Daten laden
df = load_data()

# Filter für Zeitraum
st.sidebar.subheader("Zeitraum")
min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()
selected_range = st.sidebar.date_input("Zeitraum auswählen:", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter für Aggregation
st.sidebar.subheader("Datenaggregation")
aggregation_days = st.sidebar.number_input("Datenaggregation (Tage pro Datenpunkt):", min_value=1, max_value=365, value=1, step=1)

# Ereignisse einblenden
st.sidebar.subheader("Ereignisse")
show_events = st.sidebar.checkbox("Ereignisse einblenden", value=True)

# Trendlinie ein- und ausblenden
st.sidebar.subheader("Trendlinie")
show_trendline = st.sidebar.checkbox("Trendlinie anzeigen", value=True)

# Filter anwenden
filtered_df = df[(df["datetime"].dt.date >= selected_range[0]) & (df["datetime"].dt.date <= selected_range[1])]

# Daten aggregieren
filtered_df = (
    filtered_df.set_index("datetime")
    .resample(f"{aggregation_days}D")
    .sum()
    .reset_index()
)

# Visualisierung
st.subheader("Zeitreihenanalyse")
fig, ax = plt.subplots()

# Zeitreihen-Daten plotten
ax.plot(filtered_df["datetime"], filtered_df["Article Count"], label="Artikelanzahl", color="blue")

# Trendlinie hinzufügen
if show_trendline:
    z = np.polyfit(filtered_df.index, filtered_df["Article Count"], 1)
    p = np.poly1d(z)
    ax.plot(filtered_df["datetime"], p(filtered_df.index), label="Trendlinie", linestyle="--", color="orange")

# Ereignisse hinzufügen
if show_events:
    events = [
        {"date": "2020-12-11", "event": "Einführung des EU-Klimaziels 2030"},
        {"date": "2021-07-14", "event": "Fit-for-55-Paket vorgestellt"},
        {"date": "2022-11-06", "event": "COP27 Klimakonferenz"},
    ]
    for event in events:
        event_date = pd.to_datetime(event["date"])
        if selected_range[0] <= event_date.date() <= selected_range[1]:
            ax.axvline(event_date, color="red", linestyle="--", alpha=0.7)
            ax.text(event_date, ax.get_ylim()[1] * 0.9, event["event"], rotation=90, verticalalignment="bottom", fontsize=8)

# Diagramm anpassen
ax.set_title("Artikelanzahl im Zeitverlauf (Green Deal)")
ax.set_xlabel("Datum")
ax.set_ylabel("Artikelanzahl")
ax.legend()
st.pyplot(fig)
