import streamlit as st
from main import ask_agent

# Thiết lập thông tin trang
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Agentic AI Assistant")
st.caption("Search + Weather AI Agent using LangChain")

# Khởi tạo lịch sử hội thoại trong session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các tin nhắn trước đó
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Khung nhập câu hỏi
if user_query := st.chat_input("Hỏi tôi về thời tiết hoặc tin tức (ví dụ: thời tiết Hà Tĩnh hôm nay)..."):
    # 1. Lưu và hiển thị câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. Gọi Agent xử lý và hiển thị câu trả lời
    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu thông tin..."):
            try:
                answer = ask_agent(user_query)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Đã xảy ra lỗi: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})