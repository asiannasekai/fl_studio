import streamlit as st
import numpy as np
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from src.core.config import Settings
    from src.core.model import GenrePatternGenerator
    from src.core.data_processor import DataProcessor
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Initialize settings
try:
    settings = Settings()
except Exception as e:
    st.error(f"Error initializing settings: {e}")
    st.stop()

# Set page config
st.set_page_config(
    page_title="FL Studio AI Assistant",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .stSelectbox {
        background-color: #2D2D2D;
    }
    .stTextInput {
        background-color: #2D2D2D;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎵 FL Studio AI Assistant")
st.markdown("""
    Generate genre-specific drum patterns using AI. Select your genre and customize the pattern generation.
    """)

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    try:
        genre = st.selectbox(
            "Select Genre",
            options=list(settings.GENRE_PATTERNS.keys()),
            index=0
        )
        
        bpm = st.slider(
            "BPM",
            min_value=settings.BPM_RANGES[genre][0],
            max_value=settings.BPM_RANGES[genre][1],
            value=(settings.BPM_RANGES[genre][0] + settings.BPM_RANGES[genre][1]) // 2
        )
        
        pattern_length = st.slider(
            "Pattern Length (beats)",
            min_value=4,
            max_value=32,
            value=16,
            step=4
        )
    except Exception as e:
        st.error(f"Error in settings sidebar: {e}")
        st.stop()

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.header("Pattern Preview")
    
    try:
        # Initialize pattern generator
        generator = GenrePatternGenerator()
        
        if st.button("Generate Pattern"):
            with st.spinner("Generating pattern..."):
                try:
                    pattern = generator.generate_pattern(genre, pattern_length)
                    
                    # Display pattern visualization
                    st.write("### Drum Pattern")
                    for drum_type in settings.GENRE_PATTERNS[genre].keys():
                        st.write(f"**{drum_type.capitalize()}**")
                        pattern_data = pattern.get(drum_type, [])
                        if pattern_data:
                            st.write(pattern_data)
                        else:
                            st.warning(f"No pattern data for {drum_type}")
                except Exception as e:
                    st.error(f"Error generating pattern: {e}")
    except Exception as e:
        st.error(f"Error initializing pattern generator: {e}")
        st.stop()

with col2:
    st.header("Pattern Details")
    
    try:
        # Display genre-specific information
        st.write(f"### {genre.capitalize()} Characteristics")
        st.write(f"**BPM Range:** {settings.BPM_RANGES[genre][0]} - {settings.BPM_RANGES[genre][1]}")
        
        st.write("### Common Patterns")
        for drum_type, patterns in settings.GENRE_PATTERNS[genre].items():
            st.write(f"**{drum_type.capitalize()}**")
            for beat, duration in patterns:
                st.write(f"- Beat {beat}, Duration: {duration}")
    except Exception as e:
        st.error(f"Error displaying pattern details: {e}")
        st.stop()

# Footer
st.markdown("---")
st.markdown("""
    ### How to Use
    1. Select your desired genre from the sidebar
    2. Adjust BPM and pattern length
    3. Click 'Generate Pattern' to create a new pattern
    4. Use the generated pattern in your FL Studio project
    """) 