"""Tools component module"""

import streamlit as st
from app.utils.session import restart_assistant

def render_tools_tab():
    """Render tools tab"""
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("#### Select enabled tools")
    
    # Calculator tool
    calculator_enabled = st.session_state["calculator_enabled"]
    calculator = st.checkbox("🧮 Calculator", value=calculator_enabled)
    if calculator_enabled != calculator:
        st.session_state["calculator_enabled"] = calculator
        restart_assistant()
    
    # File tools
    file_tools_enabled = st.session_state["file_tools_enabled"]
    file_tools = st.checkbox("📁 File tools", value=file_tools_enabled)
    if file_tools_enabled != file_tools:
        st.session_state["file_tools_enabled"] = file_tools
        restart_assistant()
    
    # Web search tool
    ddg_search_enabled = st.session_state["ddg_search_enabled"]
    ddg_search = st.checkbox("🔍 Web search", value=ddg_search_enabled)
    if ddg_search_enabled != ddg_search:
        st.session_state["ddg_search_enabled"] = ddg_search
        restart_assistant()
    
    # Finance tools
    finance_tools_enabled = st.session_state["finance_tools_enabled"]
    finance_tools = st.checkbox("📈 Finance tools", value=finance_tools_enabled)
    if finance_tools_enabled != finance_tools:
        st.session_state["finance_tools_enabled"] = finance_tools
        restart_assistant()
    
    st.markdown("#### Team members")
    
    # Research assistant
    research_assistant_enabled = st.session_state["research_assistant_enabled"]
    research_assistant = st.checkbox("🔬 Research assistant (Exa)", value=research_assistant_enabled)
    if research_assistant_enabled != research_assistant:
        st.session_state["research_assistant_enabled"] = research_assistant
        restart_assistant()
    
    st.markdown("---")
    if st.button("🔄 New session", use_container_width=True):
        restart_assistant()
    st.markdown('</div>', unsafe_allow_html=True) 