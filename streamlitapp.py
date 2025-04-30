import streamlit as st
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
    font-size: 100px;
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
           
.typewriter-1, .typewriter-2 , .typewriter-3 {
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

/* Typing animations */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

@keyframes caret-disappear {
    from { border-right: 0.15em solid black; }
    to { border-right: none; }
} 


[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    width: 300px;
}

// don't want the menu to show initially
section[data-testid="stSidebar"] > div:first-child {
    display: none;
}

.sidebar-toggle {
    font-weight: bold;
    cursor: pointer;
    padding: 10px;
    color: #333;
}

# Sidebar toggle
st.sidebar.markdown("### › Menu")
menu = st.sidebar.radio("",
    ["Co-occurrence Network", "Redacted Word Cloud", "Sunburst Themes"],
    label_visibility="collapsed"
)
            
h1, h2, h3, .stMarkdown > div {
    animation: fadeIn 1s ease-in;
}

</style>
""", unsafe_allow_html=True)

# project description
st.markdown('<div id="redacted-title">REDACTED</div>', unsafe_allow_html=True)
st.markdown('<div id="byline">by Jefrey Alexander, Janavi Kumar, and Peter Silverstein</div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-1">This project explores patterns and potential ramifications </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-2">of information removal in recent years in the United States, </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-3">from books bans to defunding research to the alterration of government websites. </div>', unsafe_allow_html=True)

#load empty sections first visually
#section1 = st.empty() 
section2 = st.empty()
section3 = st.empty()

time.sleep(6)
st.markdown('<div id="section-title">Book Bans</div>', unsafe_allow_html=True)
st.markdown('<div id="section-title">Defunding Research</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="fade-container">', unsafe_allow_html=True)
    import research_papers
    research_papers.run()
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(2)
st.markdown('<div id="section-title">Removing & Alterring Websites</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="fade-container">', unsafe_allow_html=True)
    import fedtracker_st
    fedtracker_st.run_fedtracker()
    st.markdown('</div>', unsafe_allow_html=True)
