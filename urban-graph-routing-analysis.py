import osmnx as ox
import random
import heapq
import time
import matplotlib.pyplot as plt

# Cargar el grafo
place_name = "Tamazula de Gordiano, Jalisco, Mexico"
G = ox.graph_from_place(place_name, network_type="drive")

# Configuracion inicial de aristas
for edge in G.edges:
    Velocidad_mx = 40
    if "Velocidad_mx" in G.edges[edge]:
        Velocidad_mx = G.edges[edge]["Velocidad_mx"]
        if isinstance(Velocidad_mx, list):
            Velocidad_mx = min([int(vel) for vel in Velocidad_mx])
        elif isinstance(Velocidad_mx, str):
            Velocidad_mx = int(Velocidad_mx)
    G.edges[edge]["Velocidad_mx"] = Velocidad_mx
    G.edges[edge]["Pes"] = G.edges[edge]["length"] / Velocidad_mx

# Estilos para nodos y aristas
def estilo_nov_edge(edge):
    G.edges[edge].update({"color": "#cccccc", "alpha": 0.3, "Linea": 0.5})

def estilo_mst_edge(edge):
    G.edges[edge].update({"color": "#34a853", "alpha": 1, "Linea": 2})

def estilo_ruta_edge(edge):
    G.edges[edge].update({"color": "#1a73e8", "alpha": 1, "Linea": 3})

def estilo_punto_inicio(node):
    G.nodes[node].update({"color": "#ea4335", "tamano": 120})

def estilo_punto_destino(node):
    G.nodes[node].update({"color": "#34a853", "tamano": 120})

# Funcion para dibujar el grafo
def plot_graph(title):
    fig, ax = ox.plot_graph(
        G,
        node_size=[G.nodes[node].get("tamano", 0) for node in G.nodes],
        edge_color=[G.edges[edge]["color"] for edge in G.edges],
        edge_alpha=[G.edges[edge]["alpha"] for edge in G.edges],
        edge_linewidth=[G.edges[edge]["Linea"] for edge in G.edges],
        node_color=[G.nodes[node].get("color", "#f0f0f0") for node in G.nodes],
        bgcolor="white",
        show=False,
        close=False,
    )
    ax.set_title(title, color="black", fontsize=15)
    plt.show()

def prim(orig, dest, title):
    for node in G.nodes:
        G.nodes[node]["tamano"] = 0
    for edge in G.edges:
        estilo_nov_edge(edge)

    visitado = {orig}
    pq = []
    mst_edges = []

    def add_edges(node):
        for neighbor in G.neighbors(node):
            edge = (node, neighbor, 0)
            if neighbor not in visitado:
                heapq.heappush(pq, (G.edges[edge]["Pes"], edge))

    add_edges(orig)
    while pq:
        peso, edge = heapq.heappop(pq)
        node1, node2, _ = edge
        if node2 not in visitado:
            visitado.add(node2)
            mst_edges.append(edge)
            estilo_mst_edge(edge)
            add_edges(node2)

    # Obtener y graficar la mejor ruta dentro del arbol MST
    path = []
    current_node = dest
    parents = {edge[1]: edge[0] for edge in mst_edges}
    while current_node != orig:
        path.append((parents[current_node], current_node, 0))
        current_node = parents[current_node]

    for edge in path:
        estilo_ruta_edge(edge)

    estilo_punto_inicio(orig)
    estilo_punto_destino(dest)
    plot_graph(title)

