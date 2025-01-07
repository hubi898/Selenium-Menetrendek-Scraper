import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Excel betöltése (eredeti adat és csomópontok színei, méretei)
excel_data = pd.ExcelFile("data3.xlsx")
df = excel_data.parse(excel_data.sheet_names[0])

# Csomópontok attribútumokat tartalmazó másik Excel fájl betöltése
attrib_excel_data = pd.ExcelFile("city_population.xlsx")
attrib_df = attrib_excel_data.parse(attrib_excel_data.sheet_names[0])

# Élek szűrése
edges = df[df["Kapcsolat"] == "Van kapcsolat"]

# Gráf létrehozása
graph = nx.DiGraph()
for node in pd.concat([df["Induló hely"], df["Érkező hely"]]).unique():
    graph.add_node(node)
graph.add_edges_from(zip(edges["Induló hely"], edges["Érkező hely"]))

# Attribútumok hozzáadása: csak a populáció
node_sizes = {}

# Az attrib_df-nek tartalmaznia kell a csomópont nevét és populációját
for idx, row in attrib_df.iterrows():
    node = row["Node"]  # Node oszlop neve
    population = row["Population"]  # Population oszlop neve
    # A csomópont méretének beállítása (proporcionálisan)
    node_sizes[node] = population * 2  # Ezt a szorzót igény szerint módosíthatod

# Központiság számítása
degree_centrality = nx.degree_centrality(graph)
in_degree_centrality = nx.in_degree_centrality(graph)
out_degree_centrality = nx.out_degree_centrality(graph)
betweenness_centrality = nx.betweenness_centrality(graph)
closeness_centrality = nx.closeness_centrality(graph)
density = nx.density(graph)

# Központiság kiírása
print("Fokszámok (Degree Centrality):")
print(pd.DataFrame([(node, dc) for node, dc in degree_centrality.items()], columns=['Node', 'Degree Centrality']))
print("Bejövő Fokszámok (In-Degree Centrality):")
print(pd.DataFrame([(node, dc) for node, dc in in_degree_centrality.items()], columns=['Node', 'In-Degree Centrality']))
print("\nKimenő Fokszámok (Out-Degree Centrality):")
print(pd.DataFrame([(node, dc) for node, dc in out_degree_centrality.items()], columns=['Node', 'Out-Degree Centrality']))
print("\nKözpontiság (Betweenness Centrality):")
print(pd.DataFrame([(node, bc) for node, bc in betweenness_centrality.items()], columns=['Node', 'Betweenness Centrality']))
print(f"\nSűrűség: {density}")
print("\nElérhetőség (Closeness Centrality):")
print(pd.DataFrame([(node, cc) for node, cc in closeness_centrality.items()], columns=['Node', 'Closeness Centrality']))

# Interconnectednesst számítása
interconnectivity = nx.average_node_connectivity(graph)
print(f"\nInterconnectednesst (átlagos csomópont-összekapcsoltság): {interconnectivity}")

# Összefüggő komponensek számítása
strongly_connected_components = list(nx.strongly_connected_components(graph))

# Ha van több mint egy összefüggő komponens, akkor az azt jelenti, hogy nem minden csomópont kapcsolódik össze
if len(strongly_connected_components) > 1:
    print("\nNem összefüggő komponensek:")
    for i, component in enumerate(strongly_connected_components, 1):
        print(f"\nKomponens {i}: {component}")
else:
    print("\nA gráf összefüggő.")

# Leghosszabb és legrövidebb út számítása

# A leghosszabb út számítása (gráf átmérője)
if nx.is_connected(graph.to_undirected()):
    diameter = nx.diameter(graph.to_undirected())
    print(f"\nLeghosszabb út (Gráf átmérője): {diameter} csomópont")
else:
    print("\nA gráf nem összefüggő, így nem lehet meghatározni a leghosszabb utat.")

# Spring layout használata
pos = nx.kamada_kawai_layout(graph)

# Rajzolás csomópont-méretezéssel
node_sizes_list = [node_sizes.get(node, 10) * 5 for node in graph.nodes()]  # Az alapértelmezett méret 100
plt.figure(figsize=(12, 10), facecolor='#D3D3D3')
nx.draw(graph, pos, with_labels=True, node_size=node_sizes_list, font_size=10, font_color="black", edge_color="gray", width=1)
plt.title("Átlátható gráf vizualizáció")
plt.show()
