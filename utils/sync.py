import json
import os
import streamlit as st
from supabase import Client

QUEUE_FILE = ".sync_queue.json"

def get_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f)

def add_to_sync_queue(action_type, data):
    queue = get_queue()
    queue.append({"action": action_type, "data": data})
    save_queue(queue)
    st.toast("⚠️ Offline: Task saved locally. Will sync when online.", icon="💾")

def sync_offline_data(supabase: Client):
    queue = get_queue()
    if not queue:
        return True
    
    remaining_queue = []
    success_count = 0
    
    for item in queue:
        try:
            if item["action"] == "insert":
                supabase.table("todos").insert(item["data"]).execute()
            elif item["action"] == "update_status":
                supabase.table("todos").update({"status": item["data"]["status"]}).eq("id", item["data"]["id"]).execute()
            elif item["action"] == "delete":
                supabase.table("todos").delete().eq("id", item["data"]["id"]).execute()
            success_count += 1
        except Exception:
            remaining_queue.append(item)
    
    save_queue(remaining_queue)
    if success_count > 0:
        st.toast(f"✅ Synced {success_count} offline actions to cloud!", icon="☁️")
    return len(remaining_queue) == 0

def is_online(supabase: Client):
    try:
        supabase.table("todos").select("count", count="exact").limit(1).execute()
        return True
    except:
        return False
