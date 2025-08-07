# 🏙️ Urban Graph Routing Analysis – Dijkstra & Prim

This project implements and compares **Dijkstra's** and **Prim's** algorithms on real-world urban road networks using **OSMnx**.  
Developed as a final project for the **Analysis of Algorithms** course.

## 📌 Objective

To analyze shortest paths and minimum spanning trees (MST) in a real city graph, evaluate scalability, and visualize algorithm performance.

## 🛣️ Dataset

- City: *Tamazula de Gordiano, Jalisco, Mexico*
- Source: OpenStreetMap via OSMnx

## ⚙️ Algorithms

- **Dijkstra**: shortest path between A → B → C using edge weights as time (distance / speed)
- **Prim**: MST built from a given node, visualizing optimal paths within the tree

## 📊 Visualization

- Road network and routes plotted with **matplotlib**
- Color-coded:
  - Gray: untouched edges
  - Green: MST edges
  - Blue: optimal path
- Nodes marked for origin/destination

## 📈 Performance Evaluation

The `ejecutar_analisis_crecimiento_grafo()` function runs multiple experiments:
- Builds subgraphs of increasing size
- Runs Dijkstra and Prim on selected nodes
- Measures and plots execution time

## 🧪 Libraries

- osmnx
- heapq
- random
- time
- matplotlib
- networkx

## 🧠 Authors

- Jesús Antonio Torres Contreras  
- Luis Ángel Lozano Reyes

## 📚 License
This project is for academic and educational purposes.
