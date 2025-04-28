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
    content: '';
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

.typewriter {
    font-family: 'Courier New', Courier, monospace;
    overflow: hidden;
    border-right: 0.15em solid black;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    margin: 20px auto;
    letter-spacing: 0.08em;
    animation: typing 3s steps(40, end), blink-caret 0.8s step-end infinite;
    font-size: 24px;
    width: 400ch; /* width in characters */
}

@keyframes typing {
    from { width: 0 }
    to { width: 400ch }
}

@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: black; }
}
</style>
""", unsafe_allow_html=True)

research_papers.run()