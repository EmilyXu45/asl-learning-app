import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=st.secrets["FEATHERLESS_API_KEY"]
)

models = client.models.list()
for model in models.data:
    if "vision" in model.id.lower():
        print(model.id)