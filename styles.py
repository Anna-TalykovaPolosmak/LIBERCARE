def load_css():
    return """
    html {
        scroll-behavior: smooth;
        scroll-padding-top: 0;
    }

    .stApp {
        background-image: url("https://images5.alphacoders.com/138/1382223.png");
        background-attachment: fixed;
        background-size: cover;
    }

    /* Modal styles */
    .modal-container {
        position: relative;
        z-index: 1000;
    }

    .modal {
        background-color: rgba(47, 53, 66, 0.95);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    .modal h4 {
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 1.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .modal ul {
        margin: 1.5rem 0;
        padding-left: 1.2rem;
        list-style-type: none;
    }

    .modal li {
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }

    /* Streamlit checkbox customization */
    .stCheckbox {
        margin: 1rem 0;
    }

    .stCheckbox label {
        color: white !important;
        font-size: 1.1em !important;
    }

    .stCheckbox label span {
        color: white !important;
    }

    /* Streamlit button customization */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        width: 100% !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        margin-top: 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #45a049 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }

    .stButton > button:disabled {
        background-color: #cccccc !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    /* Input styles */
    .stTextInput > div > div {
        background-color: rgba(47, 53, 66, 0.8) !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 20px !important;
        color: white !important;
    }
    
    .stChatInput {
        margin-bottom: 40px !important;
    }

    /* Article styles */
    .article-container {
        padding: 0 20px !important;
        max-width: 1800px !important;
        margin: 0 auto !important;
    }
    
    .article-card {
        background-color: rgba(47, 53, 66, 0.9) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        margin: 10px !important;
        height: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        max-width: 400px !important;
        width: 100% !important;
        cursor: pointer !important;
    }

    .article-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    .article-card h4 {
        color: white !important;
        font-size: 1em !important;
        line-height: 1.3 !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100px !important;
        overflow: hidden !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 4 !important;
        -webkit-box-orient: vertical !important;
        text-overflow: ellipsis !important;
    }

    .article-card img {
        width: 100% !important;
        aspect-ratio: 4/3 !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 8px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: transform 0.3s ease !important;
    }

    .article-card img:hover {
        transform: scale(1.02);
    }

    .article-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block !important;
        height: 100% !important;
    }

    /* Title styles */
    .title {
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        padding: 2rem 0;
        margin-bottom: 20px;
        font-size: 2.5em;
    }

    .articles-title {
        color: white;
        text-align: center;
        margin: 40px 0 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-size: 1.8em;
    }

    /* Chat message styles */
    .stChatMessage {
        background-color: rgba(47, 53, 66, 0.8) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Search result styles */
    .search-result {
        background-color: rgba(47, 53, 66, 0.8);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .search-result h4 {
        color: #4CAF50;
        margin: 0 0 10px 0;
    }

    .search-result a {
        color: #4CAF50;
        text-decoration: none;
    }

    .search-result p {
        color: white;
        margin: 0;
        font-size: 0.9em;
    }

    /* Scrollbar styles */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(47, 53, 66, 0.3);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.4);
    }

    /* Responsive styles */
    @media (max-width: 1200px) {
        .article-card {
            height: 400px !important;
        }
        
        .article-card h4 {
            height: 90px !important;
        }
        
        .modal {
            max-width: 90%;
            padding: 2rem;
        }
    }

    @media (max-width: 768px) {
        .article-card {
            height: 380px !important;
        }
        
        .article-card h4 {
            font-size: 0.95em !important;
            height: 80px !important;
        }
        
        .title {
            font-size: 2em;
        }
        
        .articles-title {
            font-size: 1.5em;
        }

        .modal {
            padding: 1.5rem;
            width: 95%;
        }

        .modal h4 {
            font-size: 1.3em;
        }

        .modal label {
            font-size: 1em;
        }

        .stButton > button {
            font-size: 1.1rem !important;
            padding: 0.6rem 1.5rem !important;
        }
    }
    """