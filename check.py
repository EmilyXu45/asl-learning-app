from google import genai
import streamlit as st

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
