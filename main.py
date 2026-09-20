import os
import certifi
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# ======================================================
# LOAD ENV VARIABLES
# ======================================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ======================================================
# TOOLS
# ======================================================
search_tool = TavilySearchResults(max_results=5)

@tool 
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a specified city."""
    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )
    
    response = requests.get(url)
    data = response.json()
    
    if "current" not in data:
        return f"Không thể lấy dữ liệu thời tiết cho thành phố {city}"
    
    return (
        f"Thành phố: {city}\n"
        f"Nhiệt độ: {data['current']['temperature']}°C\n"
        f"Tình trạng thời tiết: {data['current']['weather_descriptions'][0]}\n"
        f"Độ ẩm: {data['current']['humidity']}%"
    )

tools = [search_tool, get_weather_data]

# ======================================================
# LLM & AGENT SETUP
# ======================================================
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY
)

from datetime import datetime

# Lấy thời gian thực tế từ hệ thống máy tính
current_date = datetime.now().strftime("%d/%m/%Y")
current_year = datetime.now().year

custom_prompt = (
    f"Hôm nay là ngày {current_date}, năm hiện tại là {current_year}. "
    "Bạn là một trợ lý ảo thông minh. "
    "Khi người dùng hỏi về tin tức, kết quả bóng đá, sự kiện gần đây hoặc thời tiết, "
    "hãy luôn sử dụng các công cụ được cung cấp và ưu tiên kết quả mới nhất theo mốc thời gian hiện tại. "
    "Luôn trả lời bằng tiếng Việt một cách lịch sự, tự nhiên."
)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=custom_prompt
)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=custom_prompt
)

# ======================================================
# processing and cleaning
# ======================================================
def ask_agent(query: str) -> str:
    """Gửi câu hỏi vào Agent và bóc tách lấy nội dung chữ sạch sẽ."""
    response = agent.invoke({
        "messages": [("user", query)]
    })
    
    raw_content = response["messages"][-1].content
    
    # Bóc tách trường 'text' nếu model trả về list các dictionary kèm signature
    if isinstance(raw_content, list) and len(raw_content) > 0:
        first_item = raw_content[0]
        if isinstance(first_item, dict) and "text" in first_item:
            return first_item["text"].strip()
        return str(first_item).strip()
    
    return str(raw_content).strip()