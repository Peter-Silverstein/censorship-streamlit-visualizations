import streamlit as st
from streamlit_scroll_navigation import scroll_navbar
import time

# set up page
st.set_page_config(page_title="REDACTED", layout="wide")

#styling & html for title & typing things
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #ffffff;
    color: #000000;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

// set font everywhere
* {
    font-family: 'Courier New', monospace !important;
}

#redacted-title {
    font-size: 115px;
    font-weight: bold;
    text-align: center;
    opacity: 0;
    animation: fadeIn 2s ease-in forwards;
    animation-delay: 0s;
    margin-top: 50px;
    position: relative;
}
            
#byline {
    font-size: 13px;
    text-align: center;   
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    opacity: 0;
    animation: fadeIn 2s ease-in forwards;   
    position: relative; 
}
            
#section-title {
    font-size: 50px;   
    font-weight: bold;
    text-align: center;
    opacity: 0;
    animation: fadeIn 2s ease-in forwards;
    animation-delay: 0s;
    position: relative;
}  

#redacted-title::after {
    content: 'A Look At Censorship in Modern America';
    font-family: 'Courier New', Courier, monospace;
    font-size: 20px;
    color: #FFFFFF;
    position: absolute;
    top: 40%;
    left: 10%;
    width: 80%;
    height: 30px;
    background: black;
    transform: scaleX(0);
    transform-origin: left;
    animation: strikeThrough 1s forwards;
    animation-delay: 3s;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes strikeThrough {
    to { transform: scaleX(1); }
}
           
.typewriter-1, .typewriter-2 , .typewriter-3 , .typewriter-4 {
    font-family: 'Courier New', Courier, monospace;
    overflow: hidden;
    white-space: nowrap;
    margin: 20px auto;
    text-align: center;
    letter-spacing: 0.08em;
    font-size: 18px;
    width: 0;
    border-right: 0.15em solid black; 
}

.typewriter-1 {
    animation:
        typing 4s steps(50, end) 0s forwards,
        caret-disappear 0.1s forwards 0.1s;
}

.typewriter-2 {
    animation:
        typing 4s steps(70, end) 2s forwards,
        caret-disappear 0.1s forwards 0s;
}
            
.typewriter-3 {
    animation:
        typing 4s steps(70, end) 4s forwards,
        caret-disappear 0.1s forwards 0s;
}
            
.typewriter-4 {
    animation:
        typing 4s steps(70, end) 6s forwards,
        caret-disappear 0.1s forwards 0s;
}

/* Typing animations */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

@keyframes caret-disappear {
    from { border-right: 0.15em solid black; }
    to { border-right: none; }
} 

/* When sidebar is expanded */
[data-testid="stSidebar"][aria-expanded="true"] {
    width: 310px !important;
    min-width: 310px !important;
    max-width: 310px !important;
    padding-right: 10px;
    background-color: #F8F7F2;
}

/* When sidebar is collapsed */
[data-testid="stSidebar"][aria-expanded="false"] {
    position: absolute !important; /* Take it out of the flow */
    left: -310px !important; /* Move completely off-screen */
    width: 310px !important;
}

/* Main content when sidebar is expanded */
[data-testid="stSidebar"][aria-expanded="true"] ~ section[data-testid="stMain"] {
    margin-left: 10px !important;
    width: calc(100% - 10px) !important;
}

/* Main content when sidebar is collapsed */
[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stMain"] {
    width: 100% !important;
    margin-left: 0 !important;
}

