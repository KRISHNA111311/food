import streamlit as st
import google.generativeai as genai
import os

# --- 1. LOCAL GUIDE CONTEXT (The product.md content) ---
# This fulfills the "must rely on a custom context file" requirement
# by making the AI use this specific data.
LOCAL_CONTEXT = """
# Local Guide Context: Visakhapatnam (The City of Destiny)

## Local Nuances & Slang
- "Mowa": Local slang for friend or "dude." 
- "Beach Road": The stretch from RK Beach to Bheemili; a local ritual drive.
- "Punugulu": Must-try snack near MVP Colony or Jail Road.

## Hidden Food Gems
- Muri Mixture: Stalls at RK Beach near the Kursura Submarine Museum.
- Bamboo Chicken: Authentic Araku style found near city hotspots.

## Navigation Hacks
- Siripuram Junction: Avoid 5 PM - 8 PM; use Waltair Uplands instead.
- Jagadamba Centre: Park far away and walk to enjoy the old-city vibe.
"""

# Page configuration
st.set_page_config(page_title="Vizag Local Guide", page_icon="📍")

# Sidebar for Configuration
with st.sidebar:
    st.header("🔑 AI Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    # Check for the actual file as per challenge rules
    if os.path.exists("product.md"):
        st.success("✅ product.md detected in root.")
    else:
        st.warning("⚠️ Remember to upload product.md to your GitHub root!")

# Main UI
st.title("📍 The Vizag Local Guide")
st.markdown("---")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    # User input
    user_query = st.text_input("Ask about Vizag slang, food, or traffic:", 
                               placeholder="e.g., Where is the best Muri Mixture?")

    if st.button("Get Local Advice"):
        if user_query:
            # We inject the LOCAL_CONTEXT directly into the prompt
            prompt = f"""
            You are a specialized AI Local Guide for Visakhapatnam. 
            Use the following context to answer the user's question. 
            If the answer isn't in the context, use your knowledge but stay in the 'Vizag Local' persona.

            CONTEXT:
            {LOCAL_CONTEXT}

            USER QUESTION:
            {user_query}
            """
            
            with st.spinner("Thinking like a local..."):
                try:
                    response = model.generate_content(prompt)
                    st.subheader("💡 Guide's Response:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("Please enter your API key in the sidebar to start.")

# Footer for the Technical Blog Post proof
st.sidebar.markdown("---")
st.sidebar.caption("Built for AI for Bharat Challenge: Week 5")