import streamlit as st
import os
from datetime import datetime
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
import base64
import config
from utils import ChatEnvironment, create_character, save_chat_history, load_chat_history
import utils

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom CSS
def load_css():
    st.markdown("""
        <style>
            /* Main container padding */
            .main > div {
                padding: 2rem 3rem;
            }
            
            /* Typography */
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 1rem;
            }
            
            /* Chat messages */
            .stChatMessage {
                padding: 2rem;
                border-radius: 10px;
                margin: 1rem 2;
                background-color: #000000;
            }
            
            /* Sidebar */
            .css-1d391kg {
                padding: 2rem 1rem;
            }
            
            /* Input fields */
            .stTextInput>div>div>input {
                padding: 1.75rem;
                border-radius: 8px;
            }
            
            /* Text area */
            .stTextArea>div>div>textarea {
                padding: 0.75rem;
                border-radius: 8px;
            }
            
            /* Buttons */
            .stButton>button {
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }
            
            /* Environment info box */
            .element-container .stAlert {
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
            
            /* Character cards */
            .stExpander {
                border-radius: 8px;
                margin: 0.5rem 0;
            }
            
            /* Chat container */
            .stChatMessageContent {
                background-color: red;
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            /* User messages */
            .stMarkdown {
                padding: 0.5rem 0;
            }
            
            /* Images */
            .stImage {
                border-radius: 8px;
                margin: 0.5rem 0;
            }
            
            /* Multiselect */
            .stMultiSelect {
                margin: 1rem 0;
            }
            
            /* Slider */
            .stSlider {
                margin: 1.5rem 0;
            }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_characters' not in st.session_state:
        st.session_state.selected_characters = []
    if 'environment' not in st.session_state:
        st.session_state.environment = None
    if 'chat_env_description' not in st.session_state:
        st.session_state.chat_env_description = ""
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.7

def save_uploaded_image(uploaded_file):
    """Save uploaded image to a temporary file and return the path."""
    if uploaded_file is not None:
        # Create a temporary file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save the uploaded file
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Convert to base64
        base64_image = utils.image_to_base64(temp_path)
        return temp_path, base64_image
    return None, None

def create_or_update_environment(selected_chars, env_description):
    """Create or update the chat environment with selected characters."""
    env = ChatEnvironment(
        name="Persona Chat",
        agents=[create_character(config.CHARACTERS[char]) for char in selected_chars],
        description=env_description
    )
    
    # Set the environment context for all agents
    if env_description:
        env.broadcast_context(f"""Current environment/context: {env_description}
Please consider this context in all your responses and interactions.""")
    
    return env

def main():
    st.set_page_config(
        page_title="Persona Simulator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()
    
    init_session_state()

    # Sidebar
    with st.sidebar:
        # Display logo
        if os.path.exists(config.APP_LOGO):
            st.image(config.APP_LOGO, width=200)
        
        st.title("Settings")
        
        # Character selection with multi-select dropdown
        st.subheader("Select Characters")
        available_characters = list(config.CHARACTERS.keys())
        selected_chars = st.multiselect(
            "Choose personas to interact with:",
            available_characters,
            default=st.session_state.selected_characters
        )
        
        # Update selected characters
        st.session_state.selected_characters = selected_chars

        # Display character cards
        if selected_chars:
            st.subheader("Selected Characters")
            for char_type in selected_chars:
                char_config = config.CHARACTERS[char_type]
                with st.expander(f"{char_type} ({char_config['name']})"):
                    if os.path.exists(char_config['image']):
                        st.image(char_config['image'], width=150)
                    st.write(f"**Age:** {char_config['age']}")
                    st.write(f"**Nationality:** {char_config['nationality']}")
                    st.write(f"**Occupation:** {char_config['occupation']}")
                    st.write("**Traits:**")
                    for trait in char_config['personality_traits']:
                        st.write(f"- {trait['trait']}")

        # Temperature adjustment
        st.subheader("LLM Settings")
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher values make the output more random, lower values make it more focused and deterministic."
        )

        # Environment description
        st.subheader("Environment Description")
        new_env_description = st.text_area(
            "Describe the environment/context:",
            value=st.session_state.chat_env_description,
            help="Describe the situation or context for the conversation.",
            height=150
        )

        # Update environment if description changes
        if new_env_description != st.session_state.chat_env_description:
            st.session_state.chat_env_description = new_env_description
            if st.session_state.environment and new_env_description:
                st.session_state.environment.broadcast_context(
                    f"""Current environment/context: {new_env_description}
                    Please consider this context in all your responses and interactions."""
                )

        # Save/Load chat history
        st.subheader("Chat History")
        if st.button("Save Chat History"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            utils.create_chat_folder()
            save_chat_history(
                st.session_state.chat_history,
                f"chat_histories/chat_{timestamp}.json"
            )
            st.success("Chat history saved!")

        uploaded_file = st.file_uploader("Load Chat History", type=['json'])
        if uploaded_file is not None:
            st.session_state.chat_history = load_chat_history(uploaded_file)
            st.success("Chat history loaded!")

    # Main chat interface
    st.title("Persona Simulator")

    # Display current environment description if set
    if st.session_state.chat_env_description:
        st.info(f"Current Environment: {st.session_state.chat_env_description}")

    # Create or update environment when characters are selected
    if selected_chars:
        if (not st.session_state.environment or 
            set(selected_chars) != {char.name for char in st.session_state.environment.agents}):
            st.session_state.environment = create_or_update_environment(
                selected_chars,
                st.session_state.chat_env_description
            )

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
                if "image" in message:
                    if isinstance(message["image"], str) and message["image"].startswith("data:image"):
                        st.image(message["image"])
                    else:
                        st.image(message["image"])
        else:
            # Use default avatar if character image doesn't exist
            avatar_path = config.DEFAULT_AVATAR
            if "character_type" in message:
                char_config = config.CHARACTERS.get(message["character_type"])
                if char_config and os.path.exists(char_config["image"]):
                    avatar_path = char_config["image"]
            
            with st.chat_message(message["role"], avatar=avatar_path):
                formatted_response = utils.format_character_response(
                    message.get("character_type", "Assistant"),
                    message["content"]
                )
                st.markdown(f'<div style="color: {message["color"]}; padding: 0.5rem 0;">{formatted_response}</div>', 
                          unsafe_allow_html=True)

    # Chat input
    if st.session_state.environment:
        # Image upload
        uploaded_image = st.file_uploader("Upload an image for characters to analyze", 
                                        type=['png', 'jpg', 'jpeg'])
        image_path, base64_image = save_uploaded_image(uploaded_image) if uploaded_image else (None, None)

        # Text input
        user_input = st.chat_input("Type your message here...")
        
        if user_input or image_path:
            # Add user message to chat history
            user_message = {"role": "user", "content": user_input or ""}
            if base64_image:
                user_message["image"] = f"data:image/{utils.get_file_extension(uploaded_image.name)[1:]};base64,{base64_image}"
            st.session_state.chat_history.append(user_message)

            # Get responses from characters
            responses = st.session_state.environment.process_message(
                message=user_input,
                openai_client=client,
                temperature=st.session_state.temperature,
                image_path=image_path
            )
            
            # Add responses to chat history
            for response in responses:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["response"],
                    "color": response["color"],
                    "character_type": response["agent"]
                })

            # Force a rerun to update the chat display
            st.rerun()
    else:
        st.info("Please select at least one character from the sidebar to start the conversation.")

if __name__ == "__main__":
    main()
