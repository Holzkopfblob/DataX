import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Daten laden
@st.cache_data
def load_data():
    df = pd.read_csv("green_deal_data.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    return df

def aggregate_data(df, days):
    df["datetime"] = df["datetime"].dt.floor(f"{days}D")
    return df.groupby("datetime").agg({"Article Count": "sum", "All Articles": "sum"}).reset_index()

# Streamlit App
st.title("Green Deal Data Explorer")

# Daten einlesen
try:
    df = load_data()
    st.success("Daten erfolgreich geladen!")
except Exception as e:
    st.error(f"Fehler beim Laden der Daten: {e}")
    st.stop()

# Filtereinstellungen
st.sidebar.header("Filtereinstellungen")
date_range = st.sidebar.date_input(
    "Zeitraum wählen",
    value=(df["datetime"].min().date(), df["datetime"].max().date()),
    min_value=df["datetime"].min().date(),
    max_value=df["datetime"].max().date(),
)

aggregation = st.sidebar.number_input(
    "Tage pro Datenpunkt (Aggregation)", min_value=1, max_value=365, value=1
)

# Ereignisse ein-/ausblenden
event_display = st.sidebar.checkbox("Ereignisse anzeigen", value=True)
trendline_display = st.sidebar.checkbox("Trendlinie anzeigen", value=True)

# Ereignisliste
EVENTS = [
    {"date": "2019-05-26", "event": "Europawahl 2019"},
    {"date": "2020-12-12", "event": "Verabschiedung des EU-Klimagesetzes"},
    {"date": "2021-11-01", "event": "COP26 in Glasgow"},
    {"date": "2022-10-30", "event": "Parlamentswahlen in Brasilien"},
    {"date": "2023-09-01", "event": "G20-Klimagipfel"},
    # Weitere Ereignisse können hier hinzugefügt werden
]

# Daten filtern und aggregieren
try:
    df_filtered = df[(df["datetime"] >= pd.to_datetime(date_range[0], utc=True)) & (df["datetime"] <= pd.to_datetime(date_range[1], utc=True))]
    df_aggregated = aggregate_data(df_filtered.copy(), aggregation)
except Exception as e:
    st.error(f"Fehler bei der Datenverarbeitung: {e}")
    st.stop()

# Diagramm "Artikelanzahl im Zeitverlauf"
st.subheader("Artikelanzahl im Zeitverlauf")
plt.figure(figsize=(16, 8))  # Vergrößertes Diagramm
plt.plot(df_aggregated["datetime"], df_aggregated["Article Count"], label="Artikelanzahl", color="blue")
if trendline_display:
    sns.regplot(
        x=pd.to_numeric(df_aggregated["datetime"]),
        y=df_aggregated["Article Count"],
        scatter=False,
        label="Trendlinie",
        color="red",
    )
if event_display:
    for i, event in enumerate(EVENTS, start=1):
        event_date = pd.to_datetime(event["date"], utc=True)
        if pd.to_datetime(date_range[0], utc=True) <= event_date <= pd.to_datetime(date_range[1], utc=True):
            plt.axvline(event_date, color="green", linestyle="--", linewidth=0.8)
            plt.text(event_date, df_aggregated["Article Count"].max() * 0.8, str(i), rotation=90, verticalalignment="bottom", fontsize=8, color="green")
plt.title("Artikelanzahl im Zeitverlauf")
plt.xlabel("Datum")
plt.ylabel("Artikelanzahl")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Ereignisliste anzeigen
if event_display:
    st.subheader("Ereignisliste")
    st.write(pd.DataFrame(EVENTS).reset_index().rename(columns={"index": "Nr.", "date": "Datum", "event": "Ereignis"}))

# Gefilterte und aggregierte Daten anzeigen
st.subheader("Gefilterte und aggregierte Daten")
st.write(df_aggregated)

