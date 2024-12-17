"""
Test script to verify the setup of the Persona Simulator application.
Run this script to check if all dependencies are installed and configurations are correct.
"""

import os
import sys
import importlib.util

def check_module(module_name):
    """Check if a Python module is installed."""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {module_name} is NOT installed")
        return False
    print(f"✓ {module_name} is installed")
    return True

def check_file(filepath, required=True):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    if exists:
        print(f"✓ {filepath} exists")
    else:
        if required:
            print(f"❌ {filepath} is missing")
        else:
            print(f"! {filepath} is not present (optional)")
    return exists

def main():
    print("\n=== Persona Simulator Setup Check ===\n")

    # Check required Python modules
    print("Checking required Python modules...")
    modules = ['streamlit', 'openai', 'python-dotenv', 'tinytroupe', 'PIL']
    all_modules_present = all(check_module(module) for module in modules)

    print("\nChecking application files...")
    required_files = [
        'requirements.txt',
        'config.py',
        'utils.py',
        'app.py',
        'README.md',
        '.gitignore',
        '.env.template'
    ]
    all_files_present = all(check_file(f) for f in required_files)

    # Check optional files
    print("\nChecking optional files...")
    check_file('.env', required=False)
    
    # Check directories
    print("\nChecking directories...")
    if not os.path.exists('chat_histories'):
        os.makedirs('chat_histories')
        print("✓ Created chat_histories directory")
    else:
        print("✓ chat_histories directory exists")

    # Overall status
    print("\n=== Setup Status ===")
    if all_modules_present and all_files_present:
        print("✓ All required components are present!")
        if not os.path.exists('.env'):
            print("\nNext steps:")
            print("1. Create a .env file from .env.template")
            print("2. Add your OpenAI API key to the .env file")
            print("3. Run the application with: streamlit run app.py")
    else:
        print("❌ Some components are missing. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
