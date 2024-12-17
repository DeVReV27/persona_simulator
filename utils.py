"""Helper functions for the persona simulator."""
import json
import base64
from datetime import datetime
from agent import Agent

def create_character(character_config):
    """Create an Agent instance from character configuration."""
    person = Agent(character_config["name"], character_config)
    return person

def save_chat_history(chat_history, filename):
    """Save chat history to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(chat_history, f)

def load_chat_history(filename):
    """Load chat history from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def create_chat_folder():
    """Create a folder to store chat histories if it doesn't exist."""
    import os
    if not os.path.exists("chat_histories"):
        os.makedirs("chat_histories")

def image_to_base64(image_path):
    """Convert image to base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

def get_file_extension(filename):
    """Get file extension from filename."""
    import os
    return os.path.splitext(filename)[1].lower()

def is_valid_image(file_extension):
    """Check if file extension is a valid image type."""
    return file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']

def format_character_response(character_type, response):
    """Format the character's response with their type prefix."""
    return f"{character_type}: {response}"

def load_image_url(url):
    """Load image from URL and convert to base64."""
    import requests
    try:
        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except Exception as e:
        print(f"Error loading image from URL: {e}")
        return None

def get_character_image(character_config):
    """Get character image as base64 string."""
    if 'image' in character_config:
        if character_config['image'].startswith('http'):
            return load_image_url(character_config['image'])
        else:
            return image_to_base64(character_config['image'])
    return None

class ChatEnvironment:
    """Custom environment for chat interactions."""
    
    def __init__(self, name="Chat Environment", agents=None, description=""):
        self.name = name
        self.agents = agents or []
        self.description = description
        self.current_datetime = datetime.now()
        self.make_everyone_accessible()
        
        # Set initial context if provided
        if description:
            self.broadcast_context(description)
            
    def add_agent(self, agent):
        """Add an agent to the environment."""
        if agent not in self.agents:
            self.agents.append(agent)
            
    def remove_agent(self, agent):
        """Remove an agent from the environment."""
        if agent in self.agents:
            self.agents.remove(agent)
            
    def broadcast_context(self, context):
        """Update context for all agents."""
        self.description = context
        for agent in self.agents:
            agent.change_context([
                f"Current environment/context: {context}",
                "Consider this context in all your responses and interactions.",
                f"You are participating in a conversation with {len(self.agents)} other characters.",
                "Maintain your character's personality and perspective while engaging with others."
            ])

    def make_everyone_accessible(self):
        """Make all agents accessible to each other."""
        for agent in self.agents:
            for other_agent in self.agents:
                if agent != other_agent:
                    agent.make_agent_accessible(other_agent)

    def process_message(self, message, openai_client, temperature=0.7, image_path=None):
        """Process a message and get responses from all agents."""
        responses = []
        
        context_prefix = ""
        if self.description:
            context_prefix = f"[Context: {self.description}] "
        
        for agent in self.agents:
            if image_path:
                agent.see(f"An image was shared: {image_path}")
            
            # Add context to the message if available
            full_message = context_prefix + (message or "")
            agent.listen(full_message)
            
            response = agent.generate_response(openai_client, temperature)
            if response:
                responses.append({
                    "agent": agent.name,
                    "response": response,
                    "color": agent.config.get("color", "#000000")
                })
                
        return responses
