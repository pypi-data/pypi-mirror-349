"""Chat interface component module"""

import streamlit as st
from phi.assistant import Assistant
from phi.utils.log import logger
from ai.assistants import get_lyraios
from app.utils.session import get_tool_states
from app.db.models import ChatMessage
from app.config.settings import chat_settings
from datetime import datetime

def init_assistant(user_id: str) -> Assistant:
    """Initialize assistant"""
    if "lyraios" not in st.session_state or st.session_state["lyraios"] is None:
        with st.spinner("Initializing LYRAIOS..."):
            logger.info("---*--- Creating LYRAIOS ---*---")
            try:
                tool_states = get_tool_states()
                lyraios = get_lyraios(
                    user_id=user_id,
                    calculator=tool_states["calculator"],
                    ddg_search=tool_states["ddg_search"],
                    file_tools=tool_states["file_tools"],
                    finance_tools=tool_states["finance_tools"],
                    research_assistant=tool_states["research_assistant"],
                )
                st.session_state["lyraios"] = lyraios
            except Exception as e:
                st.error(f"Failed to create assistant: {str(e)}")
                logger.error(f"Failed to create assistant: {e}")
                return None
    
    return st.session_state["lyraios"]

def init_chat_history(lyraios: Assistant):
    """Initialize chat history"""
    if "messages" not in st.session_state:
        assistant_chat_history = lyraios.memory.get_chat_history()
        if len(assistant_chat_history) > 0:
            logger.debug("Loading chat history")
            st.session_state["messages"] = assistant_chat_history
        else:
            logger.debug("No chat history found")
            st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm LYRAIOS, an advanced AI assistant. I can help you find information, answer questions, perform calculations and more. Please let me know what you need help with?"}]

def create_assistant_run(lyraios: Assistant):
    """Create assistant run"""
    try:
        if "lyraios_run_id" not in st.session_state or st.session_state["lyraios_run_id"] is None:
            run_id = lyraios.create_run()
            st.session_state["lyraios_run_id"] = run_id
            logger.info(f"Created new run: {run_id}")
    except Exception as e:
        st.error(f"Failed to create assistant run: {str(e)}")
        logger.error(f"Failed to create run: {e}")
        return False
    
    return True

def render_chat_interface(user_id: str):
    """Render chat interface"""
    # Initialize assistant
    lyraios = init_assistant(user_id)
    if lyraios is None:
        return
    
    # Create assistant run
    if not create_assistant_run(lyraios):
        return
    
    # Initialize chat history
    init_chat_history(lyraios)
    
    # Create chat interface container
    chat_container = st.container()
    
    # Display existing chat messages
    with chat_container:
        for message in st.session_state["messages"]:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Enter your question..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response = ""
                
                with st.spinner("Thinking..."):
                    for delta in lyraios.run(prompt):
                        response += delta  # type: ignore
                        response_placeholder.markdown(response)
                
                st.session_state["messages"].append({"role": "assistant", "content": response})

def save_message(message):
    db = ChatMessage(content=message, timestamp=datetime.now())
    db.save()
    return {"status": "success", "settings": chat_settings.get_all()} 