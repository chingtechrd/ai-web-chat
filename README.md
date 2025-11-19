# AI Web Chat

A local web chat application powered by a Python FastAPI backend and the Gemini CLI. This project allows you to chat with an AI agent in a modern web interface, featuring multi-turn conversation capabilities.

## Features

- **FastAPI Backend**: Robust and fast Python backend serving the application.
- **Gemini CLI Integration**: Utilizes the `gemini` CLI for intelligent responses.
- **Multi-turn Conversations**: Supports maintaining context across multiple exchanges using session management.
- **Modern UI**: Clean and responsive HTML/CSS/JS frontend.
- **Streaming-like Experience**: Visual feedback while the AI is processing.

## Prerequisites

- **Python 3.10+**
- **Gemini CLI**: Ensure the `gemini` command-line tool is installed and authenticated.
- **uv** (Optional but recommended): For fast Python package management.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai-web-chat
    ```

2.  **Install dependencies:**

    Using `uv` (recommended):
    ```bash
    uv sync
    ```

    Or using standard `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, install directly: `pip install fastapi uvicorn`)*

## Usage

1.  **Start the server:**
    ```bash
    uv run main.py
    ```
    Or with python directly:
    ```bash
    python main.py
    ```
    The server will start at `http://127.0.0.1:8000`.

2.  **Access the Chat:**
    Open your browser and navigate to:
    [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)

3.  **Start Chatting:**
    Type your message in the input box and hit Send. The AI will respond, remembering the context of your conversation.

## Project Structure

- `main.py`: The FastAPI application entry point. Handles chat endpoints and invokes the Gemini CLI.
- `static/`: Contains the frontend assets (`index.html`, `style.css`, `script.js`).
- `pyproject.toml`: Project configuration and dependencies.
