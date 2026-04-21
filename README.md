# 🪐 ZENITH OS | THE PRODUCTIVITY ENGINE

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://zenith-os.streamlit.app/)
[![Supabase Powered](https://img.shields.io/badge/Backend-Supabase-3ECF8E?style=flat&logo=supabase)](https://supabase.com)
[![Python Version](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Zenith OS** is a high-performance, visually stunning workspace designed for those who demand more from their productivity tools. It's not just a task manager; it's a sleek, glassmorphic operating environment built on Python, Streamlit, and Supabase.

---

## ✨ Premium Features

### 🌌 Elite UI/UX
Experience productivity with a focus on aesthetics. Switch between three curated visual modes:
- **Midnight**: A deep, radial-gradient dark mode for focused night sessions.
- **Cyberpunk**: Neon-infused high-energy workspace.
- **Elysium**: A clean, airy light mode for high-clarity daylight work.

### ⚡ Hybrid Architecture
- **Supabase Core**: Real-time data persistence and secure user authentication.
- **Offline-First Sync**: Built-in resilience with a queue-based synchronization engine that handles network fluctuations without breaking your flow.

### 🧭 Advanced Execution
- **Universal Workspace**: A seamless Kanban interface to track tasks from Backlog to Settled.
- **Deep Work Timer**: Integrated Pomodoro-style timer to maximize focus windows.
- **Energy Trends**: Real-time Plotly analytics visualizing your productivity distribution.

### 🤝 Global Collaboration
- **Global Relay**: Instant team-wide chat for rapid coordination.
- **Workspace Context**: Task-specific discussion threads and activity logs to keep everything in its place.

---

## 🛠️ Stack Components

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python-driven) |
| **Styling** | Custom Vanilla CSS (Glassmorphism) |
| **Backend** | Supabase (PostgreSQL + Auth) |
| **Analytics** | Plotly & Pandas |
| **Icons** | Emojis & Custom CSS Markers |

---

## 🚀 Getting Started

### 1. Clone the Frontier
```bash
git clone https://github.com/Fridayhere/zenith.git
cd zenith
```

### 2. Prepare the Environment
```bash
pip install -r requirements.txt
```

### 3. Connect the Core
Create a `.streamlit/secrets.toml` file with your Supabase credentials:
```toml
[supabase]
URL = "your-project-url"
KEY = "your-anon-key"
```

### 4. Launch the OS
```bash
streamlit run app.py
```

---

## 🎮 Gamification & Progress
Earn **XP Points** as you complete tasks. Monitor your rank and watch your "Settle" column grow as you conquer your backlog. Zenith OS turns the grind into a quest.

---

<div align="center">
  <p>Built with ❤️ by the Zenith Team</p>
  <p><i>"The peak of productivity is just a click away."</i></p>
</div>