# Algoritmo de Dijkstra
def dijkstra(orig, dest, title):
    for node in G.nodes:
        G.nodes[node].update({"visitado": False, "distancia": float("inf"), "Anterior": None, "tamano": 0})
    for edge in G.edges:
        estilo_nov_edge(edge)

    G.nodes[orig]["distancia"] = 0
    estilo_punto_inicio(orig)
    estilo_punto_destino(dest)

    pq = [(0, orig)]
    while pq:
        _, node = heapq.heappop(pq)
        if node == dest:
            path = []
            while node is not None:
                path.append(node)
                node = G.nodes[node]["Anterior"]
            path.reverse()
            for i in range(len(path) - 1):
                edge = (path[i], path[i + 1], 0)
                estilo_ruta_edge(edge)
            plot_graph(title)
            return path

        if G.nodes[node]["visitado"]:
            continue
        G.nodes[node]["visitado"] = True

        for edge in G.out_edges(node, keys=True):
            neighbor = edge[1]
            peso = G.edges[edge]["Pes"]
            if G.nodes[neighbor]["distancia"] > G.nodes[node]["distancia"] + peso:
                G.nodes[neighbor]["distancia"] = G.nodes[node]["distancia"] + peso
                G.nodes[neighbor]["Anterior"] = node
                heapq.heappush(pq, (G.nodes[neighbor]["distancia"], neighbor))

# Funcion para medir tiempos y generar una grafica consolidada
def ejecutar_analisis_crecimiento_grafo(ejemplos=3):
    tamaños_grafo = []
    tiempos_dijkstra_global = []
    tiempos_prim_global = []

    for tamano_subgrafo in range(50, len(G.nodes), max(1, len(G.nodes) // 5)):
        print(f"\n*** Analizando subgrafo con {tamano_subgrafo} nodos ***")

        # Seleccion aleatoria de nodos del subgrafo
        nodos_subgrafo = random.sample(list(G.nodes), tamano_subgrafo)
        subgrafo = G.subgraph(nodos_subgrafo).copy()

        # Seleccion de puntos A, B y C
        A = nodos_subgrafo[0]
        B = nodos_subgrafo[len(nodos_subgrafo) // 2]
        C = nodos_subgrafo[-1]

        # Tiempos de Dijkstra
        print(f"Ejecutando Dijkstra: A → B → C en subgrafo de {tamano_subgrafo} nodos...")
        start_time = time.time()
        dijkstra(A, B, f"Dijkstra: A → B en subgrafo ({tamano_subgrafo} nodos)")
        dijkstra(B, C, f"Dijkstra: B → C en subgrafo ({tamano_subgrafo} nodos)")
        tiempo_dijkstra = time.time() - start_time
        print(f"Tiempo Dijkstra A → B → C: {tiempo_dijkstra:.4f} segundos \n")
        tiempos_dijkstra_global.append(tiempo_dijkstra)

        # Tiempos de Prim
        print(f"Ejecutando Prim en subgrafo de {tamano_subgrafo} nodos...")
        start_time = time.time()
        prim(A, B, f"Prim: Arbol y ruta (A → B, {tamano_subgrafo} nodos)")
        prim(B, C, f"Prim: Arbol y ruta (B → C, {tamano_subgrafo} nodos)")
        tiempo_prim = time.time() - start_time
        print(f"Tiempo Prim A → B → C: {tiempo_prim:.4f} segundos \n")
        tiempos_prim_global.append(tiempo_prim)

        tamaños_grafo.append(tamano_subgrafo)

    # Graficar tiempos
    plt.figure(figsize=(10, 6))
    plt.plot(tamaños_grafo, tiempos_dijkstra_global, marker="o", label="Dijkstra", color="blue")
    plt.plot(tamaños_grafo, tiempos_prim_global, marker="o", label="Prim", color="green")

    # Añadir descripcion en la parte superior
    plt.suptitle(
        "Comparacion de Dijkstra y Prim en subgrafos de tamaño creciente",
        color="white", fontsize=14, fontweight="bold", backgroundcolor="#18080e"
    )
    plt.title(
        "Se muestran los tiempos de ejecucion de Dijkstra y Prim para rutas A → B → C "
        "en subgrafos generados aleatoriamente con tamaños crecientes.",
        fontsize=10, color="white"
    )

    # Configuracion de etiquetas y graficos
    plt.xlabel("Cantidad de nodos en el grafo", fontsize=10)
    plt.ylabel("Tiempo de ejecucion (s)", fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Mostrar grafica
    plt.show()

# Ejecutar
ejecutar_analisis_crecimiento_grafo()