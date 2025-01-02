import streamlit as st
import base64
from streamlit_lottie import st_lottie
import requests

# Configure page
st.set_page_config(
    page_title="Disney Movies Analysis",
    page_icon="🏰",
    layout="wide"
)

# Custom CSS with refined styling
st.markdown("""
    <style>
    /* Base theme colors */
    :root {
        --primary-color: #1a1a2e;
        --secondary-color: #16213e;
        --accent-color: #0f3460;
        --text-color: #ffffff;
        --shadow-color: rgba(0, 0, 0, 0.2);
    }

    /* Main container */
    .main .block-container {
        padding: 2rem !important;
    }

    /* Background image setup */
    .stApp {
        background-image: linear-gradient(
            rgba(0, 0, 0, 0.7),
            rgba(0, 0, 0, 0.7)
        ), url('data:image/jpg;base64,{background_image}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
    }

    /* Navigation buttons */
    .stButton > button {
        width: 100%;
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px);
    }

    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
    }

    .logo-container img {
        max-width: 150px;
        margin: 0 auto;
    }

    /* Title styling */
    .title-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        backdrop-filter: blur(5px);
    }

    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px var(--shadow-color);
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Description text */
    .description-text {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin: 1.5rem 0;
        padding: 1.5rem;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    </style>
""", unsafe_allow_html=True)

# Function to load and encode background image
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set background image
background_image = get_base64_encoded_image("assets/background.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(
            rgba(0, 0, 0, 0.7),
            rgba(0, 0, 0, 0.7)
        ), url("data:image/jpg;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    # Logo in sidebar
    st.markdown("""
        <div class="logo-container">
            <img src="data:image/png;base64,{}" alt="Disney Logo">
        </div>
    """.format(get_base64_encoded_image("assets/logo.png")), unsafe_allow_html=True)
    
    if st.button("Home", key="home"):
        st.session_state["page"] = "home"
    if st.button("Explore Data", key="explore"):
        st.session_state["page"] = "explore"
    if st.button("Visualizations", key="viz"):
        st.session_state["page"] = "viz"
    if st.button("Insights", key="insights"):
        st.session_state["page"] = "insights"

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Main content
if st.session_state["page"] == "home":
    st.markdown("""
        <div class="title-container">
            <h1 style="color: white; font-size: 3rem;">Disney Movies Analysis</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Center content
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
            <div class="description-text">
                <h2>Explore the Magic of Disney Through Data!</h2>
                <p>Discover insights about your favorite Disney movies, from classics to modern hits.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Metrics display
    col1, col2, col3 = st.columns(3)
    
    metrics = [
        {"label": "Total Movies", "value": "500+"},
        {"label": "Years of Magic", "value": "95+"},
        {"label": "Box Office", "value": "$100B+"}
    ]
    
    for col, metric in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{metric['label']}</div>
                    <div class="metric-value">{metric['value']}</div>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state["page"] == "explore":
    st.markdown("""
        <div class="title-container">
            <h1 style="color: white;">Explore Data</h1>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state["page"] == "viz":
    st.markdown("""
        <div class="title-container">
            <h1 style="color: white;">Visualizations</h1>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state["page"] == "insights":
    st.markdown("""
        <div class="title-container">
            <h1 style="color: white;">Insights</h1>
        </div>
    """, unsafe_allow_html=True)  