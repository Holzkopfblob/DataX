import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Daten laden
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "green_deal_data.csv")

    if not os.path.exists(csv_path):
        st.error(f"Die Datei 'green_deal_data.csv' wurde nicht gefunden. Bitte stellen Sie sicher, dass sie im gleichen Verzeichnis wie dieses Skript liegt.")
        st.stop()

    df = pd.read_csv(csv_path)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    return df

data = load_data()

# Dashboard-Überschrift
st.title("Green Deal Data Dashboard")

# Sidebar-Optionen
st.sidebar.header("Einstellungen")

# Zeitaggregation wählen
aggregation = st.sidebar.selectbox(
    "Wähle Zeitaggregation",
    options=["Täglich", "Wöchentlich", "Monatlich", "Jährlich"],
    index=0
)

# Ereignisse anzeigen
event_toggle = st.sidebar.checkbox("Ereignisse anzeigen", value=False)

# Regressionslinien-Option
regression_toggle = st.sidebar.checkbox("Regressionslinie hinzufügen", value=False)

# Zeitaggregation anwenden
if aggregation == "Täglich":
    df_agg = data
elif aggregation == "Wöchentlich":
    df_agg = data.resample("W", on="datetime").sum().reset_index()
elif aggregation == "Monatlich":
    df_agg = data.resample("M", on="datetime").sum().reset_index()
elif aggregation == "Jährlich":
    df_agg = data.resample("Y", on="datetime").sum().reset_index()

# Ereignisse
events = [
    {"date": "2019-12-11", "event": "Verabschiedung EU Green Deal"},
    {"date": "2021-11-01", "event": "COP26 in Glasgow"},
    {"date": "2022-11-06", "event": "COP27 in Sharm El-Sheikh"}
]

# Plot erstellen
fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(data=df_agg, x="datetime", y="Article Count", ax=ax, label="Artikelanzahl")

if event_toggle:
    for event in events:
        event_date = pd.to_datetime(event["date"])
        ax.axvline(event_date, color="red", linestyle="--", alpha=0.7)
        ax.text(event_date, ax.get_ylim()[1] * 0.9, event["event"], color="red", rotation=90, fontsize=10)

if regression_toggle:
    sns.regplot(data=df_agg, x=df_agg["datetime"].map(pd.Timestamp.toordinal), y="Article Count", scatter=False, ax=ax, color="green", label="Regressionslinie")

ax.set_title("Artikelanzahl im Zeitverlauf")
ax.set_xlabel("Datum")
ax.set_ylabel("Anzahl der Artikel")
ax.legend()

st.pyplot(fig)

# Tabelle der aggregierten Daten anzeigen
st.write("### Aggregierte Daten", df_agg)
