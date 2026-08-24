import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🤟 ASL Learning App")
        st.divider()

        # Navigation Header
        st.subheader("Menu")
        
        # Navigation Buttons
        if st.button("Home", use_container_width=True):
            st.switch_page("app.py")
        if st.button("Practice Lab", use_container_width=True):
            st.session_state.page = "app"
            st.rerun()
        if st.button("Beat the Robot Game", use_container_width=True):
            st.switch_page("pages/quiz.py")
            
        if st.button("Sentence Maker", use_container_width=True):
            st.switch_page("pages/sentence_maker.py")
            

        st.divider()

        # Extra UI Widget (Progress or Quick Info)
        st.subheader("🎯 Daily Goal")
        st.progress(0.6, text="3/5 Letters Practiced")
        
        st.info("💡 **Tip:** Practice in a brightly lit room for better AI vision accuracy!")