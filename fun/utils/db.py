import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["supabase"]["URL"]
    key = st.secrets["supabase"]["KEY"]
    return create_client(url, key)

def get_todos(supabase: Client, user_id: str):
    response = supabase.table("todos").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return response.data

def insert_todo(supabase: Client, user_id: str, title: str, description: str, category: str, priority: str, due_date: str):
    data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "status": "Pending"
    }
    # remove None values and replace with empty string
    data = {k: v for k, v in data.items() if v is not None}
    supabase.table("todos").insert(data).execute()

def update_todo_status(supabase: Client, todo_id: str, status: str):
    supabase.table("todos").update({"status": status}).eq("id", todo_id).execute()

def delete_todo(supabase: Client, todo_id: str):
    supabase.table("todos").delete().eq("id", todo_id).execute()

# --- Chat / Collaboration Logic ---

def get_messages(supabase: Client, limit: int = 20):
    response = supabase.table("messages").select("*").order("created_at", desc=True).limit(limit).execute()
    # Reverse to show in chronological order
    return sorted(response.data, key=lambda x: x['created_at'])

def send_message(supabase: Client, user_id: str, email: str, content: str):
    data = {"user_id": user_id, "user_email": email, "content": content}
    try:
        supabase.table("messages").insert(data).execute()
    except Exception as e:
        print(f"Failed to send message: {e}")

# --- Advanced Detail Handlers ---

def log_activity(supabase: Client, todo_id: str, user_id: str, action: str):
    try:
        supabase.table("activity_log").insert({"todo_id": todo_id, "user_id": user_id, "action": action}).execute()
    except Exception as e:
        print(f"Logging failed: {e}") # Log to console instead of crashing

def get_activity(supabase: Client, todo_id: str):
    return supabase.table("activity_log").select("*").eq("todo_id", todo_id).order("created_at", desc=True).execute().data

def add_comment(supabase: Client, todo_id: str, user_id: str, email: str, content: str):
    try:
        supabase.table("comments").insert({"todo_id": todo_id, "user_id": user_id, "user_email": email, "content": content}).execute()
    except Exception as e:
        print(f"Failed to add comment: {e}")

def get_comments(supabase: Client, todo_id: str):
    return supabase.table("comments").select("*").eq("todo_id", todo_id).order("created_at", desc=True).execute().data
