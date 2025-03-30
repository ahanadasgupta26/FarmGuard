import streamlit as st
import numpy as np
import pandas as pd
import joblib
from streamlit_option_menu import option_menu
import requests
import json
from deep_translator import GoogleTranslator
import pyttsx3

model = joblib.load('disease_model.pkl')
scaler = joblib.load('scaler.pkl')
feature_columns = joblib.load('feature_columns.pkl')

yield_model = joblib.load('yield_prediction_model.pkl')

disease_labels = ['Healthy', 'Leaf Spot', 'Powdery Mildew', 'Root Rot']
disease_labels = ['Leaf Spot','Healthy', 'Powdery Mildew', 'Root Rot']
disease_labels = ['Powdery Mildew','Healthy', 'Leaf Spot', 'Root Rot']
disease_labels = ['Root Rot','Powdery Mildew','Healthy', 'Leaf Spot', ]

st.set_page_config(layout="wide")

if "selected" not in st.session_state:
    st.session_state.selected = "Home"

selected = option_menu(
    menu_title=None,
    options=["Home", "Community", "Analysis", "About Us", "Contact Us"],
    icons=["Home", "users", "graph", "Community", "mail", "mail"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

st.session_state.selected = selected

if st.session_state.selected == "Home":
    #st.write("##")

    selected_plant = st.query_params.get("plant", None)

    plant_details = {
    "Coleus": """
        **Taxonomy**:
        - Kingdom: Plantae
        - Order: Lamiales
        - Family: Lamiaceae
        - Genus: Coleus

        **Description**:
        Coleus is a genus of annual or perennial herbs or shrubs, sometimes succulent, with a fleshy or tuberous rootstock. 
        It is widely cultivated as an ornamental plant for its brightly colored foliage.

        **Uses**:
        - Ornamental plant for gardens and indoor decoration.
        - Some species are used in traditional medicine.

        **Habitat**:
        Found in the Afro-Eurasia tropics and subtropics.
    """,
    "Common Yarrow": """
        **Taxonomy**:
        - Kingdom: Plantae
        - Order: Asterales
        - Family: Asteraceae
        - Genus: Achillea
        - Species: Achillea millefolium

        **Description**:
        Common Yarrow is a flowering plant known for its feathery leaves and clusters of small, white flowers. 
        It is drought-resistant and has medicinal properties.

        **Uses**:
        - Used in traditional medicine for wound healing and as an anti-inflammatory.
        - Attracts pollinators like bees and butterflies.

        **Habitat**:
        Found in temperate regions of the Northern Hemisphere.
    """,
    "Wheat": """
        **Taxonomy**:
        - Kingdom: Plantae
        - Order: Poales
        - Family: Poaceae
        - Genus: Triticum
        - Species: Triticum aestivum

        **Description**:
        Wheat is a cereal grain and a staple food worldwide. It is used to make flour for bread, pasta, and other products.

        **Uses**:
        - Primary source of carbohydrates in many diets.
        - Used in baking, brewing, and animal feed.

        **Habitat**:
        Grown in temperate regions worldwide.
    """,
    "Bajra": """
        **Taxonomy**:
        - Kingdom: Plantae
        - Order: Poales
        - Family: Poaceae
        - Genus: Pennisetum
        - Species: Pennisetum glaucum

        **Description**:
        Bajra, or pearl millet, is a nutritious grain widely grown in arid and semi-arid regions. 
        It is drought-resistant and rich in protein and fiber.

        **Uses**:
        - Consumed as a staple food in many regions.
        - Used as fodder for livestock.

        **Habitat**:
        Grown in arid and semi-arid regions of Africa and Asia.
    """,
    "Maize": """
        **Taxonomy**:
        - Kingdom: Plantae
        - Order: Poales
        - Family: Poaceae
        - Genus: Zea
        - Species: Zea mays

        **Description**:
        Maize, also known as corn, is a cereal grain first domesticated by indigenous peoples in southern Mexico. 
        It is one of the most widely grown crops in the world.

        **Uses**:
        - Consumed as food (cornmeal, tortillas, popcorn, etc.).
        - Used in animal feed, biofuel production, and industrial products.

        **Habitat**:
        Grown in a variety of climates, primarily in temperate and tropical regions.
    """
}
    if selected_plant and selected_plant in plant_details:
        st.header(f"{selected_plant}")
        st.markdown(plant_details[selected_plant], unsafe_allow_html=True)  
        if st.button("Go Back"):
            st.query_params.clear()
            st.rerun()
    else:
        st.header("Learn about Crops")
        st.write("##")

        cols = st.columns(5)
        plant_images = {
            "Coleus": "https://www.mydomaine.com/thmb/LBMnjlmPujptoV-vYe_3HbQuvDI=/2121x0/filters:no_upscale():strip_icc()/coleus-plant-care-8c76caf0af5f4581b1ddd4ecb7458ca5.jpg",
            "Common Yarrow": "https://th.bing.com/th/id/OIP.m0wQw5eCqdUxaO70XrwqZgHaFj?rs=1&pid=ImgDetMain",
            "Wheat": "https://extension.umd.edu/sites/extension.umd.edu/files/styles/optimized/public/2021-02/wheat.jpg?itok=PdyXi_Z7",
            "Bajra": "https://i.pinimg.com/originals/89/0f/b2/890fb29b481e38c804b5d3b30fa385e3.jpg",
            "Maize": "https://www.healthbenefitstimes.com/glossary/wp-content/uploads/2020/10/Maize.jpg",
        }

        for i, (plant, image_url) in enumerate(plant_images.items()):
            with cols[i]:
                
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="{image_url}" alt="{plant}" style="height:200px; width:250px; object-fit:cover;">
                        <p>{plant}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
                if st.button(f"Learn about {plant}", key=plant):
                    st.query_params["plant"] = plant  
                    st.rerun()

    st.write("##")

    col1, col2, col3, col4 = st.columns([0.4, 1, 0.7, 1]) 
    
    with col1:
        pass
    with col2:
        st.markdown("### Community Updates")
        st.write("Stay updated with the latest news and discussions from the community:")
        st.write("- **New farming techniques shared by experts**")
        st.write("- **Upcoming webinars on sustainable agriculture**")
        st.write("- **Tool recommendations for better yield**")
        st.write("- **Join the discussion forums**")
        if st.button("Visit Community Forum"):
            st.write("Redirecting to the community forum...")

    with col3:
        pass  

    with col4:
        st.markdown("### Tasks for the Day")
        st.write("Add your daily goals:")
        task1 = st.checkbox("Check soil moisture levels")
        task2 = st.checkbox("Inspect crops for pests or diseases")
        task3 = st.checkbox("Make organic paste")
        task4 = st.checkbox("Buy fertilizer")
        task5 = st.checkbox("Water the crops")
    st.write("##")   
if selected == "About Us":
    st.markdown("<h1 style='text-align: center; color: black; margin-bottom: 50px;'>About Us</h1>", unsafe_allow_html=True)
    st.markdown(
    """
    <h2 style="text-align: center; font-size: 30px; color: black;">
        At FarmGuard, we are passionately committed to empowering farmers through the use of technology 
        designed to safeguard their crops and promote healthier, more sustainable harvests.
    </h2>
    <br>
    <h2 style="text-align: center; font-size: 30px; color: black;">
        Our mission is to transform the agricultural landscape by offering a sophisticated, 
        user-friendly mobile application that enables farmers to predict, identify, and 
        manage crop diseases with precision and assurance.
    </h2>
    <br>
    <h2 style="text-align: center; font-size: 30px; color: black;">
        After years of in-depth research and close collaboration with leading agricultural experts, 
        we have crafted a disease prediction model. This innovative tool meticulously analyzes 
        real-time data, drawing insights from intricate weather patterns, diverse soil conditions, 
        and comprehensive crop health indicators, providing farmers with the critical information 
        they need to thrive.
    </h2>
    """,
    unsafe_allow_html=True
)
    st.write("##")

if selected == "Analysis":
    #st.write("#")
    st.markdown("<h3 style='font-size:24px;'>Select Analysis Type</h3>", unsafe_allow_html=True)

    analysis_option = st.selectbox("", ["Yield Prediction", "Disease Prediction"])

    if analysis_option == "Yield Prediction":
        st.write("## Enter the following details:")
        soil_quality = st.number_input("Soil Quality (It refers to the soil's ability to sustain plant growth, support ecosystems, and maintain environmental health)", min_value=0, max_value=100, step=1)
        rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=500, step=1)
        fertilizer = st.number_input("Fertilizer (kg)", min_value=0, max_value=200, step=1)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, step=0.1)
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)

        if st.button("🔍 Predict Yield"):
            input_data = pd.DataFrame([[soil_quality, rainfall, fertilizer, temperature, humidity]],
                                      columns=['soil_quality', 'rainfall', 'fertilizer', 'temperature', 'humidity'])
        
            predicted_yield = yield_model.predict(input_data)[0]

            st.success(f"### 🌾 Predicted Yield: **{predicted_yield:.2f} kg/ha**")
    

    elif analysis_option == "Disease Prediction":
        st.write("## Enter the following details:")
        yellow_leaves = st.number_input("Yellow Leaves (0 or 1)", min_value=0, max_value=1, step=1)
        wilting = st.number_input("Wilting (0 or 1)", min_value=0, max_value=1, step=1)
        white_powder = st.number_input("White Powder (0 or 1)", min_value=0, max_value=1, step=1)
        brown_spots = st.number_input("Brown Spots (0 or 1)", min_value=0, max_value=1, step=1)
        stunted_growth = st.number_input("Stunted Growth (0 or 1)", min_value=0, max_value=1, step=1)

        if st.button("🔍 Predict Disease"):
            input_data = pd.DataFrame([[yellow_leaves, wilting, white_powder, brown_spots, stunted_growth]],
                                      columns=['yellow_leaves', 'wilting', 'white_powder', 'brown_spots', 'stunted_growth'])

            for col in feature_columns:
                if col not in input_data.columns:
                    input_data[col] = 0

            input_data = input_data[feature_columns]
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)
            predicted_label = np.argmax(prediction, axis=1)[0]
            st.success(f"### 🌱 Predicted Disease: **{disease_labels[predicted_label]}**")
                       
