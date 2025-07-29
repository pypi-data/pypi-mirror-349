"""History component module"""

from typing import List
import streamlit as st
from phi.utils.log import logger
from ai.assistants import get_lyraios
from app.utils.session import get_tool_states

def render_history_tab(user_id: str):
    """Render history tab"""
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    if "lyraios" in st.session_state and st.session_state["lyraios"] is not None:
        lyraios = st.session_state["lyraios"]
        
        if lyraios.storage:
            st.markdown("#### History sessions")
            
            # Get history session list
            assistant_run_ids: List[str] = lyraios.storage.get_all_run_ids(user_id=user_id)
            
            if assistant_run_ids:
                current_run_id = st.session_state.get("lyraios_run_id", "")
                new_assistant_run_id = st.selectbox(
                    "Select history session", 
                    options=assistant_run_ids,
                    index=assistant_run_ids.index(current_run_id) if current_run_id in assistant_run_ids else 0
                )
                
                if "lyraios_run_id" in st.session_state and st.session_state["lyraios_run_id"] != new_assistant_run_id:
                    with st.spinner("Loading history session..."):
                        logger.info(f"---*--- Loading run: {new_assistant_run_id} ---*---")
                        tool_states = get_tool_states()
                        st.session_state["lyraios"] = get_lyraios(
                            user_id=user_id,
                            run_id=new_assistant_run_id,
                            calculator=tool_states["calculator"],
                            ddg_search=tool_states["ddg_search"],
                            file_tools=tool_states["file_tools"],
                            finance_tools=tool_states["finance_tools"],
                            research_assistant=tool_states["research_assistant"],
                        )
                        st.rerun()
            else:
                st.info("No history sessions")
        
        # Team members memory display
        if lyraios.team and len(lyraios.team) > 0:
            st.markdown("#### Team members memory")
            
            for team_member in lyraios.team:
                if len(team_member.memory.chat_history) > 0:
                    with st.expander(f"{team_member.name} memory"):
                        st.json(team_member.memory.get_llm_messages())
    st.markdown('</div>', unsafe_allow_html=True) 