import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Beispiel-Ereignisliste
EVENTS = [
    {"date": "2019-05-26", "event": "Europawahl 2019"},
    {"date": "2019-07-07", "event": "Parlamentswahl in Griechenland"},
    {"date": "2019-12-12", "event": "Parlamentswahl im Vereinigten Königreich"},
    {"date": "2021-12-15", "event": "UN-Klimakonferenz in Madrid (COP25) (02. Dezember - 15. Dezember 2019)"},
    {"date": "2020-01-31", "event": "Brexit – Austritt des Vereinigten Königreichs aus der EU"},
    {"date": "2020-03-11", "event": "WHO erklärt COVID-19 zur Pandemie"},
    {"date": "2021-07-29", "event": "Inkrafttreten des Europäischen Klimagesetzes"},
    {"date": "2021-10-31", "event": "UN-Klimakonferenz in Glasgow (COP26) (31. Oktober – 12. November 2021)"},
    {"date": "2022-02-24", "event": "Beginn des Ukraine-Konflikts"},
    {"date": "2022-04-10", "event": "Präsidentschaftswahl in Frankreich (1. Runde)"},
    {"date": "2022-04-24", "event": "Präsidentschaftswahl in Frankreich (2. Runde)"},
    {"date": "2022-11-06", "event": "UN-Klimakonferenz in Sharm El-Sheikh (COP27) (6. – 18. November 2022)"},
    {"date": "2022-11-08", "event": "Zwischenwahlen in den USA"},
    {"date": "2023-01-15", "event": "Parlamentswahl in Schweden"},
    {"date": "2023-03-13", "event": "Verabschiedung des EU-Klimaanpassungsgesetzes"},
    {"date": "2023-03-05", "event": "Parlamentswahl in Estland"},
    {"date": "2023-04-30", "event": "Parlamentswahl in Finnland"},
    {"date": "2023-11-30", "event": "UN-Klimakonferenz in Dubai (COP28) (30. November – 12. Dezember 2023)"},
    {"date": "2023-07-23", "event": "Parlamentswahl in Spanien"},
    {"date": "2023-10-08", "event": "Parlamentswahl in Luxemburg"},
    {"date": "2023-10-13", "event": "Parlamentswahl in Polen"},
    {"date": "2024-05-26", "event": "Europawahl 2024"},
    {"date": "2024-06-09", "event": "Parlamentswahl in Belgien"},
    {"date": "2024-06-09", "event": "Parlamentswahl in Litauen"},
    {"date": "2024-09-29", "event": "Parlamentswahl in Österreich"},
    {"date": "2024-10-27", "event": "Parlamentswahl in Portugal"},
    {"date": "2024-11-03", "event": "Parlamentswahl in Rumänien"},
    {"date": "2024-11-30", "event": "UN-Klimakonferenz in Baku (COP29) (30. November – 12. Dezember 2024)"}
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
