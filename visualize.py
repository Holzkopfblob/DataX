import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Daten laden
data_path = "data/raw/green_deal_data.csv"
df = pd.read_csv(data_path)

# Daten vorbereiten
df['datetime'] = pd.to_datetime(df['datetime'])
df['Article Ratio'] = df['Article Count'] / df['All Articles']

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
