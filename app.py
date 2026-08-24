import streamlit as st
import base64
from openai import OpenAI
from navigation import render_sidebar

render_sidebar()

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# 3. Initialize OpenAI / Featherless Client for facts
featherless_client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=st.secrets["FEATHERLESS_API_KEY"]
)

def asl_fact():
    try:
        fact = featherless_client.chat.completions.create(
            model="Magistral-Small-2507-Rebased-Vision",
            messages=[{"role": "user", "content": "Tell me one short, inspiring, or interesting random fact about ASL or the Deaf community. Keep it under 30 words."}],
            max_tokens=60
        )
        return fact.choices[0].message.content.strip()
    except Exception:
        return "There are over 300 different sign languages used around the world! ASL is just one of them!"

st.title("Let's Learn ASL!")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🤟 Practice Lab", use_container_width=True):
        st.switch_page("pages/practice_lab.py")

with col2:
    if st.button("🤖 Beat the Robot", use_container_width=True):
        st.switch_page("pages/quiz.py")

with col3:
    if st.button("✍️ Sentence Maker", use_container_width=True):
        st.switch_page("pages/sentence_maker.py")

st.divider()
st.subheader("🌍 UN Sustainable Development Goals")
st.write("Hover over the cards to see how this app contributes!")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <img src="https://raw.githubusercontent.com/EmilyXu45/asl-learning-app/d0a068fa355aa14763dec78c45a7fb79d3a25d7a/images/sdg4.png" style="width:100%; height:auto;">
            </div>
            <div class="flip-card-back">
              <p><b>Making sign language learning accessible to everyone through AI-powered interactive tools.</b></p>
            </div>
          </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
             <img src="https://raw.githubusercontent.com/EmilyXu45/asl-learning-app/d0a068fa355aa14763dec78c45a7fb79d3a25d7a/images/sdg10.png" style="width:100%; height:auto;">
            </div>
            <div class="flip-card-back">
              <p><b>Breaking communication barriers to ensure deaf and hard-of-hearing individuals have equal opportunities.</b></p>
            </div>
          </div>
        </div>
    """, unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("💡 Did you know?")
    if st.button("Generate New Fact"):
        st.session_state.asl_fact = asl_fact()
        
    if 'asl_fact' not in st.session_state:
        st.session_state.asl_fact = asl_fact()
    st.write(st.session_state.asl_fact)