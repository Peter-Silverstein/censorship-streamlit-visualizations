import streamlit as st
import research_papers
import fedtracker_st

# set up page
st.set_page_config(page_title="REDACTED", layout="wide")

#styling & html for title & typing things
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Playfair+Display:wght@700&display=swap');

//get this to work lowkey
html, body, [class*="css"] {
    background-color: #ffffff;
    color: #000000;
    font-family: 'Merriweather', 'Playfair Display', Georgia, serif;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
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

.plain-text {
    font-family: 'Courier New', Courier, monospace;
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
    to { opacity: 1; }
}

@keyframes strikeThrough {
    to { transform: scaleX(1); }
}
            
.plain-text {
    font-family: 'Courier New', Courier, monospace;
}

.typewriter-1, .typewriter-2 , .typewriter-3 {
    font-family: 'Courier New', Courier, monospace;
    overflow: hidden;
    white-space: nowrap;
    margin: 20px auto;
    text-align: center;
    letter-spacing: 0.08em;
    font-size: 16px;
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
        typing 4s steps(70, end) 3.75s forwards,
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
</style>
""", unsafe_allow_html=True)
st.markdown('<div id="redacted-title">REDACTED</div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-1">This project explores patterns and potential ramifications </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-2">of information removal in recent years in the United States, </div>', unsafe_allow_html=True)
st.markdown('<div class="typewriter-3">from books bans to flagged research to the alterration of government websites. </div>', unsafe_allow_html=True)

research_papers.run()
fedtracker_st.run_fedtracker()