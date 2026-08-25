import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="wide"
)

# ============================================================
# INITIALIZE OPENAI CLIENT
# ============================================================
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #C77D5E, #A8654A);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    .recipe-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border-left: 4px solid #D4AF37;
        margin-bottom: 1rem;
    }
    .recipe-card h3 {
        color: #C77D5E;
        margin-bottom: 0.5rem;
    }
    .recipe-card p {
        color: #333;
        line-height: 1.7;
    }
    .recipe-meta {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin: 0.5rem 0 1rem 0;
        font-size: 0.9rem;
        color: #666;
    }
    .recipe-meta span {
        background: #F5EEF9;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
    }
    .stButton > button {
        background: #D4AF37;
        color: #3D2B1F;
        font-weight: 700;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #C77D5E;
        color: white;
        transform: scale(1.02);
    }
    .favorite-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        transition: transform 0.3s;
    }
    .favorite-btn:hover {
        transform: scale(1.2);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
    <div class="main-header">
        <h1>🍳 AI Recipe Generator</h1>
        <p>Turn your ingredients into a delicious meal</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'current_recipe' not in st.session_state:
    st.session_state.current_recipe = None
if 'recipe_history' not in st.session_state:
    st.session_state.recipe_history = []

# ============================================================
# SIDEBAR - FAVORITES & HISTORY
# ============================================================
with st.sidebar:
    st.header("⭐ My Saved Recipes")
    
    if st.session_state.favorites:
        for i, recipe in enumerate(st.session_state.favorites):
            if st.button(f"🍽️ {recipe.get('name', 'Recipe')}", key=f"fav_{i}"):
                st.session_state.current_recipe = recipe
                st.rerun()
        
        if st.button("🗑️ Clear All Favorites", type="secondary"):
            st.session_state.favorites = []
            st.rerun()
    else:
        st.info("No saved favorites yet. Click the ❤️ button to save a recipe!")
    
    st.markdown("---")
    st.header("📜 Recent Recipes")
    
    if st.session_state.recipe_history:
        for i, recipe in enumerate(st.session_state.recipe_history[-5:]):
            st.write(f"{i+1}. {recipe.get('name', 'Recipe')}")
    else:
        st.info("No recent recipes. Generate one!")

# ============================================================
# MAIN FORM
# ============================================================
st.subheader("🥘 What ingredients do you have?")

col1, col2 = st.columns([3, 1])

with col1:
    ingredients = st.text_area(
        "Enter your ingredients (separated by commas)",
        placeholder="e.g., chicken, rice, tomatoes, onions, garlic, pepper",
        height=80
    )

with col2:
    st.markdown("### ⚙️ Options")
    meal_type = st.selectbox(
        "Meal Type",
        ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
    )
    cuisine = st.selectbox(
        "Cuisine",
        ["Any", "Nigerian", "Italian", "Chinese", "Mexican", "Indian", "French", "Japanese"]
    )
    servings = st.number_input("Servings", min_value=1, max_value=10, value=2)

# Additional dietary preferences
st.subheader("🥗 Dietary Preferences (Optional)")
col3, col4, col5 = st.columns(3)

with col3:
    vegetarian = st.checkbox("Vegetarian")
with col4:
    vegan = st.checkbox("Vegan")
with col5:
    gluten_free = st.checkbox("Gluten Free")

# ============================================================
# GENERATE RECIPE
# ============================================================
if st.button("✨ Generate Recipe"):
    if not ingredients.strip():
        st.error("Please enter at least one ingredient.")
        st.stop()
    
    if not client.api_key:
        st.error("OpenAI API key not set. Please add it to Streamlit secrets.")
        st.stop()
    
    with st.spinner("👨‍🍳 AI is creating your recipe..."):
        # Build prompt
        prompt = f"""
        Create a delicious recipe using these ingredients:
        
        Ingredients: {ingredients}
        Meal Type: {meal_type}
        Cuisine: {cuisine}
        Servings: {servings}
        Vegetarian: {vegetarian}
        Vegan: {vegan}
        Gluten Free: {gluten_free}
        
        Please provide:
        1. Recipe name (creative and appetizing)
        2. Cooking time (prep + cook)
        3. A list of all ingredients with measurements
        4. Step-by-step cooking instructions
        5. Estimated nutrition info (calories, protein, carbs, fat)
        6. Optional: A tip or variation
        
        Format the recipe clearly and make it easy to follow.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert chef and recipe creator. You create delicious, easy-to-follow recipes using the ingredients provided. Your recipes are creative, practical, and always taste amazing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            recipe_content = response.choices[0].message.content
            
            # Parse the recipe to extract name
            lines = recipe_content.split('\n')
            recipe_name = lines[0].replace('#', '').strip() if lines else "My Recipe"
            
            # Create recipe object
            recipe = {
                "name": recipe_name,
                "ingredients": ingredients,
                "content": recipe_content,
                "meal_type": meal_type,
                "cuisine": cuisine,
                "servings": servings,
                "date_created": datetime.now().strftime("%B %d, %Y"),
                "is_favorite": False
            }
            
            st.session_state.current_recipe = recipe
            
            # Add to history
            if recipe not in st.session_state.recipe_history:
                st.session_state.recipe_history.append(recipe)
            
            st.success("✅ Recipe generated successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating recipe: {e}")

# ============================================================
# DISPLAY RECIPE
# ============================================================
if st.session_state.current_recipe:
    recipe = st.session_state.current_recipe
    
    st.markdown("---")
    
    # Recipe header with actions
    col_title, col_actions = st.columns([3, 1])
    
    with col_title:
        st.subheader(f"🍽️ {recipe['name']}")
        st.markdown(f"""
            <div class="recipe-meta">
                <span>⏱️ {recipe.get('meal_type', 'Any')}</span>
                <span>🌍 {recipe.get('cuisine', 'Any')}</span>
                <span>👥 {recipe.get('servings', 2)} servings</span>
                <span>📅 {recipe.get('date_created', 'Today')}</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col_actions:
        # Favorite button
        is_fav = any(f.get('name') == recipe['name'] for f in st.session_state.favorites)
        if st.button("❤️" if is_fav else "🤍", key="favorite_btn"):
            if is_fav:
                st.session_state.favorites = [f for f in st.session_state.favorites if f.get('name') != recipe['name']]
                st.toast("Removed from favorites")
            else:
                recipe_copy = recipe.copy()
                recipe_copy['is_favorite'] = True
                st.session_state.favorites.append(recipe_copy)
                st.toast("Added to favorites! ❤️")
            st.rerun()
    
    # Display recipe content
    st.markdown(f"""
    <div class="recipe-card">
        {recipe['content'].replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    # Download and share buttons
    col_download, col_share = st.columns(2)
    
    with col_download:
        st.download_button(
            label="📥 Download Recipe",
            data=recipe['content'],
            file_name=f"{recipe['name'].replace(' ', '_')}_Recipe.txt",
            mime="text/plain"
        )
    
    with col_share:
        # Share on WhatsApp
        share_text = f"🍳 {recipe['name']}\n\n{recipe['content'][:500]}..."
        share_url = f"https://wa.me/?text={share_text.replace(' ', '%20').replace(chr(10), '%0A')}"
        st.markdown(f"""
            <a href="{share_url}" target="_blank" style="
                display: inline-block;
                background: #25D366;
                color: white;
                padding: 0.5rem 2rem;
                border-radius: 50px;
                text-decoration: none;
                font-weight: 700;
                text-align: center;
                width: 100%;
            ">
                <i class="fab fa-whatsapp"></i> Share on WhatsApp
            </a>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.85rem; padding: 1rem 0;">
        🍳 AI Recipe Generator — Turn your ingredients into delicious meals ✨
    </div>
""", unsafe_allow_html=True)
