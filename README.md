# repo-architecture-analyzer
Analyze any GitHub repository with AI. Fetches repo files and uses an LLM to generate architecture summaries, tech stack insights, and module explanations to help developers understand codebases faster.



1. Install ollama
2. ollama run llama3.2:1b

Executing it:

# create a virtual environment (once)
python3 -m venv .venv

# activate it (every new terminal)
source .venv/bin/activate

# now pip is safe to use inside this venv
python -m pip install openai ollama gradio
python main.py