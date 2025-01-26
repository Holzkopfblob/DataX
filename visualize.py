import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Ereignisse für die Visualisierung
events = {
    "2020-12-12": "Paris Agreement 5th Anniversary",
    "2021-11-01": "COP26 in Glasgow",
    "2022-11-06": "COP27 in Sharm El-Sheikh",
    "2023-10-01": "EU Emission Reduction Target Updated",
    "2024-06-06": "European Green Deal Summit",
}

# Funktion zum Laden der Daten
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/Holzkopfblob/DataX/main/green_deal_data.csv"
    df = pd.read_csv(url)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    return df

# Dashboard-Konfiguration
st.title("Green Deal Media Analysis Dashboard")
st.sidebar.header("Filter Optionen")

# Daten laden
df = load_data()

# Zeitauswahl
default_date_range = [df["datetime"].min(), df["datetime"].max()]
date_range = st.sidebar.date_input("Zeitraum", value=default_date_range, 
                                   min_value=default_date_range[0], max_value=default_date_range[1])

# Aggregationsoptionen
aggregation = st.sidebar.number_input("Aggregation (Tage pro Datenpunkt)", min_value=1, max_value=365, value=1)

# Ereignisse anzeigen oder ausblenden
show_events = st.sidebar.checkbox("Ereignisse anzeigen", value=True)

# Trendlinie ein-/ausblenden
show_trend = st.sidebar.checkbox("Trendlinie anzeigen", value=True)

# Daten filtern
try:
    df_filtered = df[(df["datetime"] >= pd.to_datetime(date_range[0])) &
                     (df["datetime"] <= pd.to_datetime(date_range[1]))]

    # Stelle sicher, dass "datetime" korrekt ist
    if not pd.api.types.is_datetime64_any_dtype(df_filtered["datetime"]):
        df_filtered["datetime"] = pd.to_datetime(df_filtered["datetime"], errors="coerce")

    # Entferne ungültige Datumswerte
    df_filtered = df_filtered.dropna(subset=["datetime"])

    # Aggregiere die Daten
    df_filtered["datetime"] = df_filtered["datetime"].dt.to_period(f"{aggregation}D").dt.start_time
    df_agg = df_filtered.groupby("datetime").agg({"Article Count": "sum", "All Articles": "sum"}).reset_index()
    df_agg["Ratio"] = df_agg["Article Count"] / df_agg["All Articles"]

    # Visualisierung
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(df_agg["datetime"], df_agg["Article Count"], label="Artikelanzahl", color="blue", alpha=0.7)
    ax.set_ylabel("Artikelanzahl", color="blue")
    ax.tick_params(axis="y", labelcolor="blue")

    # Zweite Achse für das Verhältnis
    ax2 = ax.twinx()
    ax2.plot(df_agg["datetime"], df_agg["Ratio"], label="Verhältnis Artikel/Alle Artikel", color="green")
    ax2.set_ylabel("Verhältnis", color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    # Ereignisse einfügen
    if show_events:
        for event_date, event_name in events.items():
            if pd.to_datetime(event_date) in df_agg["datetime"].values:
                ax.axvline(pd.to_datetime(event_date), color="red", linestyle="--", linewidth=1, alpha=0.7)
                ax.text(pd.to_datetime(event_date), ax.get_ylim()[1] * 0.9, str(event_date),
                        rotation=90, verticalalignment="top", color="red")

    # Trendlinie
    if show_trend:
        z = pd.np.polyfit(df_agg.index, df_agg["Article Count"], 1)
        p = pd.np.poly1d(z)
        ax.plot(df_agg["datetime"], p(df_agg.index), color="orange", linestyle="--", label="Trendlinie")

    ax.set_title("Green Deal Medienanalyse")
    ax.set_xlabel("Datum")
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    st.pyplot(fig)

    # Ereignisliste anzeigen
    if show_events:
        st.subheader("Ereignisliste")
        for i, (event_date, event_name) in enumerate(events.items(), start=1):
            st.write(f"{i}. {event_date}: {event_name}")

except Exception as e:
    st.error(f"Fehler bei der Datenverarbeitung: {e}")
