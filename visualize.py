import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Beispiel-Ereignisliste
EVENTS = [
    {"date": "2019-05-26", "event": "EU-Parlamentswahl"},
    {"date": "2021-11-01", "event": "COP26 in Glasgow"},
    {"date": "2022-02-24", "event": "Beginn des Ukraine-Kriegs"},
    {"date": "2023-09-01", "event": "G20-Klimagipfel"},
]

@st.cache_data
def load_data(csv_file: str) -> pd.DataFrame:
    """Lädt CSV, konvertiert datetime und entfernt ungültige Datensätze."""
    df = pd.read_csv(csv_file)
    # Datumsumwandlung
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    # Ungültige Datumswerte entfernen
    df.dropna(subset=["datetime"], inplace=True)
    return df

def aggregate_data(df: pd.DataFrame, days: int) -> pd.DataFrame:
    """Aggregiert Daten auf x-Tage-Ebene."""
    df = df.copy()
    df["datetime"] = df["datetime"].dt.floor(f"{days}D")
    return df.groupby("datetime").agg({"Article Count": "sum"}).reset_index()

def main():
    st.title("Green Deal Dashboard")
    st.write("Analyse der medialen Berichterstattung zum EU Green Deal.")
    
    # Daten laden
    try:
        df = load_data("green_deal_data.csv")
        st.success("Daten erfolgreich geladen!")
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        st.stop()

    # Sidebar-Filter
    st.sidebar.header("Filter")
    min_date = df["datetime"].min().date()
    max_date = df["datetime"].max().date()

    date_range = st.sidebar.date_input(
        "Zeitraum wählen",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    agg_days = st.sidebar.number_input(
        "Tage pro Datenpunkt (Aggregation)",
        min_value=1, max_value=365, value=1
    )
    
    show_events = st.sidebar.checkbox("Ereignisse anzeigen", value=True)
    show_trend = st.sidebar.checkbox("Trendlinie anzeigen", value=False)

    # Daten filtern & aggregieren
    try:
        df_filtered = df[
            (df["datetime"] >= pd.to_datetime(date_range[0], utc=True)) &
            (df["datetime"] <= pd.to_datetime(date_range[1], utc=True))
        ]
        df_agg = aggregate_data(df_filtered, agg_days)
    except Exception as e:
        st.error(f"Fehler bei der Datenverarbeitung: {e}")
        st.stop()

    # Hauptdiagramm
    st.subheader("Artikelanzahl im Zeitverlauf")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_agg["datetime"], df_agg["Article Count"], label="Artikelanzahl", color="blue")

    # Optionale Trendlinie
    if show_trend:
        # Für robustere Zeitachsen: matplotlib-Datumszahlen verwenden
        df_agg["mdates_num"] = mdates.date2num(df_agg["datetime"])
        sns.regplot(
            x="mdates_num",
            y="Article Count",
            data=df_agg,
            scatter=False,
            ax=ax,
            color="red",
            label="Trendlinie"
        )

    # Ereignismarkierungen
    if show_events:
        for i, event in enumerate(EVENTS, start=1):
            event_date = pd.to_datetime(event["date"], utc=True)
            if event_date >= df_filtered["datetime"].min() and event_date <= df_filtered["datetime"].max():
                ax.axvline(event_date, color="green", linestyle="--", linewidth=0.8)
                ax.text(event_date, df_agg["Article Count"].max() * 0.8, str(i),
                        rotation=90, verticalalignment="bottom", fontsize=8, color="green")
    
    ax.set_title("Artikelanzahl im Zeitverlauf")
    ax.set_xlabel("Datum")
    ax.set_ylabel("Artikelanzahl")
    ax.legend()
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    st.pyplot(fig)

    # Ereignisliste
    if show_events:
        st.subheader("Ereignisliste")
        st.table(pd.DataFrame(EVENTS).reset_index().rename(columns={"index": "Nr.", "date": "Datum", "event": "Ereignis"}))

    # Daten anzeigen
    st.subheader("Gefilterte & aggregierte Daten")
    st.dataframe(df_agg)

if __name__ == "__main__":
    main()
