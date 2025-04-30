def run_bookbans():
    import streamlit as st
    import pandas as pd
    import folium
    from streamlit_folium import st_folium

    # Fix: @st.cache_data needs to decorate a function
    @st.cache_data
    def load_data():
        DATA_URL = 'combined_bans.csv'
        data = pd.read_csv(DATA_URL)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        return data
    
    st.markdown("""
    <style>
    .st-bo {
        background-color: rgb(0, 0, 0); important! 
    }
                
    .plain-text {
        font-size: 15px;   
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        animation: fadeIn 0.5s ease-in forwards;
        animation-delay: 0s;
        opacity: 0;
        position: relative;
    }                             
    </style>
    """, unsafe_allow_html=True)

    # Function to plot bans by year
    def plot_bans_by_year(df, year):
        df = df.copy()
        df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year  # Isolate year
        filtered = df[df['year'] == year]
        state_counts = filtered.groupby('state').size().reset_index(name='bans')
        
        # Get lat/lon info
        state_coords_df = df[['state', 'lat', 'lon']].drop_duplicates()
        state_counts = state_counts.merge(state_coords_df, on='state', how='left')

        m = folium.Map(location=[39.5, -98.35], zoom_start=4)
        for _, row in state_counts.dropna(subset=['lat', 'lon']).iterrows():
            folium.CircleMarker(
                location=(row['lat'], row['lon']),
                radius=row['bans']**0.5 / 2,
                popup=f"{row['state']}: {row['bans']} bans in {year}",
                color='crimson',
                fill=True,
                fill_opacity=0.6
            ).add_to(m)

        return m

    # Start of Streamlit app
    st.markdown('<div class="plain-text">Book bans are a form of censorship that can have significant implications for free speech, intellectual freedom, and access to information. In the United States, book bans have been a contentious issue, with various states and school districts implementing restrictions on certain books in libraries and classrooms.</div>', unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Slider for year
    year_to_filter = st.slider('Select Year', 2021, 2023, 2023)

    # Plot folium map
    st.subheader(f"Book Bans in {year_to_filter}")
    folium_map = plot_bans_by_year(data, year_to_filter)
    st_folium(folium_map, width=700, height=500)

# To run
# run_bookbans()

