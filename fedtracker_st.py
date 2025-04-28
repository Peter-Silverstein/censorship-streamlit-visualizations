import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import regex as re

# Get Data
@st.cache_data
def get_fed_data():
    df = pd.read_csv("envirofedtracker.csv")

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
    # simplified_agency_counts.loc[4,'midpoint_norm'] = simplified_agency_counts.loc[4,'midpoint_norm'] + 0.01
    # simplified_agency_counts['text_position'] = simplified_agency_counts["text_position"] - 0.5*simplified_agency_counts["Count"]

    # Topics DataFrame
    df_topics = df[["Agency", "Topic 1", "Topic 2"]].copy()
    df_topics['ID'] = df.index
    df_long = pd.melt(df_topics, 
                  id_vars=['ID', "Agency"], 
                  value_vars=['Topic 1', 'Topic 2'],
                  var_name='value',
                  value_name='Topic')
    df_long = df_long.drop("value", axis = 1).dropna()
    agencies = pd.unique(df_long['Agency'])
    return df_long, agencies, simplified_agency_counts

def filter_data(df, agency = None):
    filtered_df = df
    if agency:
        filtered_df = filtered_df[filtered_df['Agency'] == agency]
        
    return filtered_df

def main():
    st.set_page_config(layout="wide")

    st.header("Climate Censorship on Government Websites")
    df_long, agencies, simplified_agency_counts = get_fed_data()

    agency_order = ["EPA", "DOT", "NOAA", "CEQ", "USGCRP", "OTHER"]
    range_ = ['#00908F', '#0A3E94', '#488026', '#30312F', '#918224', '#8A1D21']

    agency_bars = alt.Chart(simplified_agency_counts).mark_bar().encode(
    x=alt.X('sum(Count):Q', axis=None).stack("normalize"),
    y=alt.value(1),
    color=alt.Color('Agency:N', legend=None, 
                sort={'field': 'Count', 'order': 'descending'},
                scale=alt.Scale(domain=agency_order, range=range_)),
    order=alt.Order('agency_order:Q', sort='ascending')
    )
    
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

    st.subheader("Which US Federal Agencies are most affected?")
    st.altair_chart(agency_chart, use_container_width=True)

    col1, col2 = st.columns([1,5])

    with col1:
        agency = st.selectbox(
            "Select an agency",
            agencies,
            index=None,
            placeholder="All agencies"
        )

    filtered_df = filter_data(df_long, agency)
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df['Topic'] = filtered_df['Topic'].apply(lambda x: re.sub(r'[^\x20-\x7E]', '', str(x)))
    filtered_df['Topic'] = filtered_df['Topic'].str.strip().str.replace(r'\s+', ' ', regex=True)
    grouped_counts = filtered_df.groupby(['Topic']).size().reset_index(name='Count')

    with col2:
        topics_chart = alt.Chart(grouped_counts).mark_bar().encode(
                x=alt.X('Count:Q'),
                y=alt.Y('Topic', title=None, sort = '-x'),
                tooltip=['Topic', 'Count']
            ).properties(
                title="Topics by Change Type",
                width=150
            ).interactive()
        
        st.altair_chart(topics_chart, use_container_width=True)

if __name__ == "__main__":
    main()