#!/usr/bin/env python3
"""
Setup script for API key configuration
"""

import os
from pathlib import Path

def setup_api_keys():
    """Setup API keys for the AI Character Toolkit"""
    print("AI Character Toolkit - API Key Setup")
    print("=" * 40)

    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("""# AI Character Toolkit Environment Variables

# Choose your AI provider: openai, claude, or zhipu
AI_PROVIDER=zhipu

# OpenAI Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Claude Configuration
# Get your API key from: https://console.anthropic.com/
CLAUDE_API_KEY=your_claude_api_key_here

# ZhipuAI Configuration
# Get your API key from: https://bigmodel.cn
ZHIPU_API_KEY=your_zhipu_api_key_here

# Optional: Log file path
# LOG_FILE=./logs/ai_toolkit.log
""")

    print("Please choose your AI provider:")
    print("1. OpenAI (GPT-4)")
    print("2. Claude (Anthropic)")
    print("3. ZhipuAI (智谱)")
    print("4. Multiple providers")

    choice = input("Enter your choice (1-4): ").strip()

    provider = ""
    if choice == "1":
        provider = "openai"
    elif choice == "2":
        provider = "claude"
    elif choice == "3":
        provider = "zhipu"
    elif choice == "4":
        provider = "openai"
        print("Note: You'll need to configure all selected providers")
    else:
        print("Invalid choice. Defaulting to ZhipuAI")
        provider = "zhipu"

    # Read current .env content
    with open(env_file, 'r') as f:
        content = f.read()

    # Update provider
    content = content.replace("AI_PROVIDER=openai", f"AI_PROVIDER={provider}")

    # Get API key(s)
    if choice in ["1", "4"]:
        openai_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
        if openai_key:
            content = content.replace("OPENAI_API_KEY=your_openai_api_key_here",
                                   f"OPENAI_API_KEY={openai_key}")

    if choice in ["2", "4"]:
        claude_key = input("Enter your Claude API key (or press Enter to skip): ").strip()
        if claude_key:
            content = content.replace("CLAUDE_API_KEY=your_claude_api_key_here",
                                   f"CLAUDE_API_KEY={claude_key}")

    if choice in ["3", "4"]:
        zhipu_key = input("Enter your ZhipuAI API key (or press Enter to skip): ").strip()
        if zhipu_key:
            content = content.replace("ZHIPU_API_KEY=your_zhipu_api_key_here",
                                   f"ZHIPU_API_KEY={zhipu_key}")

    # Write updated content
    with open(env_file, 'w') as f:
        f.write(content)

    print(f"\nConfiguration updated!")
    print(f"AI Provider set to: {provider}")

    # Verify setup
    from dotenv import load_dotenv
    load_dotenv()

    if provider == "openai" and os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here':
        print("OpenAI API key configured successfully")
    elif provider == "claude" and os.getenv('CLAUDE_API_KEY') and os.getenv('CLAUDE_API_KEY') != 'your_claude_api_key_here':
        print("Claude API key configured successfully")
    elif provider == "zhipu" and os.getenv('ZHIPU_API_KEY') and os.getenv('ZHIPU_API_KEY') != 'your_zhipu_api_key_here':
        print("ZhipuAI API key configured successfully")

    print("\nSetup complete! You can now run the AI Character Toolkit.")

if __name__ == "__main__":
    setup_api_keys()