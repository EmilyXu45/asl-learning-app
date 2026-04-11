import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url="https://api.featherless.ai/v1", 
    api_key="rc_1251eccde58b548cb0095bc3e93896ff93cc81427f0ad9d6b9733927b93632be" 
)

st.title("✍️ ASL Sentence Maker")

if st.button("⬅️ Home"):
    st.session_state.page = "home"
    st.switch_page("app.py")

if 'draft_letters' not in st.session_state:
    st.session_state.draft_letters = []


col_main, col_keys = st.columns([2, 1])

with col_keys:
    st.write("### ⌨️ ASL Keyboard")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " 
    # Create a 4-column grid for buttons
    k_cols = st.columns(4)
    for i, char in enumerate(alphabet):
        label = "Space" if char == " " else char
        if k_cols[i % 4].button(label, key=f"k_{char}", width="stretch"):
            st.session_state.draft_letters.append(char)
            st.rerun()

with col_main:
    st.write("### Your Draft")
    current_text = "".join(st.session_state.draft_letters)
    
    st.info(f"👉 **{current_text}**" if current_text else "Click letters to start...")
    
    if st.button("Clear All 🗑️", width="stretch"):
        st.session_state.draft_letters = []
        st.rerun()

    st.divider()


    if st.button("🪄 Fix with AI", type="primary", width="stretch"):
        if not current_text:
            st.warning("Type some letters first!")
        else:
            with st.spinner("Featherless is processing..."):
                try:
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.1-8B-Instruct", 
                        messages=[
                            {"role": "system", "content": "You are an ASL interpreter. The user will provide a string of letters. Turn them into a grammatically correct English sentence. Fix typos and add punctuation. Return ONLY the sentence."},
                            {"role": "user", "content": f"The letters are: {current_text}"}
                        ]
                    )
                    
                    ai_sentence = response.choices[0].message.content
                    st.success(f"**AI Translation:** {ai_sentence}")
                except Exception as e:
                    st.error(f"AI Error: {e}")
                