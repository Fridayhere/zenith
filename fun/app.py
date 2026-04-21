import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
import time
from datetime import datetime, date
from utils.auth import login_user, signup_user, check_session, logout_user
from utils.db import (init_connection, get_todos, insert_todo, update_todo_status, delete_todo, 
                      get_messages, send_message, log_activity, get_activity, add_comment, get_comments)
from utils.sync import sync_offline_data, add_to_sync_queue, is_online

# --- Zenith OS Engine ---
st.set_page_config(page_title="Zenith OS | Ultimate", page_icon="🪐", layout="wide")

if "view" not in st.session_state: st.session_state.view = "dashboard"
if "selected_task" not in st.session_state: st.session_state.selected_task = None
if "theme" not in st.session_state: st.session_state.theme = "Midnight"
if "points" not in st.session_state: st.session_state.points = 0

def apply_themes():
    themes = {
        "Midnight": {"bg": "radial-gradient(circle at top right, #1a1c2c, #0d0d12)", "accent": "#8b5cf6", "card": "rgba(255,255,255,0.02)"},
        "Cyberpunk": {"bg": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)", "accent": "#00f2ff", "card": "rgba(0,242,255,0.05)"},
        "Elysium": {"bg": "#f8fafc", "accent": "#6366f1", "card": "rgba(255,255,255,0.8)"}
    }
    t = themes[st.session_state.theme]
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        * {{ font-family: 'Outfit', sans-serif; }}
        .stApp {{ background: {t['bg']}; color: {'#1e293b' if st.session_state.theme == 'Elysium' else '#f8fafc'}; }}
        .premium-card {{ background: {t['card']}; border: 1px solid {t['accent']}33; border-radius: 20px; padding: 25px; backdrop-filter: blur(20px); transition: 0.3s; cursor: pointer; }}
        .premium-card:hover {{ border-color: {t['accent']}; transform: scale(1.02); }}
        .accent-text {{ color: {t['accent']}; font-weight: 700; }}
        .stButton button {{ border-radius: 12px; background: {t['accent']}; color: white; border: none; }}
        </style>
    """, unsafe_allow_html=True)

def render_todo_card_mini(t, supabase):
    status_icon = "⏳" if t['status'] == 'Pending' else ("⚡" if t['status'] == 'In Progress' else "✅")
    st.markdown(f"""
        <div class="premium-card" onclick="window.location.reload();">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 0.8rem; opacity: 0.6;">{t['category']}</span>
                <span>{status_icon}</span>
            </div>
            <h4 style="margin: 10px 0;">{t['title']}</h4>
            <div style="font-size: 0.8rem; opacity: 0.5;">Priority: {t['priority']}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Workspace", key=f"view_{t['id']}", use_container_width=True):
        st.session_state.selected_task = t
        st.session_state.view = "detail"
        st.rerun()