if selected == "Contact Us":
    st.write("Reach out to us here!")
    with st.container():
        st.header("Get In Touch With Us!")
        st.write("##")

        contact_form = """
        <style>
        .form-container {
            max-width: 500px;
            margin: auto;
        }
        .form-container input, .form-container textarea, .form-container button {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color:white;
            color:black;
        }
        </style>
        <div class="form-container">
        <form action="https://formsubmit.co/ahanadasgupta26@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        </div>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
        st.write("##")
        st.write("##")
  
if "show_chatbot" not in st.session_state:
    st.session_state["show_chatbot"] = False

if st.button("Click for help", key="toggle_chatbot"):
    st.session_state["show_chatbot"] = not st.session_state["show_chatbot"]


st.markdown(
    """
    <script>
    function toggleChatbot() {
        window.dispatchEvent(new Event("ask-button-clicked"));
    }
    </script>
    """,
    unsafe_allow_html=True
)
   
if st.session_state["show_chatbot"]:
    with st.sidebar:
        st.markdown("## Welcome to FarmGuard")
        user_input = st.text_input("You:", key="chat_input")
        if user_input:
            
            def get_gemini_response(prompt):
                api_key = "AIzaSyC1T7ySveQKBQekEw9ccA2_E7GKjU27qJw"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": prompt}]}]}
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    response.raise_for_status()
                    response_json = response.json()
                    return response_json["candidates"][0]["content"]["parts"][0]["text"]
                except requests.exceptions.RequestException as e:
                    return f"Error communicating with the API: {e}"
                except (KeyError, IndexError, json.JSONDecodeError) as e:
                    return "Error parsing API response."

            response = get_gemini_response(user_input)
            st.write("FarmBot:", response)
def get_gemini_response(prompt, api_key, model="gemini-2.0-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the API: {e}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return "Error parsing API response."

if st.session_state.selected == "Home":
    try:
        texttospeech = pyttsx3.init()
        voices = texttospeech.getProperty('voices')
        if voices:
            texttospeech.setProperty('voice', voices[0].id)
        texttospeech.setProperty('rate', 150)
    except Exception as e:
        st.error(f"Failed to initialize Text-to-Speech engine: {e}")

    languages = {
        'af': 'Afrikaans', 
        'sq': 'Albanian', 
        'am': 'Amharic', 
        'ar': 'Arabic', 
        'hy': 'Armenian', 
        'az': 'Azerbaijani',
        'eu': 'Basque', 
        'be': 'Belarusian', 
        'bn': 'Bengali', 
        'bs': 'Bosnian', 
        'bg': 'Bulgarian', 
        'ca': 'Catalan',
        'zh-CN': 'Chinese (Simplified)', 
        'zh-TW': 'Chinese (Traditional)', 
        'hr': 'Croatian', 
        'cs': 'Czech',
        'da': 'Danish', 
        'nl': 'Dutch', 
        'en': 'English', 
        'et': 'Estonian', 
        'fi': 'Finnish', 
        'fr': 'French',
        'gl': 'Galician', 
        'ka': 'Georgian', 
        'de': 'German', 
        'el': 'Greek', 
        'gu': 'Gujarati', 
        'ht': 'Haitian Creole',
        'he': 'Hebrew', 
        'hi': 'Hindi', 
        'hu': 'Hungarian', 
        'is': 'Icelandic', 
        'id': 'Indonesian', 
        'ga': 'Irish',
        'it': 'Italian', 
        'ja': 'Japanese', 
        'kn': 'Kannada', 
        'ko': 'Korean', 
        'ku': 'Kurdish', 
        'lv': 'Latvian',
        'lt': 'Lithuanian', 
        'mk': 'Macedonian', 
        'ms': 'Malay', 
        'ml': 'Malayalam', 
        'mt': 'Maltese', 
        'mi': 'Maori',
        'mr': 'Marathi', 
        'mn': 'Mongolian', 
        'my': 'Myanmar (Burmese)', 
        'ne': 'Nepali', 
        'no': 'Norwegian', 
        'or': 'Oriya',
        'ps': 'Pashto', 
        'fa': 'Persian', 
        'pl': 'Polish', 
        'pt': 'Portuguese', 
        'pa': 'Punjabi', 
        'ro': 'Romanian',
        'ru': 'Russian', 
        'sr': 'Serbian', 
        'st': 'Sesotho', 
        'si': 'Sinhala', 
        'sk': 'Slovak', 
        'sl': 'Slovenian',
        'es': 'Spanish', 
        'sw': 'Swahili', 
        'sv': 'Swedish', 
        'tg': 'Tajik', 
        'ta': 'Tamil', 
        'te': 'Telugu', 
        'th': 'Thai',
        'tr': 'Turkish', 
        'uk': 'Ukrainian', 
        'ur': 'Urdu', 
        'uz': 'Uzbek', 
        'vi': 'Vietnamese', 
        'cy': 'Welsh',
        'xh': 'Xhosa', 
        'yi': 'Yiddish', 
        'yo': 'Yoruba', 
        'zu': 'Zulu'
    }

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Select Source Language", options=list(languages.values()),
                                    index=list(languages.values()).index("English"))
    with col2:
        target_lang = st.selectbox("Select Target Language", options=list(languages.values()),
                                    index=list(languages.values()).index("Spanish"))

    text = st.text_area("Enter text to translate:", height=150)

    if st.button("Translate"):
        if text.strip():
            source_code = list(languages.keys())[list(languages.values()).index(source_lang)]
            target_code = list(languages.keys())[list(languages.values()).index(target_lang)]

            try:
                translated_text = GoogleTranslator(source=source_code, target=target_code).translate(text)
                st.success(f"**Translated Text:** {translated_text}")
                st.session_state["translated_text"] = translated_text
            except Exception as e:
                st.error(f"Translation failed: {e}")
        else:
            st.warning("Please enter text to translate.")

