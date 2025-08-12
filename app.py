import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

# ✅ Configure Streamlit page
st.set_page_config(page_title="Agent Ramana (Mistral)", page_icon="🤖", layout="wide")

# ✅ Get HF token from environment or Streamlit secrets
hf_token = os.getenv("HF_TOKEN", st.secrets.get("HF_TOKEN"))
if not hf_token:
    st.error("❌ Please set your Hugging Face token as HF_TOKEN in Streamlit secrets or as an environment variable.")
    st.stop()

# ✅ Load Mistral model and tokenizer (from Hugging Face)
@st.cache_resource(show_spinner="Loading Mistral model... (this may take a while)")
def load_mistral():
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        token=hf_token
    )
    return model, tokenizer

model, tokenizer = load_mistral()

# ✅ Custom CSS
st.markdown(
    """
    <style>
    .chat-message {
        max-width: 75%;
        padding: 12px 16px;
        margin: 10px 0;
        border-radius: 12px;
        font-size: 16px;
        line-height: 1.5;
        display: inline-block;
        word-break: break-word;
    }
    .user-container {
        display: flex;
        justify-content: flex-end;
    }
    .user-message {
        background-color: #2563eb;
        color: white;
        text-align: right;
    }
    .ai-container {
        display: flex;
        justify-content: flex-start;
    }
    .ai-message {
        background-color: #f3f4f6;
        color: #111827;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Agent Ramana (Mistral)")

# ✅ Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "content": (
                "Hey, I'm Ramana (Mistral powered) — your friendly personal companion 🤗. "
                "You can share anything with me — your thoughts, dreams, problems, or just chat casually. "
                "I'm always here to listen and talk like a friend 💬"
            )
        }
    ]

# ✅ Display all past messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-container"><div class="chat-message user-message">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-container"><div class="chat-message ai-message">{msg["content"]}</div></div>', unsafe_allow_html=True)

# ✅ Chat input
user_input = st.chat_input("Say something to Ramana...")

if user_input:
    # Step 1: Append & display user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-container"><div class="chat-message user-message">{user_input}</div></div>', unsafe_allow_html=True)

    # Step 2: Prepare prompt for Mistral (chat style)
    history = st.session_state.messages
    prompt = ""
    for message in history:
        if message["role"] == "user":
            prompt += f"User: {message['content']}\n"
        else:
            prompt += f"Assistant: {message['content']}\n"
    prompt += "Assistant:"

    # Step 3: Generate response with Mistral
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    if torch.cuda.is_available():
        input_ids = input_ids.cuda()
        model.cuda()

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.75,
            top_p=0.95,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )
    output_text = tokenizer.decode(output_ids[0][input_ids.shape[-1]:], skip_special_tokens=True)
    ai_reply = output_text.strip()

    # Step 4: Display AI reply
    st.markdown(
        f'<div class="ai-container"><div class="chat-message ai-message">{ai_reply}</div></div>',
        unsafe_allow_html=True
    )

    # Step 5: Append AI reply to history
    st.session_state.messages.append({"role": "ai", "content": ai_reply})

    # Step 6: Force UI update
    st.rerun()
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
