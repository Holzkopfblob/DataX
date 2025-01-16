import pandas as pd
import matplotlib.pyplot as plt
import os

# Verzeichnisse festlegen
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "data", "raw", "green_deal_data.csv")
output_dir = os.path.join(base_dir, "data", "outputs")
os.makedirs(output_dir, exist_ok=True)

# CSV-Datei laden
df = pd.read_csv(data_path)

# Spaltennamen prüfen und konvertieren
required_columns = ['datetime', 'Article Count', 'All Articles']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Die Spalte '{col}' fehlt in der CSV-Datei.")

df['datetime'] = pd.to_datetime(df['datetime'])

# Diagramm 1: Artikelanzahl im Zeitverlauf
plt.figure(figsize=(12, 6))
plt.plot(df['datetime'], df['Article Count'], label="Artikelanzahl", color="blue")
plt.title("Artikelanzahl im Zeitverlauf (Green Deal)")
plt.xlabel("Datum")
plt.ylabel("Artikelanzahl")
plt.legend()
plt.grid(True)
output_file_1 = os.path.join(output_dir, "green_deal_article_count_timeline.png")
plt.savefig(output_file_1)
plt.show()

print(f"Diagramm 1 gespeichert unter: {output_file_1}")

# Diagramm 2: Verhältnis von Artikeln zu allen Artikeln im Zeitverlauf
df['Article Ratio'] = df['Article Count'] / df['All Articles']

plt.figure(figsize=(12, 6))
plt.plot(df['datetime'], df['Article Ratio'], label="Artikelanteil (%)", color="green")
plt.title("Artikelanteil im Verhältnis zu allen Artikeln im Zeitverlauf (Green Deal)")
plt.xlabel("Datum")
plt.ylabel("Artikelanteil (%)")
plt.legend()
plt.grid(True)
output_file_2 = os.path.join(output_dir, "green_deal_article_ratio_timeline.png")
plt.savefig(output_file_2)
plt.show()

print(f"Diagramm 2 gespeichert unter: {output_file_2}")
