import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Datei laden und sicherstellen, dass "datetime" korrekt formatiert ist
@st.cache_data
def load_data():
    df = pd.read_csv("green_deal_data.csv", sep="\t")  # Tab-Separierung beachten
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")  # Datetime-Konvertierung
    df["datetime"] = df["datetime"].dt.tz_localize(None)  # Zeitzone entfernen
    return df

# Daten laden
df = load_data()

# Sidebar-Einstellungen
st.sidebar.header("Filtereinstellungen")
date_range = st.sidebar.date_input(
    "Wähle den Zeitraum:",
    value=(df["datetime"].min(), df["datetime"].max()),
    min_value=df["datetime"].min(),
    max_value=df["datetime"].max(),
)

# Filter anwenden
filtered_df = df[df["datetime"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))]

# Zusätzliche Analyse-Optionen
analysis_option = st.sidebar.selectbox(
    "Wähle die Datenanalyse:",
    [
        "Artikelanzahl im Zeitverlauf",
        "Artikelanzahl im Verhältnis zu allen Artikeln",
    ],
)

# Visualisierungen
st.title("Green Deal Data Explorer")
st.success("Daten erfolgreich geladen!")

if filtered_df.empty:
    st.warning("Keine Daten im ausgewählten Zeitraum.")
else:
    if analysis_option == "Artikelanzahl im Zeitverlauf":
        # Artikelanzahl im Zeitverlauf
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(filtered_df["datetime"], filtered_df["Article Count"], label="Artikelanzahl", color="blue")
        ax.set_title("Artikelanzahl im Zeitverlauf")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Artikelanzahl")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    elif analysis_option == "Artikelanzahl im Verhältnis zu allen Artikeln":
        # Artikelanzahl im Verhältnis zu allen Artikeln
        filtered_df["relative_articles"] = filtered_df["Article Count"] / filtered_df["All Articles"]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(filtered_df["datetime"], filtered_df["relative_articles"], label="Relativer Anteil", color="green")
        ax.set_title("Relativer Anteil der Artikel im Zeitverlauf")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Anteil der Artikel")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# Footer
st.sidebar.markdown("Datenquelle: Green Deal Data Explorer")
