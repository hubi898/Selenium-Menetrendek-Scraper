from pyvis.network import Network
import pandas as pd

# Excel betöltése (eredeti adat és csomópontok színei, méretei)
excel_data = pd.ExcelFile("data3.xlsx")
df = excel_data.parse(excel_data.sheet_names[0])

# Csomópontok attribútumokat tartalmazó másik Excel fájl betöltése
attrib_excel_data = pd.ExcelFile("city_population.xlsx")
attrib_df = attrib_excel_data.parse(attrib_excel_data.sheet_names[0])

# Élek szűrése
edges = df[df["Kapcsolat"] == "Van kapcsolat"]

# PyVis háló létrehozása
net = Network(height="800px", width="100%", bgcolor="#D3D3D3", font_color="black", notebook=True)

# Csomópontok és élek hozzáadása
for node in pd.concat([df["Induló hely"], df["Érkező hely"]]).unique():
    net.add_node(node, label=node, title=node)  # Nevek hozzáadása

# Élek hozzáadása
for _, row in edges.iterrows():
    net.add_edge(row["Induló hely"], row["Érkező hely"])

# Csomópontok attribútumainak hozzáadása (pl. populáció)
for idx, row in attrib_df.iterrows():
    node = row["Node"]
    population = row["Population"]
    
    # Ha a csomópont szerepel az élekben
    if node in [n['id'] for n in net.nodes]:
        # Méret beállítása a populáció alapján, skálázva
        net.get_node(node)["size"] = population / 50  # Méret a populáció alapján
        net.get_node(node)["title"] = f"Populáció: {population}"

# Fizika kikapcsolása, hogy szabadon mozgathassuk a csomópontokat
net.set_options("""
var options = {
  "physics": {
    "enabled": false
  },
  "manipulation": {
    "enabled": true
  }
}
""")

# Interaktív hálózat megjelenítése
net.show("interactive_graph.html")
