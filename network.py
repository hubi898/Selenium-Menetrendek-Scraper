import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Excel betöltése (eredeti adat és csomópontok színei, méretei)
excel_data = pd.ExcelFile("data4.xlsx")
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

# Reciprocitás kiszámítása minden csomópontra
reciprocity = {}
for node in graph.nodes:
    total_edges = graph.out_degree(node) + graph.in_degree(node)
    reciprocal_edges = sum(1 for neighbor in graph.successors(node) if graph.has_edge(neighbor, node))
    reciprocity[node] = reciprocal_edges / total_edges if total_edges > 0 else 0

# Reciprocitás kiírása
print("\nReciprocitás (csomópontokra lebontva):")
print(pd.DataFrame([(node, r) for node, r in reciprocity.items()], columns=['Node', 'Reciprocity']))

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

# A leghosszabb út számítása (gráf átmérője)
if nx.is_connected(graph.to_undirected()):
    diameter = nx.diameter(graph.to_undirected())
    print(f"\nLeghosszabb út (Gráf átmérője): {diameter} csomópont")
else:
    print("\nA gráf nem összefüggő, így nem lehet meghatározni a leghosszabb utat.")

#layout beállítása
pos = nx.kamada_kawai_layout(graph)

# Rajzolás csomópont-méretezéssel
node_sizes_list = [node_sizes.get(node, 10) * 3 for node in graph.nodes()]  # Az alapértelmezett méret 100
plt.figure(figsize=(12, 10))
ax = plt.gca()

nx.draw(graph, pos, with_labels=True, node_size=node_sizes_list, font_size=10, font_color="black", edge_color="gray", width=1)
plt.title("Átlátható gráf vizualizáció")
plt.show()
