import os
import pandas as pd
import streamlit as st

def load_data():
    # Absoluten Pfad zur CSV-Datei basierend auf dem Skriptverzeichnis ermitteln
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
option = st.sidebar.selectbox(
    "Wähle die Visualisierungsart:",
    ["Artikel im Zeitverlauf", "Artikel im Verhältnis zu allen Artikeln"]
)

# Filtereinstellungen
start_date = st.sidebar.date_input("Startdatum", df["datetime"].min().date())
end_date = st.sidebar.date_input("Enddatum", df["datetime"].max().date())

# Daten filtern
filtered_df = df[(df["datetime"] >= pd.Timestamp(start_date)) & (df["datetime"] <= pd.Timestamp(end_date))]

# Visualisierung erstellen
if option == "Artikel im Zeitverlauf":
    st.subheader("Artikel im Zeitverlauf")
    st.line_chart(data=filtered_df.set_index("datetime")["Article Count"], use_container_width=True)

elif option == "Artikel im Verhältnis zu allen Artikeln":
    st.subheader("Artikel im Verhältnis zu allen Artikeln")
    filtered_df["Ratio"] = filtered_df["Article Count"] / filtered_df["All Articles"]
    st.line_chart(data=filtered_df.set_index("datetime")["Ratio"], use_container_width=True)
