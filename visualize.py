import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    df = pd.read_csv("green_deal_data.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filtereinstellungen")
start_date, end_date = st.sidebar.date_input(
    "Wähle den Zeitraum:",
    [df["datetime"].min().date(), df["datetime"].max().date()],
    min_value=df["datetime"].min().date(),
    max_value=df["datetime"].max().date(),
)

# Filter data
filtered_df = df[df["datetime"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))]

# Main title
st.title("Green Deal Data Explorer")
st.success("Daten erfolgreich geladen!")

# Visualization 1: Articles over time
st.header("Artikelanzahl im Zeitverlauf")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(filtered_df["datetime"], filtered_df["Article Count"], label="Artikelanzahl", color="blue")
ax.set_title("Artikelanzahl im Zeitverlauf")
ax.set_xlabel("Datum")
ax.set_ylabel("Anzahl der Artikel")
ax.grid(True)
st.pyplot(fig)

# Visualization 2: Articles vs Total Articles Ratio
st.header("Verhältnis der Artikelanzahl zur Gesamtartikelanzahl")
filtered_df["Article Ratio"] = filtered_df["Article Count"] / filtered_df["All Articles"]
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(filtered_df["datetime"], filtered_df["Article Ratio"], label="Artikelverhältnis", color="green")
ax2.set_title("Verhältnis der Artikelanzahl zur Gesamtartikelanzahl")
ax2.set_xlabel("Datum")
ax2.set_ylabel("Verhältnis")
ax2.grid(True)
st.pyplot(fig2)
