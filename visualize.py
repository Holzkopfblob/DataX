import os
import pandas as pd
import streamlit as st

def load_data():
    # Absoluter Pfad zur CSV-Datei basierend auf dem Skriptverzeichnis
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "green_deal_data.csv")

    # Überprüfen, ob die Datei existiert
    if not os.path.exists(csv_path):
        st.error(f"Die Datei 'green_deal_data.csv' wurde nicht gefunden. Bitte stellen Sie sicher, dass sie im gleichen Verzeichnis wie dieses Skript liegt. (Gesuchter Pfad: {csv_path})")
        st.stop()

    # CSV-Datei laden
    df = pd.read_csv(csv_path)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")  # Datetime-Konvertierung
    return df

# Streamlit-Anwendung
st.title("Green Deal Data Explorer")
st.sidebar.header("Filtereinstellungen")

# Daten laden
df = load_data()
st.success("Daten erfolgreich geladen!")

# Visualisierungsoptionen
st.header("Datenanalyse")

# Filter anwenden
date_range = st.sidebar.date_input(
    "Wähle den Zeitraum:",
    [df["datetime"].min(), df["datetime"].max()]
)
filtered_df = df[df["datetime"].between(*pd.to_datetime(date_range))]

# Artikelvolumen im Zeitverlauf
st.subheader("Artikelvolumen im Zeitverlauf")
st.line_chart(filtered_df.set_index("datetime")["Article Count"])

# Verhältnis von Artikeln zu allen Artikeln
st.subheader("Artikelverhältnis (Artikel zu allen Artikeln)")
filtered_df["Ratio"] = filtered_df["Article Count"] / filtered_df["All Articles"]
st.line_chart(filtered_df.set_index("datetime")["Ratio"])

st.write("Datenquelle: GDELT API")
