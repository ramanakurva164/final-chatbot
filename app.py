import streamlit as st
import requests
import os

# ✅ Set your Mistral API Key (You can also store in Streamlit Secrets)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "your_api_key_here")

# ✅ API endpoint
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# ✅ Streamlit UI
st.set_page_config(page_title="Mistral Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Mistral AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask something..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create empty container for AI streaming response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # API request with streaming enabled
            response = requests.post(
                MISTRAL_API_URL,
                headers={
                    "Authorization": f"Bearer {MISTRAL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistral-small-latest",  # You can change to mistral-medium-latest
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "stream": True
                },
                stream=True  # Enable streaming
            )

            # ✅ Read and display chunks as they arrive
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = line.decode("utf-8")
                        if '"content"' in chunk:
                            text_piece = chunk.split('"content":"')[-1].split('"')[0]
                            full_response += text_piece
                            response_placeholder.markdown(full_response)
                    except:
                        pass

        except Exception as e:
            full_response = f"⚠️ Error: {e}"
            response_placeholder.markdown(full_response)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": full_response})




# import streamlit as st
# import requests
# import os
# import time

# # ✅ Streamlit page settings
# st.set_page_config(page_title="Agent Ramana (Mistral API)", page_icon="🤖", layout="wide")

# # ✅ Hugging Face token
# hf_token = os.getenv("HF_TOKEN") or st.secrets.get("HF_TOKEN")
# if not hf_token:
#     st.error("❌ Please set your Hugging Face token in Streamlit secrets or environment variables.")
#     st.stop()

# API_URL = "https://router.huggingface.co/v1/chat/completions"
# HEADERS = {"Authorization": f"Bearer {hf_token}"}
# MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"

# # ✅ Chat history in session state
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hey, I'm Ramana (Mistral powered via API). How can I help you today? 😊"}
#     ]

# # ✅ Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ✅ Chat input
# if user_input := st.chat_input("Say something to Ramana..."):
#     # Append user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Prepare payload
#     payload = {
#         "model": MODEL_ID,
#         "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
#         "max_tokens": 256,
#         "temperature": 0.7,
#         "top_p": 0.95
#     }

#     with st.chat_message("assistant"):
#         placeholder = st.empty()
#         full_reply = ""

#         try:
#             # ✅ No streaming — single full reply
#             response = requests.post(API_URL, headers=HEADERS, json=payload)
#             response.raise_for_status()
#             data = response.json()

#             full_reply = data["choices"][0]["message"]["content"]

#             # Typing effect
#             typed_text = ""
#             for char in full_reply:
#                 typed_text += char
#                 placeholder.markdown(typed_text + "▌")
#                 time.sleep(0.015)
#             placeholder.markdown(typed_text)

#             st.session_state.messages.append({"role": "assistant", "content": full_reply})

#         except requests.exceptions.RequestException as e:
#             st.error(f"API Error: {e}")



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
