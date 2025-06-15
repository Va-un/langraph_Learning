# README

## Project Overview

This repository contains several Python projects and utilities demonstrating the use of LangGraph and LangChain for building agent workflows, document processing, code execution, and interactive tools. Each script showcases a unique application, such as code drafting, document updating, RAG-based document Q&A, and simple games, all orchestrated using stateful graphs and tool integrations.

---

## Table of Contents

- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [1. LangGraph.ipynb](#1-langgraphipynb)
  - [2. Mailer.py](#2-mailerpy)
  - [3. Project.py](#3-projectpy)
  - [4. RAG.py](#4-ragpy)
  - [5. Roullete.py](#5-roulletepy)
- [Prompts Module](#prompts-module)
- [Key Features](#key-features)
- [Contributing](#contributing)
- [License](#license)

---

## Requirements

- Python 3.8+
- pip (Python package installer)

**Python Libraries:**

- langgraph
- langchain-core
- langchain-openai or langchain-google-genai
- chroma
- python-dotenv
- IPython (for notebook visualization)
- Other dependencies as needed for document loaders and text splitters

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Project Structure

| File/Folder     | Description                                                    |
|-----------------|----------------------------------------------------------------|
| LangGraph.ipynb | Jupyter notebook with basic and advanced LangGraph examples    |
| Mailer.py       | Interactive document editing and saving agent                  |
| Project.py      | Code drafting, execution, and file saving agent               |
| RAG.py          | Retrieval-Augmented Generation (RAG) Q&A over PDF documents   |
| Roullete.py     | Simple number guessing game using LangGraph                   |
| prompts.py      | Prompt templates for system and agent instructions            |

---

## Usage

### 1. LangGraph.ipynb

- Demonstrates type-safe state management, graph nodes, and agent workflows using LangGraph.
- Includes examples for:
  - TypedDict and Union usage
  - Building simple and sequential state graphs
  - Visualizing graphs using Mermaid diagrams
- To run: Open in Jupyter Notebook and execute cells sequentially[1].

### 2. Mailer.py

- An interactive agent for updating, modifying, and saving document content.
- Features:
  - `update` tool: Replace document content.
  - `save` tool: Save content to a text file.
  - Conversational interface for iterative document editing.
- To run:  
  ```bash
  python Mailer.py
  ```
  Follow on-screen prompts to update and save documents[2].

### 3. Project.py

- A code drafting and execution assistant.
- Features:
  - Accepts user instructions, drafts code, executes it, and updates as needed.
  - Uses tools for code execution and file saving.
  - Conditional graph transitions for code correction and saving.
- To run:
  ```bash
  python Project.py
  ```
  Interact via command line to draft and save Python code[3].

### 4. RAG.py

- Retrieval-Augmented Generation agent for answering questions about PDF documents.
- Features:
  - Loads and splits PDF documents.
  - Embeds and stores document chunks in a vector database.
  - Uses a retriever tool for semantic search and Q&A.
- To run:
  - Place your PDF (e.g., "Tender.pdf") in the working directory.
  - Update API keys as needed.
  - Run:
    ```bash
    python RAG.py
    ```
  Ask questions about the PDF content interactively[4].

### 5. Roullete.py

- A simple number guessing game implemented as a LangGraph agent.
- Features:
  - Randomly selects a number.
  - Prompts user to guess until correct.
  - Tracks attempts and provides hints.
- To run:
  ```bash
  python Roullete.py
  ```
  Follow the prompts to play the game[5].

---

## Prompts Module

- `prompts.py` contains reusable prompt templates for:
  - Coding assistant
  - Update and change detection
  - File saving confirmation
- These prompts are imported and used in the agent scripts for consistent behavior[6].

---

## Key Features

- **Type Safety and Readability**: Uses Python type hints and TypedDict for clear state management[1].
- **Interactive Agents**: Each script uses conversational prompts for user interaction.
- **Graph-Based Workflow**: LangGraph enables visual and logical orchestration of agent states and transitions.
- **Tool Integration**: Custom tools for code execution, document update, file saving, and retrieval.
- **Extensibility**: Modular design allows easy addition of new tools, prompts, and agent behaviors.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

---

## License

This project is provided for educational and demonstration purposes. Please refer to the LICENSE file for details.

---

**Contact:**  
For queries or suggestions, open an issue or contact the maintainer.

---

**Note:**  
- Ensure API keys are set in your environment for any scripts using external LLMs or embeddings.
- For any tool or script, refer to inline comments for specific usage instructions and customization.