def task_detail_view(user):
    supabase = init_connection()
    t = st.session_state.selected_task
    
    # Navigation
    if st.button("← Back to Workspace"):
        st.session_state.view = "dashboard"
        st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<h1>{t['title']}</h1>", unsafe_allow_html=True)
        st.caption(f"Category: {t['category']} | Created: {t['created_at'][:10]}")
        
        tab_a, tab_b, tab_c = st.tabs(["🚀 Execution", "📜 History", "💬 Discussion"])
        
        with tab_a:
            st.markdown(f"### Objective\n{t.get('description', 'No details provided.')}")
            
            # Feature: Pomodoro Timer
            st.divider()
            st.markdown("### ⏲️ Deep Work Timer")
            timer_col1, timer_col2 = st.columns([2, 1])
            with timer_col1:
                minutes = st.number_input("Set Focus Minutes", value=25, min_value=1)
                if st.button("Start Focus Session", use_container_width=True):
                    with st.empty():
                        for remaining in range(minutes * 60, 0, -1):
                            mins, secs = divmod(remaining, 60)
                            st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
                            time.sleep(1)
                        st.balloons()
            
            with timer_col2:
                st.info("Studies show focusing for 25 mins increases efficiency by 40%.")

        with tab_b:
            st.markdown("### Activity Timeline")
            history = get_activity(supabase, t['id'])
            for h in history:
                st.write(f"🔹 {h['created_at'][:19]} - **{h['action']}**")

        with tab_c:
            st.markdown("### Task Comments")
            coms = get_comments(supabase, t['id'])
            for c in coms:
                st.chat_message("user").write(f"**{c['user_email']}**: {c['content']}")
            
            with st.form("add_com", clear_on_submit=True):
                new_c = st.text_input("Add insight...")
                if st.form_submit_button("Post"):
                    add_comment(supabase, t['id'], user.id, user.email, new_c)
                    st.rerun()

    with col2:
        st.markdown("### Workspace Metadata")
        st.markdown(f"""
            <div class="premium-card">
                <p>Status: <span class="accent-text">{t['status']}</span></p>
                <p>Urgency: <span class="accent-text">{t['priority']}</span></p>
                <p>Assigned To: {user.email}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if t['status'] != 'Completed':
            if st.button("Mark as Finalized", use_container_width=True):
                update_todo_status(supabase, t['id'], 'Completed')
                log_activity(supabase, t['id'], user.id, "Marked as Completed")
                st.session_state.points += 100
                st.balloons()
                st.session_state.view = "dashboard"
                st.rerun()

def dashboard_view(user):
    supabase = init_connection()
    online = is_online(supabase)
    
    # --- Sidebar ---
    with st.sidebar:
        st.markdown(f"# 🪐 Zenith OS")
        st.markdown(f"**Points: {st.session_state.points} XP**")
        st.divider()
        st.session_state.theme = st.selectbox("System Theme", ["Midnight", "Cyberpunk", "Elysium"])
        
        st.divider()
        with st.expander("➕ New Deployment"):
            with st.form("new"):
                title = st.text_input("Title")
                cat = st.text_input("Dept / Category")
                prio = st.select_slider("Urgency", options=["Low", "Medium", "High"])
                if st.form_submit_button("Launch"):
                    insert_todo(supabase, user.id, title, "New task", cat, prio, str(date.today()))
                    st.rerun()
        
        st.divider()
        # Feature: Global Team Chat
        st.markdown("🗣️ **Global Relay**")
        msgs = get_messages(supabase)
        for m in msgs[-5:]: st.caption(f"{m['user_email'][:5]}...: {m['content']}")
        
        if st.button("Logout", use_container_width=True): logout_user()

    # --- Analytics & Content ---
    t_all = get_todos(supabase, user.id)
    
    st.markdown("<h1>Universal Workspace</h1>", unsafe_allow_html=True)
    
    # Feature: Activity Heatmap
    if t_all:
        st.markdown("### Energy Trends")
        df = pd.DataFrame(t_all)
        fig = px.bar(df, x='category', color='priority', barmode='group', height=200)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📌 Backlog")
        for t in [x for x in t_all if x['status'] == 'Pending']: render_todo_card_mini(t, supabase)
    with col2:
        st.markdown("### ⚡ Active")
        for t in [x for x in t_all if x['status'] == 'In Progress']: render_todo_card_mini(t, supabase)
    with col3:
        st.markdown("### ✅ Settled")
        for t in [x for x in t_all if x['status'] == 'Completed']: render_todo_card_mini(t, supabase)

def main():
    user = check_session()
    apply_themes()
    if user is None:
        login_ui()
    else:
        if st.session_state.view == "dashboard":
            dashboard_view(user)
        else:
            task_detail_view(user)

def login_ui():
    st.markdown("<h1 style='text-align: center; margin-top: 5vh;'>ZENITH <span style='color:#8b5cf6'>OS</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.6;'>Enter your secure passkey to initiate workspace</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1.2,1])
    with c2:
        tab1, tab2 = st.tabs(["🔑 Login", "✨ Register"])
        with tab1:
            email = st.text_input("User ID", key="l_email")
            pwd = st.text_input("Passkey", type="password", key="l_pwd")
            if st.button("Access Dashboard", use_container_width=True):
                login_user(email, pwd)
        with tab2:
            n_email = st.text_input("New ID", key="s_email")
            n_pwd = st.text_input("New Passkey", type="password", key="s_pwd")
            if st.button("Create Account", use_container_width=True):
                signup_user(n_email, n_pwd)

if __name__ == "__main__":
    main()
