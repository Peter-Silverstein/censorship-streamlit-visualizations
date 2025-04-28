import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
from itertools import combinations
import networkx as nx
from pyvis.network import Network
import research_papers

def run():
    # ACTUAL STREAMLIT APP
    st.markdown('<div id="redacted-title">REDACTED</div>', unsafe_allow_html=True)
    @st.cache_data
    def load_data():
        df = pd.read_csv('banned_words.csv')
        return df

    df = load_data()

    #styling for the python code 
    st.markdown("""
    <style>
    .st-bo {
        background-color: rgb(0, 0, 0); important! 
    }
    </style>
    """, unsafe_allow_html=True)


    # PARAGRAPH 1
    st.markdown('<div class="typewriter"> </div>', unsafe_allow_html=True)

    # NETWORK GRAPH - RESEARCH TEMRS BEING REMOVED CLUSTERED BY THEME
    all_themes = sorted(set([theme.strip() for themes in df['Themes'] for theme in themes.split(',')]))
    selected_themes = st.multiselect("Select Themes to View:", options=all_themes, default=all_themes)

    filtered_df = df[df['Themes'].apply(lambda x: any(theme.strip() in selected_themes for theme in x.split(',')))]

    theme_pairs = []

    for themes in filtered_df['Themes']:
        theme_list = [theme.strip() for theme in themes.split(',')]
        if len(theme_list) > 1:
            for pair in combinations(sorted(theme_list), 2):
                theme_pairs.append(pair)

    pair_df = pd.DataFrame(theme_pairs, columns=['Theme1', 'Theme2'])
    G = nx.Graph()

    for (theme1, theme2), count in pair_df.value_counts().items():
        G.add_edge(theme1, theme2, weight=count)

    net = Network(height="750px", width="100%", bgcolor="white", font_color="black")

    for node in G.nodes:
        net.add_node(node, label=node)

    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, value=data['weight'])

    net.repulsion(node_distance=200, central_gravity=0.3, spring_length=200, spring_strength=0.05, damping=0.95)

    net.save_graph('network.html')
    HtmlFile = open('network.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=800)

    # PARAGRAPH 2
    st.markdown('<div class="typewriter">Connecting redacted narratives...</div>', unsafe_allow_html=True)
