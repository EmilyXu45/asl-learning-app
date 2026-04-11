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

if 'current_letter' not in st.session_state:
    st.session_state.current_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    others = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != st.session_state.current_letter]
    options = random.sample(others, 3) + [st.session_state.current_letter]
    random.shuffle(options)
    st.session_state.options = options
    # We use session_state for 'answered' so it survives the rerun
    st.session_state.answered = False

# 2. Layout: Duo Screen
col_user, col_robot = st.columns(2)

with col_user:
    st.header("👤 Your Choice")
    # Picks random image from folder
    st.image(f"asl_images/{st.session_state.current_letter}.png", width="stretch")
    st.write(f"### What letter is shown above?")
    
    for opt in st.session_state.options:
            # We disable buttons once you've answered
        if st.button(f"Letter {opt}", key=f"btn_{opt}", width="stretch", disabled=st.session_state.answered):
            st.session_state.last_user_choice = opt
            st.session_state.answered = True
            st.rerun() # Forces a rerun to move to the Robot's turn

with col_robot:
    st.header("🤖 Robot's Choice")
    if not st.session_state.answered:
        st.info("Waiting for your move...")
    else:
        # We check if the robot has already picked for THIS round
        if 'robot_choice' not in st.session_state:
            with st.spinner("Robot is thinking..."):
                time.sleep(0.8)
                if random.random() < 0.50:
                    st.session_state.robot_choice = st.session_state.current_letter
                else:
                    st.session_state.robot_choice = random.choice([o for o in st.session_state.options if o != st.session_state.current_letter])
        
        st.write(f"### Robot chose: {st.session_state.robot_choice}")

# 3. Handle Results (Only shows if answered is True)
if st.session_state.answered:
    correct = st.session_state.current_letter
    
    if st.session_state.last_user_choice == correct:
        # We only want to add the point once!
        if 'score_updated' not in st.session_state:
            st.session_state.user_score += 1
        st.success(f"🎯 Correct! It was {correct}.")
    else:
        st.error(f"❌ Wrong! It was {correct}.")

    if st.session_state.get('robot_choice') == correct:
        if 'score_updated' not in st.session_state:
            st.session_state.robot_score += 1
        st.warning("🤖 The Robot also got it right!")
    
    # Mark that we've updated scores for this round
    st.session_state.score_updated = True

    # THE RESET BUTTON
    if st.button("Next Round ➡️", width="stretch"):
        # CLEAN THE LOCKER: Remove round-specific data
        keys_to_delete = ['current_letter', 'robot_choice', 'score_updated', 'options']
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.answered = False
        st.rerun() # Now when it reruns, 'current_letter' is missing, so it picks a new one!

# 4. Scoreboard
st.divider()
s1, s2 = st.columns(2)
s1.metric("YOUR SCORE", st.session_state.user_score)
s2.metric("ROBOT SCORE", st.session_state.robot_score)