
# Stock Market Chatbot

This project is a chatbot application that answers questions related to the stock market using a large language model (LLM) from HuggingFace.

## Project Structure
```
.
├── app.py
├── requirements.txt
├── .env-example
├── README.md
└── Prompt Engineering Report.pdf
```

## Requirements
- Python 3.8+
- A HuggingFace API token

## Setup

1. **Create a virtual environment:**

   On Windows:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```

   On MacOS:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Create a .env file:**

   Create a `.env` file like `.env-example` in the root directory of the project.  
   Add your HuggingFace API token to the `.env` file:
   ```sh
   API_TOKEN=your_huggingface_api_token
   ```

## Usage

Run the Streamlit application:
```sh
streamlit run app.py
```

## Project Features

- **Stock Market Information:** The chatbot is designed to answer stock and stock market-related questions.
- **Greeting Capability:** The chatbot can recognize and respond to greetings appropriately.
- **Restricted Topics:** The chatbot will respond with "I can only chat about stock markets." if the input is unrelated to the stock market.

## Notes

- The chatbot uses the `mistralai/Mistral-7B-v0.1` model from HuggingFace for embedding and prompting operations.
- The project leverages the Streamlit framework to create a chat window interface.
