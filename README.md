# My Rasa Chatbot

A conversational AI chatbot built with the Rasa framework. This project demonstrates the core capabilities of a virtual assistant, including natural language understanding (NLU) and dialogue management.
I used it on a scraped data about real estate to help the user find what he's looking for easier and quicker.

## ✨ Features

- **Natural Language Understanding**: Recognizes user intents and extracts key information (entities).
- **Dialogue Management**: Handles multi-turn conversations through stories and rules.
- **Custom Actions**: Integrates with external database for dynamic responses (via `actions.py`).

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or 3.9  (!)
- pip (Python package manager)

### Installation & Running

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment** ( Recommended !!!)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *If you don't have a `requirements.txt`, install Rasa directly:*
    ```bash
    pip install rasa
    ```

4.  **Train the model**
    ```bash
    rasa train
    ```

5.  **Talk to the chatbot**
    ```bash
    rasa shell
    ```
6.  **Interactive learning (Recommended for development)**
    ```bash
    rasa interactive
    ```
    *This mode allows you to chat with your bot, correct its mistakes, and automatically add new training examples -> very useful to get more precise answers*

## 📁 Project Structure

```
├── .rasa/ # Contains temporary conversation data and logs
├── actions/
│ ├── init.py
│ └── actions.py # Code for custom actions
├── data/ # Directory for training data (nlu.yml, stories.yml)
├── models/ # Contains trained model binaries (gitignored)
├── tests/ # Directory for test stories and NLU data
├── .gitignore # Specifies files to be ignored by git
├── config.yml # Model configuration (pipeline & policies)
├── credentials.yml # Setup for connecting to channels (e.g., Slack)
├── database.db # SQLite database file (if used for tracking)
├── domain.yml # Bot's universe: intents, responses, entities
├── endpoints.yml # Configuration for the action server and tracker store
└── story_graph.dot # Visualization of conversation paths (auto-generated)

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.
