import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Daten laden
@st.cache_data
def load_data():
    df = pd.read_csv("green_deal_data.csv")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")  # Konvertiere zu datetime
    return df

# Daten laden
df = load_data()

# Streamlit Widgets für Interaktivität
st.sidebar.header("Filtereinstellungen")
date_range = st.sidebar.date_input(
    "Zeitraum auswählen",
    [pd.to_datetime("2019-01-01"), pd.to_datetime("2023-12-31")]
)

aggregation = st.sidebar.number_input(
    "Aggregation (Tage pro Datenpunkt)",
    min_value=1,
    max_value=365,
    value=7
)

show_events = st.sidebar.checkbox("Ereignisse anzeigen", value=True)

# Daten filtern
try:
    df_filtered = df[(df["datetime"] >= pd.to_datetime(date_range[0])) & 
                     (df["datetime"] <= pd.to_datetime(date_range[1]))]
except Exception as e:
    st.error(f"Fehler beim Filtern der Daten: {e}")

# Daten aggregieren
df_filtered["datetime"] = df_filtered["datetime"].dt.to_period(f"{aggregation}D").dt.start_time
df_aggregated = df_filtered.groupby("datetime").sum().reset_index()

# Ereignisse laden und filtern
events = [
    {"date": "2019-05-23", "description": "Europawahl"},
    {"date": "2020-12-12", "description": "Klimakonferenz COP26"},
    # Weitere Ereignisse hier hinzufügen
]
df_events = pd.DataFrame(events)
df_events["date"] = pd.to_datetime(df_events["date"])
filtered_events = df_events[
    (df_events["date"] >= pd.to_datetime(date_range[0])) &
    (df_events["date"] <= pd.to_datetime(date_range[1]))
]

# Plot erstellen
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_aggregated["datetime"], df_aggregated["Article Count"], label="Artikelanzahl", color="blue")
if show_events:
    for _, event in filtered_events.iterrows():
        ax.axvline(event["date"], color="red", linestyle="--", alpha=0.7)
        ax.text(event["date"], max(df_aggregated["Article Count"])*0.8, f"{event.name+1}", 
                rotation=90, color="red", fontsize=8)
plt.xlabel("Datum")
plt.ylabel("Artikelanzahl")
plt.title("Artikelanzahl im Zeitverlauf")
plt.legend()
plt.grid()

# Plot anzeigen
st.pyplot(fig)

# Ereignisse anzeigen
if show_events:
    st.write("**Ereignisse:**")
    st.write(filtered_events)
