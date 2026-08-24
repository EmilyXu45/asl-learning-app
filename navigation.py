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
            st.switch_page("pages/practice_lab.py")
        if st.button("Beat the Robot Game", use_container_width=True):
            st.switch_page("pages/quiz.py")
            
        if st.button("Sentence Maker", use_container_width=True):
            st.switch_page("pages/sentence_maker.py")
            

        st.divider()

        # Dynamic Daily Goal Section
        st.subheader("🎯 Daily Goal")
        
        # Initialize score counter if it doesn't exist
        if 'letters_practiced' not in st.session_state:
            st.session_state.letters_practiced = 0
            
        goal = 5
        count = st.session_state.letters_practiced
        
        # Progress value must be between 0.0 and 1.0
        progress_val = min(count / goal, 1.0)
        
        st.progress(progress_val, text=f"{count}/{goal} Letters Practiced")
        
        if count >= goal:
            st.success("🎉 Daily goal reached! Great job!")
        
        st.info("💡 **Tip:** Practice in a brightly lit room for better AI vision accuracy!")