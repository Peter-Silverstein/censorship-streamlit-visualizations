import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
from itertools import combinations
import networkx as nx
from pyvis.network import Network
import research_papers
import matplotlib.pyplot as plt
import re
import plotly.express as px


def run():
    # ACTUAL STREAMLIT APP
    st.markdown('<div id="redacted-title">REDACTED</div>', unsafe_allow_html=True)
    @st.cache_data
    def load_data():
        df = pd.read_csv('abstracts.csv')
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

    banned_words = pd.read_csv('banned_words.txt', header=None).values.flatten().tolist()
    banned_words = [word.lower() for word in banned_words]
    df['abstract_lower'] = df['abstract'].str.lower()

    # Check if any banned word appears in the abstract
    def contains_banned(abstract):
        return any(re.search(rf'\b{re.escape(word)}\b', str(abstract), re.IGNORECASE) for word in banned_words)

    # Apply function
    df['contains_banned'] = df['abstract_lower'].apply(contains_banned)

    from collections import Counter

    # Only keep titles that contain banned words
    banned_titles = df[df['contains_banned']]['abstract_lower']

    # Count banned words
    word_counter = Counter()

    for title in banned_titles:
        for word in banned_words:
            if word in title:
                word_counter[word] += 1

    # visualization
    word_counts = pd.DataFrame.from_dict(word_counter, orient='index', columns=['count']).sort_values('count', ascending=False)
    
    # PARAGRAPH 1
    percent_banned = df['contains_banned'].mean() * 100
    percent_text = f"""{percent_banned:.2f}% contained flagged words as listed by the <a href="https://www.nytimes.com/interactive/2025/03/07/us/trump-federal-agencies-websites-words-dei.html" target="_blank" style="color: inherit; text-decoration: underline;">New York Times</a>."""
    st.markdown('<div class="typewriter-1">Out of 1000 abstracts selected from top journals,</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="typewriter-2">{percent_text}</div>', unsafe_allow_html=True)

    
    fig = px.bar(
        word_counts.reset_index(),
        x='index',       # banned words
        y='count',       # their frequency
        labels={'index': 'Banned Word', 'count': 'Count'},
        title='Banned Words Frequency in Research Abstracts',
        color_discrete_sequence=['red']  # make bars red
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        bargap=0.2
    )
    st.plotly_chart(fig, use_container_width=True)

    # PARAGRAPH 2
    st.markdown('<div class="typewriter">Connecting redacted narratives...</div>', unsafe_allow_html=True)
