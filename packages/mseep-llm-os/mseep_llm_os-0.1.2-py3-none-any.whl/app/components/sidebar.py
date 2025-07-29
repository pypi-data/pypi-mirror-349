"""Sidebar component module"""

import streamlit as st
from phi.tools.streamlit.components import get_username_sidebar
from app.components.tools import render_tools_tab
from app.components.knowledge_base import render_knowledge_base_tab
from app.components.history import render_history_tab

def setup_sidebar():
    """Setup sidebar"""
    # Get username
    user_id = get_username_sidebar()
    
    if not user_id:
        return None
    
    # Display user information
    st.sidebar.markdown(f"### 👤 User: {user_id}")
    st.sidebar.markdown("---")
    
    # Tools and settings
    st.sidebar.markdown("### ⚙️ Tools and settings")
    
    # Create tabs
    tool_tab, kb_tab, history_tab = st.sidebar.tabs(["🛠️ Tools", "📚 Knowledge base", "🕒 History"])
    
    # Render each tab content
    with tool_tab:
        render_tools_tab()
    
    with kb_tab:
        render_knowledge_base_tab()
    
    with history_tab:
        render_history_tab(user_id)
    
    return user_id 