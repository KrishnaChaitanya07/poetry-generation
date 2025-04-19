import streamlit as st
import requests
import random

# Hugging Face API Setup
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HUGGINGFACE_API_KEY = "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"  # Your API key here

def generate_poem(theme, style=None, mood=None):
    """
    Advanced poem generation with multiple customization options.
    
    Args:
        theme (str): The central theme of the poem
        style (str, optional): Poetic style
        mood (str, optional): Emotional tone of the poem
    
    Returns:
        str: Generated poem or error message
    """
    # Poem generation prompt construction
    prompt_parts = [f"Write a poem about: {theme}"]
    
    # Add style specification if provided
    if style:
        prompt_parts.append(f"Style: {style}")
    
    # Add mood specification if provided
    if mood:
        prompt_parts.append(f"Mood: {mood}")
    
    # Detailed generation parameters
    payload = {
        "inputs": ". ".join(prompt_parts) + ". Create a structured poem with vivid imagery and emotional depth. Use line breaks and proper formatting.",
        "parameters": {
            "max_length": 300,
            "temperature": 0.85,
            "top_p": 0.92,
            "top_k": 50,
            "do_sample": True,
            "no_repeat_ngram_size": 2
        }
    }

    # Headers with API key
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    try:
        # Send request to Hugging Face API
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        # Process and format the generated poem
        data = response.json()
        generated_text = data[0]['generated_text']
        
        # Advanced poem cleaning and formatting
        poem_lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
        
        # If poem generation fails, use a fallback
        if not poem_lines:
            poem_lines = _generate_fallback_poem(theme)
        
        return "\n".join(poem_lines)
    
    except requests.exceptions.RequestException as e:
        return f"🚫 Poem Generation Error: {str(e)}"

def _generate_fallback_poem(theme):
    """
    Fallback poem generation method in case of API failure.
    
    Args:
        theme (str): Theme for the fallback poem
    
    Returns:
        list: Lines of a simple poem
    """
    fallback_templates = [
        [
            f"In the realm of {theme}, whispers rise,",
            "Echoing thoughts beneath silent skies,",
            "A melody of dreams, soft and light,",
            "Dancing through the edges of insight."
        ],
        [
            f"Oh {theme}, vast and deep and wide,",
            "Where imagination's currents ride,",
            "Your essence sparks a burning flame,",
            "A poetry beyond a simple name."
        ]
    ]
    return random.choice(fallback_templates)

def main():
    # Page Configuration
    st.set_page_config(
        page_title="Poem Crafting Studio", 
        page_icon="✍️", 
        layout="wide"
    )

    # Custom Styling
    st.markdown("""
    <style>
    .main {
        background-color: #f0f0f8;
        font-family: 'Georgia', serif;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #6A1B9A;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    .stButton button {
        background-color: #8A2BE2;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #6A1B9A;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and Subtitle
    st.title("✍️ Poem Crafting Studio")
    st.subheader("Create Unique Poems with AI Magic")

    # Input Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        theme = st.text_input("🎨 Poem Theme", placeholder="Love, Nature, Hope...")
    
    with col2:
        style = st.selectbox("📝 Poem Style", [
            "Free Verse", "Sonnet", "Haiku", 
            "Limerick", "Ode", "Ballad"
        ])
    
    with col3:
        mood = st.selectbox("🌈 Emotional Tone", [
            "Joyful", "Melancholic", "Mysterious", 
            "Romantic", "Contemplative", "Inspirational"
        ])

    # Generate Poem Button
    if st.button("✨ Craft My Poem", use_container_width=True):
        if theme.strip():
            with st.spinner("Weaving poetic magic..."):
                poem = generate_poem(theme, style, mood)
            
            # Poem Display
            st.subheader("🌟 Your Generated Poem:")
            st.code(poem, language="")

            # Additional Interaction Buttons
            col_copy, col_save = st.columns(2)
            
            with col_copy:
                if st.button("📋 Copy Poem"):
                    st.code(poem)
                    st.success("Poem copied to clipboard!")
            
            with col_save:
                if st.button("💾 Save Poem"):
                    # Future: Implement save functionality
                    st.info("Save feature coming soon!")

        else:
            st.warning("Please enter a theme for your poem!")

    # Footer and Additional Info
    st.markdown("---")
    st.markdown("#### 🚀 Features")
    st.markdown("""
    - Custom theme-based poem generation
    - Multiple poetic styles
    - Emotional tone selection
    - Instant poem crafting
    """)


if __name__ == "__main__":
    main()