import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Importing Data
edges = pd.read_csv("network-graphs/edges.csv")
edges = edges[edges['domain'] == 'epa.gov']

st.title('Network Test Graph')

domain_list = ["epa.gov", "noaa.gov", "sustainability.gov"]
selected_domain = st.multiselect("Select domain(s) to visualize", domain_list)

# ADD SLIDER

if len(selected_domain) == 0:
    G = nx.from_pandas_edgelist(edges, "source", "target")

    network = Network(height = '435px', bgcolor='white', font_color = 'black', cdn_resources='remote')
    network.from_nx(G)
    network.repulsion(node_distance=400, central_gravity=0.33,
                       spring_length=2, spring_strength=0.10,
                       damping=0.95)
    
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        network.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')
    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        network.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')

    components.html(HtmlFile.read(), height = 450)

else:
    st.text("Select TEST TEst")

