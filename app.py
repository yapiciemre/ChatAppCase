import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class StockMarketChatbot:
    # HuggingFace API URL and Headers
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
    HEADERS = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}

    def __init__(self):
        # Initialize chat history
        self.chat_history = []

    @staticmethod
    def query_huggingface(prompt):
        """Queries the HuggingFace model with the provided prompt."""
        try:
            response = requests.post(StockMarketChatbot.API_URL, headers=StockMarketChatbot.HEADERS, json={"inputs": prompt})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return None

    @staticmethod
    def is_stock_related(text):
        """Checks if the user input is related to stock market topics."""
        stock_keywords = [
            "stock", "market", "share", "investment", "portfolio", "exchange", 
            "trading", "equities", "securities", "dividend", "IPO", 
            "ETF", "mutual fund", "hedge fund", "index fund", "blue chip", 
            "penny stock", "bull market", "bear market", "nasdaq", "dow jones", 
            "S&P 500", "NYSE", "brokerage", "capital gain", "bond", "asset", 
            "equity", "financial statement", "earnings report", "valuation", 
            "price to earnings ratio", "market cap", "investment strategy",
            "buy", "sell", "trade", "hold", "long position", "short position", 
            "diversification", "risk management"
        ]
        return any(keyword in text.lower() for keyword in stock_keywords)

    def get_response(self, user_input):
        """Generates a response based on user input."""
        if not user_input.strip():
            return "Please enter a message."

        greeting_keywords = [
            "hello", "hi", "hey", "greetings", "good morning", "good afternoon", 
            "good evening", "howdy", "good day"
        ]

        if any(keyword in user_input.lower() for keyword in greeting_keywords):
            return "Hello! How can I assist you with stock market information today?"

        if StockMarketChatbot.is_stock_related(user_input):
            query_text = f"My short, relevant and concise answer to your {user_input} question regarding stock market information:" + '\n' 
            response = StockMarketChatbot.query_huggingface(query_text)
            if response and "generated_text" in response[0]:
                generated_text = response[0]["generated_text"]
                # Ensure the response is concise and relevant
                sentences = generated_text.split('. ')
                limited_response = '. '.join(sentences[:3]) + '.'
                return limited_response
            else:
                return "Failed to get a response from the AI."
        else:
            return "I can only chat about stock markets."

    def display_chat(self):
        """Displays the chat history."""
        for chat in self.chat_history:
            if chat["role"] == "user":
                st.write(f"**You:** {chat['text']}")
            else:
                st.write(f"**Bot:** {chat['text']}")

    def send_message(self, user_input):
        """Sends the message and updates chat history."""
        user_input = user_input.strip()
        if user_input:
            self.chat_history.append({"role": "user", "text": user_input})
            with st.spinner("Thinking..."):
                response = self.get_response(user_input)
                self.chat_history.append({"role": "bot", "text": response})
            return ""  # Clear input box
        return user_input

def main():
    """Main function to run the Streamlit app."""
    # Set Streamlit page configuration
    st.set_page_config(page_title="Stock Market Chatbot", page_icon=":chart_with_upwards_trend:", layout="centered")
    st.title("📈 Stock Market Chatbot")
    st.write("### Ask me anything about stock markets!")

    # Initialize the chatbot instance
    chatbot = StockMarketChatbot()

    # Maintain chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "input_box" not in st.session_state:
        st.session_state.input_box = ""

    chatbot.chat_history = st.session_state.chat_history

    # Input box for user message
    user_input = st.text_input("You: ", st.session_state.input_box, placeholder="Enter your question about the stock market here...", key="input_box", on_change=lambda: send_user_message(chatbot))

    # Display chat history
    chatbot.display_chat()
    st.session_state.chat_history = chatbot.chat_history

def send_user_message(chatbot):
    """Handles sending user message and updating session state."""
    user_input = st.session_state.input_box
    st.session_state.input_box = chatbot.send_message(user_input)

if __name__ == "__main__":
    main()