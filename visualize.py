import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# GitHub-RAW-URL zur CSV-Datei
github_csv_url = "https://raw.githubusercontent.com/Holzkopfblob/DataX/main/green_deal_data.csv"

# Daten laden
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['Article Ratio'] = df['Article Count'] / df['All Articles']
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return pd.DataFrame()

df = load_data(github_csv_url)

# Überprüfen, ob Daten erfolgreich geladen wurden
if df.empty:
    st.stop()

# Titel und Sidebar
st.title("Green Deal Datenanalyse")
st.sidebar.header("Filteroptionen")

# Zeitbereich filtern
start_date = st.sidebar.date_input("Startdatum", value=df['datetime'].min().date())
end_date = st.sidebar.date_input("Enddatum", value=df['datetime'].max().date())
df_filtered = df[(df['datetime'] >= pd.Timestamp(start_date)) & (df['datetime'] <= pd.Timestamp(end_date))]

# Diagramm 1: Artikelanzahl
st.header("Artikelanzahl im Zeitverlauf")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered['datetime'], df_filtered['Article Count'], label="Artikelanzahl", color="blue")
ax.set_title("Artikelanzahl im Zeitverlauf")
ax.set_xlabel("Datum")
ax.set_ylabel("Anzahl")
ax.grid(True)
st.pyplot(fig)

# Diagramm 2: Verhältnis Artikel zu allen Artikeln
st.header("Verhältnis Artikel zu allen Artikeln")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered['datetime'], df_filtered['Article Ratio'], label="Artikelanteil", color="green")
ax.set_title("Artikelanteil im Verhältnis zu allen Artikeln")
ax.set_xlabel("Datum")
ax.set_ylabel("Anteil")
ax.grid(True)
st.pyplot(fig)

# Datentabelle anzeigen
st.header("Gefilterte Daten")
st.dataframe(df_filtered)

# Download der Daten
csv_download = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="Daten als CSV herunterladen", data=csv_download, file_name="filtered_data.csv", mime="text/csv")
