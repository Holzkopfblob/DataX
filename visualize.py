import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel der App
st.title("Green Deal Data Explorer")

# Daten laden
try:
    # CSV-Datei laden
    DATA_URL = "green_deal_data.csv"
    df = pd.read_csv(DATA_URL)

    # Sicherstellen, dass die datetime-Spalte korrekt formatiert ist
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    st.success("Daten erfolgreich geladen!")
except Exception as e:
    st.error("Fehler beim Laden der Daten. Bitte überprüfen Sie die Datei.")
    st.stop()

# Benutzeroptionen
st.sidebar.header("Filtereinstellungen")
keywords = st.sidebar.multiselect(
    "Wähle Keywords:",
    options=df["keyword"].unique(),
    default=df["keyword"].unique()
)
date_range = st.sidebar.date_input(
    "Wähle den Zeitraum:",
    [df["datetime"].min(), df["datetime"].max()]
)

# Daten filtern
filtered_df = df[(df["keyword"].isin(keywords)) & (df["datetime"].between(*date_range))]

# Visualisierungen
st.subheader("Artikelvolumen im Zeitverlauf")
if filtered_df.empty:
    st.warning("Keine Daten verfügbar für die aktuellen Filtereinstellungen.")
else:
    # Plot erstellen
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Artikeldaten plotten
    ax1.plot(filtered_df["datetime"], filtered_df["Article Count"], label="Artikelanzahl", color="blue")
    ax1.set_xlabel("Datum")
    ax1.set_ylabel("Artikelanzahl", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True)

    # Verhältnis zu allen Artikeln als zweite Y-Achse
    ax2 = ax1.twinx()
    ax2.plot(
        filtered_df["datetime"],
        filtered_df["Article Count"] / filtered_df["All Articles"],
        label="Verhältnis Artikel / Alle Artikel",
        color="green",
    )
    ax2.set_ylabel("Verhältnis", color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    fig.tight_layout()
    st.pyplot(fig)

# Datenübersicht anzeigen
st.subheader("Gefilterte Daten")
st.write(filtered_df)

# Download-Option für gefilterte Daten
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Gefilterte Daten herunterladen",
    data=csv,
    file_name="filtered_green_deal_data.csv",
    mime="text/csv",
)
