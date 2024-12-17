# Persona Simulator

A Streamlit application that simulates conversations with different personas using TinyTroupe and OpenAI's GPT-4 Vision model. This application allows users to interact with various AI personas, each with unique personalities and expertise.

## Features

- Multiple predefined personas (Savvy Customer, Critic, Psychologist, etc.)
- Real-time chat interface with multiple personas simultaneously
- Image analysis capabilities using GPT-4 Vision
- Adjustable LLM temperature for response variation
- Save and load chat histories
- Custom environment/context setting
- Color-coded responses for each persona

## Prerequisites

- macOS
- Python 3.10 or higher
- OpenAI API key
- TinyTroupe library
- Streamlit

## Quick Installation (macOS)

1. Clone this repository:
```bash
git clone <repository-url>
cd persona_simulator
```

2. Run the setup script:
```bash
./setup.sh
```

The setup script will:
- Create a Python virtual environment
- Install all required dependencies
- Create a .env file from template
- Run setup verification tests

3. Add your OpenAI API key to the .env file:
```bash
nano .env
# or
open -e .env
```

## Manual Installation (if needed)

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a .env file and add your OpenAI API key:
```bash
cp .env.template .env
nano .env  # or use any text editor
```

## Usage

1. Activate the virtual environment (if not already activated):
```bash
source venv/bin/activate
```

2. Start the Streamlit application:
```bash
streamlit run app.py
```

3. In the sidebar:
   - Select one or more personas to chat with
   - Adjust the LLM temperature as needed
   - Describe the environment/context for the conversation
   - Save or load chat histories

4. In the main chat interface:
   - Type messages to interact with the selected personas
   - Upload images for the personas to analyze
   - View color-coded responses from each persona

## Available Personas

- **Savvy Customer**: A tech-savvy consumer who provides informed product feedback
- **Critic**: A professional critic with high standards and detailed assessments
- **Top Psychologist**: An empathetic analyst providing behavioral insights
- **Top Marketer**: A strategic thinker focused on market trends and opportunities
- **Masterful CEO**: A decisive leader with extensive business acumen
- **Public Relations Expert**: A diplomatic professional skilled in perception management
- **Top Salesman**: A charismatic relationship builder focused on customer needs

## Environment Description

Use the environment description to set the context for the conversation. This helps the personas understand the situation and provide more relevant responses. For example:

- "A product launch meeting for a new smartphone"
- "A focus group discussion about a marketing campaign"
- "A therapy session discussing work-life balance"

## Saving and Loading Chats

- Click "Save Chat History" to save the current conversation
- Use "Load Chat History" to upload and continue a previous conversation
- Chat histories are stored in JSON format in the `chat_histories` folder

## Troubleshooting

If you encounter any issues:

1. Verify your Python version:
```bash
python3 --version  # Should be 3.10 or higher
```

2. Check if all dependencies are installed:
```bash
python3 test_setup.py
```

3. Verify your OpenAI API key:
```bash
cat .env  # Should show your API key
```

4. Check Streamlit is running:
```bash
which streamlit  # Should show path to streamlit in venv
```

## Notes

- The application uses GPT-4 Vision for image analysis, ensuring high-quality visual understanding
- Each persona maintains consistent personality traits throughout the conversation
- Adjust the temperature slider to control response variability (lower for more focused responses, higher for more creative ones)
- The application automatically creates necessary folders for storing chat histories

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
