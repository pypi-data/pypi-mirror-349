"""Session state management module"""

import streamlit as st
from phi.utils.log import logger

def init_session_state():
    """Initialize session state"""
    # Tool state initialization
    if "calculator_enabled" not in st.session_state:
        st.session_state["calculator_enabled"] = True
    
    if "file_tools_enabled" not in st.session_state:
        st.session_state["file_tools_enabled"] = True
    
    if "ddg_search_enabled" not in st.session_state:
        st.session_state["ddg_search_enabled"] = True
    
    if "finance_tools_enabled" not in st.session_state:
        st.session_state["finance_tools_enabled"] = True
    
    if "research_assistant_enabled" not in st.session_state:
        st.session_state["research_assistant_enabled"] = True
    
    # Knowledge base state initialization
    if "url_scrape_key" not in st.session_state:
        st.session_state["url_scrape_key"] = 0
    
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 100

def restart_assistant():
    """Restart assistant, clear session state"""
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["lyraios"] = None
    st.session_state["lyraios_run_id"] = None
    if "messages" in st.session_state:
        del st.session_state["messages"]
    if "url_scrape_key" in st.session_state:
        st.session_state["url_scrape_key"] += 1
    if "file_uploader_key" in st.session_state:
        st.session_state["file_uploader_key"] += 1
    st.rerun()

def get_tool_states():
    """Get tool states"""
    return {
        "calculator": st.session_state["calculator_enabled"],
        "file_tools": st.session_state["file_tools_enabled"],
        "ddg_search": st.session_state["ddg_search_enabled"],
        "finance_tools": st.session_state["finance_tools_enabled"],
        "research_assistant": st.session_state["research_assistant_enabled"]
    } 