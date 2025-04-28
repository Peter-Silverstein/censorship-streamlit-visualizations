import streamlit as st
import research_papers

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

#redacted-title::after {
    content: 'A Look At Censorship in Modern America';
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

.typewriter-1, .typewriter-2 {
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
        typing1 4s steps(50, end) 0s forwards,
        caret-disappear 0.1s forwards 0.1s;
}

.typewriter-2 {
    animation:
        typing2 4s steps(70, end) 3s forwards,
        caret-disappear 0.1s forwards 0s;
}

/* Typing animations */
@keyframes typing1 {
    from { width: 0 }
    to { width: 100% }
}

@keyframes typing2 {
    from { width: 0 }
    to { width: 100% }
}

@keyframes caret-disappear {
    from { border-right: 0.15em solid black; }
    to { border-right: none; }
} 
</style>
""", unsafe_allow_html=True)

research_papers.run()