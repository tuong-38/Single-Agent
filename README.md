🤖 Agentic AI Assistant

A full-stack, conversational Agentic AI system built with LangChain, LangGraph, Google Gemini, and Streamlit. The assistant dynamically plans actions and uses real-time external tools to fetch live weather data and browse recent web updates.

🌟 Key Features

ReAct Agent Architecture: Employs reasoning and acting loops (via LangGraph) to determine when and how to call tools.

Dynamic Temporal Context: Injects current system datetime into the prompt to guarantee temporal awareness (e.g., handling recent events and current year queries).

Tool Integration:

🌦️ WeatherStack API: Real-time city-level weather reports (temperature, weather status, humidity).

🔍 Tavily Search: Fast, developer-focused search engine for current events, news, and sports scores.

Sanitized Presentation: Automatically extracts plain text output and strips out metadata or cryptographic signatures.

Interactive Web Interface: Streamlit chat interface supporting session conversation history.

🏗️ Project Architecture

Single-Agent/
├── app.py              # Streamlit UI frontend & message history loop
├── main.py             # LangChain/LangGraph agent definition & tools
├── requirements.txt    # Project dependencies
├── .gitignore          # Excluded files (.env, pycache, etc.)
└── README.md           # Documentation


🚀 Getting Started

1. Clone & Setup Environment

git clone https://github.com/tuong-38/Single-Agent.git
cd Single-Agent

# Create & activate a virtual environment (Conda or venv)
conda create -n langagent python=3.11 -y
conda activate langagent


2. Install Dependencies

pip install -r requirements.txt


3. Configure Environment Variables

Create a .env file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
TAVILY_API_KEY=your_tavily_api_key


4. Run Locally

python -m streamlit run app.py


🌐 Cloud Deployment (Render)

This project is configured to run on Render as a Web Service:

Environment: Python 3

Build Command: pip install -r requirements.txt

Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0

Environment Variables: Set GOOGLE_API_KEY, WEATHERSTACK_API_KEY, and TAVILY_API_KEY in the Render dashboard.

🛠️ Built With

LangChain & LangGraph

Google Gemini Flash

Streamlit

Tavily Search

WeatherStack API