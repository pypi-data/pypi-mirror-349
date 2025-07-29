"""Knowledge base component module"""

from typing import List
import streamlit as st
from phi.document import Document
from phi.document.reader.pdf import PDFReader
from phi.document.reader.website import WebsiteReader

def render_knowledge_base_tab():
    """Render knowledge base tab"""
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    if "lyraios" in st.session_state and st.session_state["lyraios"] is not None:
        lyraios = st.session_state["lyraios"]
        
        if lyraios.knowledge_base:
            st.markdown("#### Add webpage to knowledge base")
            
            # URL input and add button
            input_url = st.text_input(
                "Enter URL", 
                placeholder="https://example.com",
                key=st.session_state["url_scrape_key"]
            )
            
            if st.button("➕ Add webpage", use_container_width=True):
                if input_url:
                    with st.spinner("Processing webpage content..."):
                        if f"{input_url}_scraped" not in st.session_state:
                            scraper = WebsiteReader(max_links=2, max_depth=1)
                            web_documents: List[Document] = scraper.read(input_url)
                            if web_documents:
                                lyraios.knowledge_base.load_documents(web_documents, upsert=True)
                                st.success(f"Successfully added {len(web_documents)} documents")
                            else:
                                st.error("Failed to read webpage content")
                            st.session_state[f"{input_url}_uploaded"] = True
            
            st.markdown("#### Add PDF document")
            
            # PDF upload
            uploaded_file = st.file_uploader(
                "Upload PDF file", 
                type="pdf", 
                key=st.session_state["file_uploader_key"]
            )
            
            if uploaded_file is not None:
                with st.spinner("Processing PDF document..."):
                    file_name = uploaded_file.name.split(".")[0]
                    if f"{file_name}_uploaded" not in st.session_state:
                        reader = PDFReader()
                        file_documents: List[Document] = reader.read(uploaded_file)
                        if file_documents:
                            lyraios.knowledge_base.load_documents(file_documents, upsert=True)
                            st.success(f"Successfully added {len(file_documents)} documents")
                        else:
                            st.error("Failed to read PDF document")
                        st.session_state[f"{file_name}_uploaded"] = True
            
            # Clear knowledge base button
            if lyraios.knowledge_base.vector_db:
                st.markdown("---")
                if st.button("🗑️ Clear knowledge base", use_container_width=True):
                    with st.spinner("Clearing knowledge base..."):
                        lyraios.knowledge_base.vector_db.clear()
                        st.success("Knowledge base cleared")
    st.markdown('</div>', unsafe_allow_html=True) 