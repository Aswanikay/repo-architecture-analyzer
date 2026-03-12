
import os
from openai import OpenAI
import gradio as gradio

def get_client() -> OpenAI:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    return OpenAI(base_url=base_url, api_key="ollama")  # key is ignored by Ollama

def get_system_prompt() -> str:
    return """
                You are a senior software architect helping a new developer understand an unfamiliar GitHub repository.

                Your task is to analyze the repository and produce a structured onboarding guide for a junior developer. Respond ONLY in well-formatted Markdown.

                Include the following sections:

                1. Repository Overview
                - Brief summary of what the project does.

                2. Tech Stack
                - List languages, frameworks, libraries, infrastructure tools.

                3. High-Level Architecture
                - Explain how the system is structured and how major components interact.

                4. Architecture Diagram
                - Provide a simple architecture diagram using Mermaid syntax.

                5. Folder / Module Structure
                - Explain important folders and modules in the repository.

                6. Key Features
                - Describe the main functionality of the project.

                7. How to Run Locally
                - Provide step-by-step instructions for running the project.

                8. Debugging Tips
                - Explain common debugging approaches and useful logs.

                9. Developer Onboarding Tips along with dependencies of the project
                - Explain what a new developer should read first and how to start contributing.

                Additional instructions:
                - Use concise, technical explanations suitable for engineers.
                - Avoid filler text or unnecessary commentary.
                - If repository details are incomplete, infer likely architecture patterns based on common practices and clearly state assumptions.
                - Provide the architecture diagram in **Mermaid flowchart syntax** so it can be rendered automatically.
                - Do not synthesize any information, only provide the information that is provided or can be infered in the repository.
                """


def stream_architecture_analysis(message, history) -> str:
    if not message:
        return  ""# or: yield "" and return
    system_message = get_system_prompt()
    user_message = "Hi there. Please analyze the architecture of the following GitHub repository and create an onboarding guide for a new developer. Repository URL:" + message


    stream = get_client().chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}],
        stream=True
    )

    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def main():
    ##repo_url = gradio.Textbox(label="Repository URL")
    gradio.ChatInterface(fn=stream_architecture_analysis).launch()

if __name__ == "__main__":
    main()