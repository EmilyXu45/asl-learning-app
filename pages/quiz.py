import streamlit as st
import random
import time

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("⬅️ Home", use_container_width=True):
        st.switch_page("app.py")

st.title("🤖 Beat the Robot: ASL Quiz")

# 1. Initialize Game State (Scores & Current Question)
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
    st.session_state.robot_score = 0
    st.session_state.current_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # Generate 4 options (1 correct, 3 random)
    others = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != st.session_state.current_letter]
    options = random.sample(others, 3) + [st.session_state.current_letter]
    random.shuffle(options)
    st.session_state.options = options

# 2. Layout: Duo Screen
col_user, col_robot = st.columns(2)

with col_user:
    st.header("👤 Your Choice")
    st.image(f"asl_images/{st.session_state.current_letter}.png", use_container_width=True)
    st.write(f"### What letter is shown above?")
    
    # Give user the options to choose their answer
    user_answered = False
    for opt in st.session_state.options:
        if st.button(f"Letter {opt}", key=f"btn_{opt}", use_container_width=True):
            st.session_state.last_user_choice = opt
            user_answered = True

with col_robot:
    st.header("🤖 Robot's Choice")
    robot_placeholder = st.empty()
    if not user_answered:
        robot_placeholder.info("Waiting for your move...")

# Need to correct this part...
if user_answered:
    # Robot "thinks" for a second
    with st.spinner("Robot is thinking..."):
        time.sleep(0.8)
        if random.random() < 0.85:
            robot_choice = st.session_state.current_letter
        else:
            robot_choice = random.choice([o for o in st.session_state.options if o != st.session_state.current_letter])
    
    # Show Robot's choice
    col_robot.write(f"### Robot chose: {robot_choice}")
    
    # Comparison
    correct = st.session_state.current_letter
    if st.session_state.last_user_choice == correct:
        st.session_state.user_score += 1
        st.success("🎯 Correct! You get a point.")
    else:
        st.error(f"❌ Wrong! The correct answer was {correct}.")

    if robot_choice == correct:
        st.session_state.robot_score += 1
        st.warning("🤖 The Robot also got it right!")

    if st.button("Next Round ➡️"):
        if 'current_letter' in st.session_state:
            del st.session_state.current_letter
        st.rerun()

# 4. Scoreboard
st.divider()
s1, s2 = st.columns(2)
s1.metric("YOUR SCORE", st.session_state.user_score)
s2.metric("ROBOT SCORE", st.session_state.robot_score)