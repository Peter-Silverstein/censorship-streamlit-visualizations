import pandas as pd
import networkx as nx
import altair as alt
import altair_nx as nxa
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="Network Graph", layout="wide")

st.legacy_altair_chart = True  # Use legacy serialization

nodes = pd.read_csv("network-graphs/nodes.csv")
edges = pd.read_csv("network-graphs/edges.csv")

nodes_epa = nodes[nodes['domain'] == "epa.gov"]
edges_epa = edges[edges['source_domain'] == "epa.gov"]

nodes_noaa = nodes[nodes['domain'] == "noaa.gov"]
edges_noaa = edges[edges['source_domain'] == "noaa.gov"]

nodes_sust = nodes[nodes['domain'] == "sustainability.gov"]
edges_sust = edges[edges['source_domain'] == "sustainability.gov"]

G_epa = nx.Graph()

for _, row in nodes_epa.iterrows():
    node_id = str(row.iloc[0])
    timestamp = row.iloc[2]
    G_epa.add_node(node_id, timestamp = timestamp)

for _, row in edges_epa.iterrows():
    source = str(row.iloc[0])
    target = str(row.iloc[2])
    timestamp = row.iloc[3]
    G_epa.add_edge(source, target, timestamp = timestamp)

# Convert NetworkX graph to agraph format
nodes = [Node(id=str(n), label=str(n)) for n in G_epa.nodes()]
edges = [Edge(source=str(e[0]), target=str(e[1])) for e in G_epa.edges()]

config = Config(width=700, height=500, physics=False, 
                hierarchical=False, staticGraph=True,
                directed=True, collapsible=True,)
                
return_value = agraph(nodes=nodes, edges=edges, config=config)
return_value