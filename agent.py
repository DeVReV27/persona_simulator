"""
Local implementation of agent functionality inspired by TinyTroupe.
Simplified for our persona simulator needs.
"""
import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Agent:
    """A simulated persona that can interact and respond to messages."""
    
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        self.memory = []
        self.context = []
        self.accessible_agents = []
        
    def define(self, key, value):
        """Define a configuration value for the agent."""
        self.config[key] = value
        
    def define_several(self, key, values):
        """Define multiple values for a configuration key."""
        if key not in self.config:
            self.config[key] = []
        self.config[key].extend(values)

    def listen(self, message, source=None):
        """Process an incoming message."""
        self.memory.append({
            'type': 'input',
            'content': message,
            'source': source,
            'timestamp': datetime.now().isoformat()
        })
        
    def see(self, image_description, source=None):
        """Process a visual input."""
        self.memory.append({
            'type': 'visual',
            'content': image_description,
            'source': source,
            'timestamp': datetime.now().isoformat()
        })

    def think(self, thought):
        """Record an internal thought."""
        self.memory.append({
            'type': 'thought',
            'content': thought,
            'timestamp': datetime.now().isoformat()
        })

    def change_context(self, context):
        """Update the agent's context."""
        self.context = context
        self.think(f"Understanding new context: {' '.join(context)}")

    def make_agent_accessible(self, agent):
        """Make another agent accessible for interaction."""
        if agent not in self.accessible_agents:
            self.accessible_agents.append(agent)

    def get_prompt(self):
        """Generate the complete prompt for the agent."""
        prompt = f"""You are {self.name}, with the following characteristics:

Age: {self.config.get('age')}
Nationality: {self.config.get('nationality')}
Occupation: {self.config.get('occupation')}

Personality traits:
"""
        for trait in self.config.get('personality_traits', []):
            prompt += f"- {trait['trait']}\n"

        # Add current context
        if self.context:
            prompt += "\nCurrent context and environment:\n"
            for ctx in self.context:
                prompt += f"- {ctx}\n"

        # Add information about other participants
        if self.accessible_agents:
            prompt += "\nOther participants in the conversation:\n"
            for agent in self.accessible_agents:
                prompt += f"- {agent.name} ({agent.config.get('occupation')})\n"

        prompt += """
Instructions:
1. Always stay in character, maintaining your personality traits and perspective
2. Consider the current context and environment in your responses
3. Interact naturally with other participants while staying true to your character
4. Express your unique viewpoint based on your background and expertise
5. If analyzing images, do so from your character's perspective

Please respond in character, maintaining these traits and characteristics.
"""
        return prompt

    def get_recent_memory(self, limit=5):
        """Get recent memory entries."""
        return self.memory[-limit:] if self.memory else []

    def generate_response(self, openai_client, temperature=0.7):
        """Generate a response using OpenAI."""
        messages = [{"role": "system", "content": self.get_prompt()}]
        
        # Add recent memory for context
        for mem in self.get_recent_memory():
            if mem['type'] == 'input':
                messages.append({
                    "role": "user",
                    "content": mem['content']
                })
            elif mem['type'] == 'visual':
                messages.append({
                    "role": "user",
                    "content": f"[Observing an image: {mem['content']}]"
                })
            elif mem['type'] == 'thought':
                messages.append({
                    "role": "assistant",
                    "content": f"[Internal thought: {mem['content']}]"
                })

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I am unable to respond at the moment."
