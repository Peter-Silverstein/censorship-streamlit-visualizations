import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import regex as re

st.markdown("""
    <style>
    .st-bo {
        background-color: rgb(0, 0, 0); !important
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

# Run!
def run_fedtracker():
    
    @st.cache_data
    def get_fed_data():
        df = pd.read_csv("envirofedtracker.csv")
        agencies = pd.read_csv("agencylookup.csv")

        # Agency DataFrame
        agency = df['Agency'].value_counts()
        agency_df = agency.reset_index()
        agency_df.columns = ['Agency', 'Count']
        agency_df = agency_df.sort_values(by=['Count'], ascending = False)
        top5_agencies = agency_df.head(5)
        other_sum = agency_df.iloc[5:]['Count'].sum()
        simplified_agency_counts = pd.concat([
            top5_agencies,
            pd.DataFrame({'Agency': ['OTHER'], 'Count': [other_sum]})
            ], ignore_index=True)
        simplified_agency_counts['text_position'] = simplified_agency_counts['Count'].cumsum() - simplified_agency_counts['Count']
        simplified_agency_counts['text_position'] = simplified_agency_counts['text_position'] + simplified_agency_counts['Count'] / 2
        total = simplified_agency_counts['Count'].sum()
        simplified_agency_counts['midpoint_norm'] = simplified_agency_counts['text_position'] / total
            
        # Topics DataFrame
        df_topics = df[["Agency", "Topic 1", "Topic 2"]].copy()
        df_topics['ID'] = df.index
        df_long = pd.melt(df_topics, 
                    id_vars=['ID', "Agency"], 
                    value_vars=['Topic 1', 'Topic 2'],
                    var_name='value',
                    value_name='Topic')
        df_long = df_long.drop("value", axis = 1).dropna()
        # agencies = pd.unique(df_long['Agency'])
        return df_long, agencies, simplified_agency_counts

    def filter_data(df, agency = None):
        filtered_df = df
        if agency:
            filtered_df = filtered_df[filtered_df['Agency'] == agency]
            
        return filtered_df

    st.markdown('<div class="plain-text">Beyond censorship that occurs upstream, when funding is allocated to researchers, availability of existing information, research, and data can be censored as well. When scientific information is highly contested political territory (such as research on the climate or vaccines), the controlling party may choose to censor information that does not conform to their worldview. In this section, we offer an exploration of a dataset from the Environmental Data & Governance Initiative (EDGI). </div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="plain-text">The EDGI tracks environment-related content removal and accessibility changes made by the Trump Administration over the first few months of 2025. Changes are categorized with the agency they were associated with, as well as what topics they involved. For example, one entry for the Department of Transportation indicated that a menu link to the \'Climate and Sustainability\' page was removed, which was tagged with the \'Climate\' and \'Infrastructure\' tags. </div>', unsafe_allow_html=True)
    
    df_long, agencies, simplified_agency_counts = get_fed_data()

    agency_order = ["EPA", "DOT", "NOAA", "CEQ", "USGCRP", "OTHER"]
    range_ = ['#0b090a', '#161a1d', '#660708', '#a4161a', '#ba181b', '#e5383b']

    agency_bars = alt.Chart(simplified_agency_counts).mark_bar(
        stroke = 'white',
        strokeWidth = 2
    ).encode(
    x=alt.X('sum(Count):Q', axis=None).stack("normalize"),
    y=alt.value(1),
    color=alt.Color('Agency:N', legend=None, 
                sort={'field': 'Count', 'order': 'descending'},
                scale=alt.Scale(domain=agency_order, range=range_)),
    order=alt.Order('agency_order:Q', sort='ascending'),
    tooltip=['Agency', 'Count']
    ).interactive()
    
    agency_text = alt.Chart(simplified_agency_counts).mark_text(dy=70,
                                                                align='center').encode(
    x=alt.X('midpoint_norm:Q', axis = None),
    y=alt.value(1),
    detail='Agency:N',
    text=alt.Text(
        'Agency:N'
        ),
    order=alt.Order('agency_order:Q', sort='ascending')
    )
    
    agency_chart = (agency_bars + agency_text).properties(
    height=200
        ).configure_axis(
            grid=False
        )

    st.subheader("Which federal agency websites had the most climate-related content removals?")
    st.altair_chart(agency_chart, use_container_width=True)

    st.markdown('<div class="plain-text">Unsurprisingly, the EPA tops the list, but the Department of Transportation\'s presence in the top 5 shows how climate-related censorship actions pervade a variety of government agencies. In the following chart, you can examine what censorship actions look like for each of the federal entities within the dataset. Note the presence of both explicitly climate-related entities (e.g., EPA, NOAA) alongside ones that are, at a surface level, not related to climate (e.g., Department of Justice, Department of State).<div>', unsafe_allow_html=True)
 

    st.subheader("What are the changes related to?")

    col1, col2 = st.columns([1,5])

    with col1:
        agency = st.selectbox(
            "Select an agency",
            agencies["Agency"],
            index=None,
            placeholder="All agencies"
        )

        if agency:  
            longname = agencies.loc[agencies["Agency"] == agency, "LongName"].iloc[0]
        else:
            longname = "All Tracked Government Websites"

    filtered_df = filter_data(df_long, agency)
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df['Topic'] = filtered_df['Topic'].apply(lambda x: re.sub(r'[^\x20-\x7E]', '', str(x)))
    filtered_df['Topic'] = filtered_df['Topic'].str.strip().str.replace(r'\s+', ' ', regex=True)
    grouped_counts = filtered_df.groupby(['Topic']).size().reset_index(name='Count')

    with col2:
        topics_chart = alt.Chart(grouped_counts).mark_bar().encode(
                x=alt.X('Count:Q'),
                y=alt.Y('Topic', title=None, sort = '-x'),
                tooltip=['Topic', 'Count'],
            ).configure_bar(
                color="red"
                ).properties(
                title=longname,
                width=150
            )
        
        st.altair_chart(topics_chart, use_container_width=True)

# run_fedtracker()