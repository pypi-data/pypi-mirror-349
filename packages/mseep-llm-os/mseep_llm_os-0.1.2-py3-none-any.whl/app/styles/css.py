"""CSS styles definition module"""

def get_css_styles():
    """Return application CSS styles"""
    return """
    <style>
        /* Main style */
        .main {
            background-color: #f9f9f9;
        }
        
        /* Chat message container */
        .stChatMessage {
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
        }
        
        /* User message style */
        .stChatMessage[data-testid="stChatMessageUser"] {
            background-color: #e6f7ff;
            border: 1px solid #91d5ff;
        }
        
        /* Assistant message style */
        .stChatMessage[data-testid="stChatMessageAssistant"] {
            background-color: #f6ffed;
            border: 1px solid #b7eb8f;
        }
        
        /* Title style */
        h1 {
            color: #1a1a1a;
            font-weight: 700;
        }
        
        /* Sidebar style */
        .css-1d391kg {
            background-color: #f0f2f6;
        }
        
        /* Button style */
        .stButton>button {
            border-radius: 8px;
            font-weight: 500;
        }
        
        /* Main button style */
        .stButton>button.primary-btn {
            background-color: #1890ff;
            color: white;
        }
        
        /* Separator style */
        hr {
            margin: 15px 0;
        }
        
        /* Tools selection area */
        .tools-section {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        /* Knowledge base area */
        .knowledge-section {
            background-color: #f0f7ff;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        /* Optimized tab styles */
        .stTabs {
            margin-top: 15px;
            margin-bottom: 20px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 0;
            margin-bottom: 15px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 8px 8px 0 0;
            padding: 10px 15px;
            margin-right: 2px;
            font-weight: 500;
            font-size: 14px;
            border: 1px solid #e0e0e0;
            border-bottom: none;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            border-bottom: 2px solid #1890ff;
            color: #1890ff;
        }
        
        /* Tools option style */
        .stCheckbox {
            padding: 8px 0;
        }
        
        /* Sidebar content spacing */
        .sidebar-content {
            padding: 10px 0;
        }
        
        /* Tab content area */
        .tab-content {
            padding: 10px 5px;
            background-color: #ffffff;
            border-radius: 0 0 8px 8px;
            margin-top: -15px;
            border: 1px solid #e0e0e0;
            border-top: none;
        }
    </style>
    """ 