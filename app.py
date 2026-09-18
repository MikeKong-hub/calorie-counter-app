import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration for Mobile Layout
st.set_page_config(page_title="AI Calorie Counter", page_icon="🥗", layout="centered")

st.title("🥗 AI Food Calorie Scanner")
st.write("Take a picture of your plate to estimate calories and macros.")

# 2. Securely Retrieve the API Key
# For local testing, it looks for a local secret; on the cloud, it uses Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please configure it in your environment settings.")
    st.stop()

# 3. Handle the Camera Input
# On mobile, this natively opens the phone's default camera application
uploaded_file = st.camera_input("Scan your plate")

if uploaded_file is not None:
    # Open the image using Pillow
    image = Image.open(uploaded_file)
    st.image(image, caption="Processing your meal...", use_container_width=True)
    
    # 4. Trigger the AI Model
    with st.spinner("Analyzing nutrients... please wait..."):
        try:
            # Using Gemini 2.0 Flash for blazing fast vision processing
            model = genai.GenerativeModel("gemini-2.0-flash")
            
            # Crafting a precise prompt to force the AI to return clean data
            prompt = """
            You are an expert nutritionist. Analyze the food items in this image.
            Provide the following breakdown:
            1. Identified Food Items & Estimated Weights (in grams).
            2. Total Estimated Calories.
            3. Macro Breakdown: Macronutrient distribution (Protein, Carbs, Fats in grams).
            
            Be concise, clear, and structure the output nicely using markdown tables where appropriate.
            If the image does not contain any food, politely state that you cannot detect a meal.
            """
            
            # Send both the instruction and the image to the model
            response = model.generate_content([prompt, image])
            
            # 5. Render the Results
            st.success("Analysis Complete!")
            st.markdown("### 📊 Nutritional Breakdown")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"An error occurred during scanning: {e}")