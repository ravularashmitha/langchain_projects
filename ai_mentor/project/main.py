import streamlit as st
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="AI Chatbot Mentor",
    page_icon="🤖",
    layout="centered"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

MODULES = [
    "Python",
    "SQL / MySQL",
    "Power BI",
    "Exploratory Data Analysis (EDA)",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Agentic AI"
]

# ================= SESSION MEMORY =================
if "module" not in st.session_state:
    st.session_state.module = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# ================= PROMPT TEMPLATE =================
prompt_template = PromptTemplate(
    input_variables=["module", "question"],
    template="""
You are an expert AI mentor ONLY for the domain: {module}.

RULE:
- Answer ONLY questions related to {module}.
- If the question is NOT related, reply EXACTLY:
"Sorry, I don’t know about this question. Please ask something related to the selected module."

Question:
{question}

Answer clearly and educationally:
"""
)

# ================= UI =================
st.title("🤖 AI Chatbot Mentor")

# ---------- MODULE SELECTION ----------
if st.session_state.module is None:
    st.markdown("""
👋 **Welcome to AI Chatbot Mentor**  
Select a learning module to begin.
""")

    module = st.selectbox("📌 Select Module", ["-- Select --"] + MODULES)

    if module != "-- Select --":
        st.session_state.module = module
        st.rerun()

# ---------- CHAT ----------
else:
    module = st.session_state.module
    st.success(f"🎯 {module} AI Mentor")
    st.caption("Ask questions. Type **bye** to end.")

    # Show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask your question")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.write(user_input)

        if user_input.lower().strip() in ["bye", "exit", "quit", "end"]:
            farewell = "👋 Session ended. Download your chat below."
            st.session_state.messages.append(
                {"role": "assistant", "content": farewell}
            )
            with st.chat_message("assistant"):
                st.write(farewell)

            st.session_state.show_download = True

        else:
            prompt = prompt_template.format(
                module=module,
                question=user_input
            )

            try:
                response = llm.invoke(prompt)
                answer = response.content
            except Exception as e:
                answer = "Gemini API error. Check API key or quota."

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            with st.chat_message("assistant"):
                st.write(answer)

    # ---------- DOWNLOAD ----------
    if st.session_state.show_download:
        chat_text = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages
        )

        st.download_button(
            "📥 Download Conversation",
            chat_text,
            file_name=f"{module}_chat.txt",
            mime="text/plain"
        )

    # ---------- RESET ----------
    if st.button("🔄 Change Module"):
        st.session_state.clear()
        st.rerun()