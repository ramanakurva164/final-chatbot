import streamlit as st
import requests
import os

# ✅ Configure Streamlit page
st.set_page_config(page_title="Agent Ramana (Mistral API)", page_icon="🤖", layout="wide")

# ✅ Get HF token
hf_token = os.getenv("HF_TOKEN", st.secrets.get("HF_TOKEN"))
if not hf_token:
    st.error("❌ Please set your Hugging Face token as HF_TOKEN in Streamlit secrets or as an environment variable.")
    st.stop()

# ✅ API URL for Hugging Face Inference
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {hf_token}"}

def query_mistral(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "temperature": 0.75, "top_p": 0.95}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return f"❌ Error: {response.status_code} - {response.text}"
    data = response.json()
    if isinstance(data, dict) and "error" in data:
        return f"❌ API Error: {data['error']}"
    return data[0]["generated_text"]

# ✅ Custom CSS
st.markdown(
    """
    <style>
    .chat-message { max-width: 75%; padding: 12px 16px; margin: 10px 0;
                    border-radius: 12px; font-size: 16px; line-height: 1.5;
                    display: inline-block; word-break: break-word; }
    .user-container { display: flex; justify-content: flex-end; }
    .user-message { background-color: #2563eb; color: white; text-align: right; }
    .ai-container { display: flex; justify-content: flex-start; }
    .ai-message { background-color: #f3f4f6; color: #111827; text-align: left; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Agent Ramana (Mistral API)")

# ✅ Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "ai",
        "content": (
            "Hey, I'm Ramana (Mistral powered via API) — your friendly personal companion 🤗. "
            "You can share anything with me — your thoughts, dreams, problems, or just chat casually. "
            "I'm always here to listen and talk like a friend 💬"
        )
    }]

# ✅ Display past messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-container"><div class="chat-message user-message">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-container"><div class="chat-message ai-message">{msg["content"]}</div></div>', unsafe_allow_html=True)

# ✅ Chat input
user_input = st.chat_input("Say something to Ramana...")

if user_input:
    # Append & show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-container"><div class="chat-message user-message">{user_input}</div></div>', unsafe_allow_html=True)

    # Prepare prompt with history
    history_text = ""
    for message in st.session_state.messages:
        if message["role"] == "user":
            history_text += f"User: {message['content']}\n"
        else:
            history_text += f"Assistant: {message['content']}\n"
    history_text += "Assistant:"

    # Call HF API
    ai_reply = query_mistral(history_text).replace(history_text, "").strip()

    # Append & show AI reply
    st.session_state.messages.append({"role": "ai", "content": ai_reply})
    st.markdown(f'<div class="ai-container"><div class="chat-message ai-message">{ai_reply}</div></div>', unsafe_allow_html=True)



# import streamlit as st
# import google.generativeai as genai
# import os

# # ✅ Configure Streamlit page
# st.set_page_config(page_title="Agent Ramana", page_icon="🤖", layout="wide")

# # ✅ Load API key (works local & cloud)
# api_key = os.getenv("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY"))
# if not api_key:
#     st.error("❌ No API key found. Please set GEMINI_API_KEY in Streamlit secrets or as an environment variable.")
#     st.stop()

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-2.0-flash-lite")

# # ✅ Custom CSS
# st.markdown(
#     """
#     <style>
#     .chat-message {
#         max-width: 75%;
#         padding: 12px 16px;
#         margin: 10px 0;
#         border-radius: 12px;
#         font-size: 16px;
#         line-height: 1.5;
#         display: inline-block;
#         word-break: break-word;
#     }
#     .user-container {
#         display: flex;
#         justify-content: flex-end;
#     }
#     .user-message {
#         background-color: #2563eb;
#         color: white;
#         text-align: right;
#     }
#     .ai-container {
#         display: flex;
#         justify-content: flex-start;
#     }
#     .ai-message {
#         background-color: #f3f4f6;
#         color: #111827;
#         text-align: left;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("🤖 Agent Ramana")

# # ✅ Session state for chat
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {
#             "role": "ai",
#             "content": (
#                 "Hey, I'm Ramana — your friendly personal companion 🤗. "
#                 "You can share anything with me — your thoughts, dreams, problems, or just chat casually. "
#                 "I'm always here to listen and talk like a friend 💬"
#             )
#         }
#     ]

# # ✅ Display all past messages
# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.markdown(f'<div class="user-container"><div class="chat-message user-message">{msg["content"]}</div></div>', unsafe_allow_html=True)
#     else:
#         st.markdown(f'<div class="ai-container"><div class="chat-message ai-message">{msg["content"]}</div></div>', unsafe_allow_html=True)

# # ✅ Chat input
# user_input = st.chat_input("Say something to Ramana...")

# if user_input:
#     # Step 1: Append & display user message immediately
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     st.markdown(f'<div class="user-container"><div class="chat-message user-message">{user_input}</div></div>', unsafe_allow_html=True)

#     # Step 2: Prepare AI reply placeholder
#     placeholder = st.empty()
#     ai_reply = ""

#     # Step 3: Create chat history for Gemini
#     chat_history = [
#         {"role": "user", "parts": [m["content"]]} if m["role"] == "user"
#         else {"role": "model", "parts": [m["content"]]}
#         for m in st.session_state.messages
#     ]

#     # Step 4: Stream AI response live
#     try:
#         response = model.generate_content(chat_history, stream=True)
#         for chunk in response:
#             if chunk.text:
#                 ai_reply += chunk.text
#                 placeholder.markdown(
#                     f'<div class="ai-container"><div class="chat-message ai-message">{ai_reply}</div></div>',
#                     unsafe_allow_html=True
#                 )
#     except Exception as e:
#         ai_reply = f"⚠️ Error: {e}"

#     # Step 5: Append final AI reply to history
#     st.session_state.messages.append({"role": "ai", "content": ai_reply})

#     # Step 6: Force UI update
#     st.rerun()