/* Center the main content container when sidebar is collapsed */
[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stMain"] .block-container {
    max-width: 1200px !important;
    padding-left: 5rem !important;
    padding-right: 5rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Ensure transition is smooth */
section[data-testid="stMain"], [data-testid="stSidebar"] {
    transition: all 0.3s ease-in-out;
}         
                    
/* Remove highlight on selected radio item */
[data-testid="stSidebar"] .css-1cpxqw2, /* wrapper for radio items */
[data-testid="stSidebar"] .css-16idsys {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.sidebar-toggle {
    font-weight: bold;
    cursor: pointer;
    padding: 10px;
    color: #333;
}
         
h1, h2, h3, .stMarkdown > div {
    animation: fadeIn 1s ease-in;
}

</style>
""", unsafe_allow_html=True)

# Define section names
anchor_ids = ["Introduction", "Book Bans", "Defunding Research", "Climate Censorship"]
anchor_icons = ["info-circle", "book-fill", "clipboard2-data-fill", "cloud-sun-fill"]

# Create the navigation bar
with st.sidebar:
    st.subheader("Navigation")
    scroll_navbar(
        anchor_ids,
        anchor_labels = None,
        anchor_icons = anchor_icons,
        auto_update_anchor=True,
        override_styles={
            "navbarButtonBase": {
                "backgroundColor": "#F8F7F2",
                "color": "#333333",
                "border": "1px solid #dddddd",
                "borderRadius": "4px",
                "marginBottom": "5px",
                "transition": "all 0.3s ease"
            },
            "navbarButtonActive": {
                "backgroundColor": "#000000",
                "color": "#ffffff",
                "borderColor": "#000000",
                "fontWeight": "bold"
            },
            "navbarButtonHover": {
                "backgroundColor": "#e6e6e6",
                "borderColor": "#cccccc"
            },
            "navigationBarBase": {
                "backgroundColor": "#F8F7F2"
            }
        }
    )

# Introduction
st.subheader("", anchor = "Introduction")
st.markdown('<div id="redacted-title">REDACTED</div>', unsafe_allow_html=True)
st.markdown('<div id="byline">by <a href="https://github.com/ilovedogs3003" target="_blank" style="color: inherit; text-decoration: underline;">Jefrey Alexander</a>, <a href="https://github.com/janavikumar" target="_blank" style="color: inherit; text-decoration: underline;">Janavi Kumar</a>, and <a href="https://github.com/Peter-Silverstein" target="_blank" style="color: inherit; text-decoration: underline;">Peter Silverstein</a></div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-1"><br>This project explores patterns and potential ramifications </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-2">of information removal in recent years in the United States, </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-3">from book bans to defunding academic research </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-4">to the alteration of government websites.</div>', unsafe_allow_html=True)

# Book Bans
st.subheader("", anchor = "Book Bans")
st.markdown('<div id="section-title">Book Bans</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="fade-container">', unsafe_allow_html=True)
    import bookbans
    bookbans.run_bookbans()
    st.markdown('</div>', unsafe_allow_html=True)

# Defunding Research
st.subheader("", anchor = "Defunding Research")
st.markdown('<div id="section-title">Defunding Research</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="fade-container">', unsafe_allow_html=True)
    import research_papers
    research_papers.run()
    st.markdown('</div>', unsafe_allow_html=True)

# Climate Censorship
st.subheader("", anchor = "Climate Censorship")
st.markdown('<div id="section-title">Climate Censorship on Government Websites</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="fade-container">', unsafe_allow_html=True)
    import fedtracker_st
    fedtracker_st.run_fedtracker()
    st.markdown('</div>', unsafe_allow_html=True)


# with st.sidebar.expander("Navigate"):
#     menu = st.radio(
#         "",
#         ["Home", "Book Bans", "Defunding Research", "Climate Censorship"]
#     )

# # project description
# if menu == "Home":
#     st.markdown('<div id="redacted-title">REDACTED</div>', unsafe_allow_html=True)
#     st.markdown('<div id="byline">by <a href="https://github.com/ilovedogs3003" target="_blank" style="color: inherit; text-decoration: underline;">Jefrey Alexander</a>, <a href="https://github.com/janavikumar" target="_blank" style="color: inherit; text-decoration: underline;">Janavi Kumar</a>, and <a href="https://github.com/Peter-Silverstein" target="_blank" style="color: inherit; text-decoration: underline;">Peter Silverstein</a></div>', unsafe_allow_html=True)
#     st.markdown('<div class="typewriter-1"><br>This project explores patterns and potential ramifications </div>', unsafe_allow_html=True)
#     st.markdown('<div class="typewriter-2">of information removal in recent years in the United States, </div>', unsafe_allow_html=True)
#     st.markdown('<div class="typewriter-3">from book bans to defunding academic research </div>', unsafe_allow_html=True)
#     st.markdown('<div class="typewriter-4">to the alteration of government websites.</div>', unsafe_allow_html=True)

# elif menu == "Book Bans":
#     st.markdown('<div id="section-title">Book Bans</div>', unsafe_allow_html=True)
#     with st.container():
#         st.markdown('<div class="fade-container">', unsafe_allow_html=True)
#         import bookbans
#         bookbans.run_bookbans()
#         st.markdown('</div>', unsafe_allow_html=True)

# elif menu == "Defunding Research":
#     st.markdown('<div id="section-title">Defunding Research</div>', unsafe_allow_html=True)
#     with st.container():
#         st.markdown('<div class="fade-container">', unsafe_allow_html=True)
#         import research_papers
#         research_papers.run()
#         st.markdown('</div>', unsafe_allow_html=True)

# elif menu == "Climate Censorship":
#     st.markdown('<div id="section-title">Climate Censorship on Government Websites</div>', unsafe_allow_html=True)
#     with st.container():
#         st.markdown('<div class="fade-container">', unsafe_allow_html=True)
#         import fedtracker_st
#         fedtracker_st.run_fedtracker()
#         st.markdown('</div>', unsafe_allow_html=True)