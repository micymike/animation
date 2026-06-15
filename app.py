import html
import os
import re

import requests
import streamlit as st

from style import CSS

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from embed import PDF_PATH
from finance_ai import answer_question
from copilot import CopilotError, send_message, start_conversation
from rag import load_index, search


st.set_page_config(page_title="Finance Bill 2026 - AI Analyst", layout="wide", page_icon="KE")
st.markdown(CSS, unsafe_allow_html=True)

_SUGGESTIONS = [
    "Summarise the key tax changes in the Bill",
    "What is the new rental income tax rate?",
    "How does VAT on digital services work?",
    "What are the new filing deadlines?",
    "Explain the tax amnesty extension",
    "What is the revenue target for 2026/27?",
    "How does the expanded royalty definition work?",
    "What changes for non-resident landlords?",
]


def _message_start(msg: dict) -> str:
    label = "You" if msg["role"] == "user" else "Finance Bill AI"
    return (
        f'<div class="chat-message {msg["role"]}">'
        f'<div class="msg-label">{label}</div>'
    )


def _plain_text(html_text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html_text)
    text = re.sub(r"</(p|li|ul)>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(re.sub(r"\n{3,}", "\n\n", text)).strip()


def _build_copilot_prompt(question: str, results: list[dict], local_answer: str) -> str:
    passages = []
    for i, result in enumerate(results[:4], 1):
        text = re.sub(r"\s+", " ", result["text"]).strip()
        passages.append(f"Passage {i} ({result['source']}, score {result['score']:.2f}): {text[:900]}")

    context = "\n\n".join(passages) if passages else "No relevant PDF passages were retrieved."
    draft = _plain_text(local_answer)

    return (
        "FINANCE_BILL_RAG_REQUEST\n\n"
        "You are Finance Bill AI for a Kenya Finance Bill 2026 RAG application.\n"
        "Answer the user's question using ONLY the Finance Bill context and extracted answer below.\n"
        "Do not ask the user what question they have. Do not give a generic financial-advice disclaimer.\n"
        "If the context is insufficient, say exactly what is missing.\n\n"
        f"USER QUESTION:\n{question}\n\n"
        f"RETRIEVED FINANCE BILL PASSAGES:\n{context}\n\n"
        f"EXTRACTED FINANCE BILL ANSWER TO PRESERVE:\n{draft}\n\n"
        "FINAL ANSWER:"
    )


def _looks_like_canned_copilot_reply(reply: str) -> bool:
    normalized = " ".join(reply.lower().split())
    canned_phrases = [
        "what question do you have about the kenyan finance bill",
        "thank you for your question about the kenyan finance bill",
        "seek the guidance of a licensed financial professional",
        "general educational purposes only",
        "making any investment or financial decisions",
        "no response from copilot",
    ]
    return any(phrase in normalized for phrase in canned_phrases)


def _format_copilot_reply(reply: str) -> str:
    return f"{reply}\n\n<span class=\"answer-muted\">Answered through Copilot Studio.</span>"


def _format_local_fallback(reply: str, reason: str) -> str:
    return (
        f"{reply}"
        "<p class=\"answer-muted\">"
        f"Copilot Studio was called, but the app used the Finance Bill RAG fallback because {html.escape(reason)}."
        "</p>"
    )


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Ask me anything about the Kenya Finance Bill 2026. "
                "I search the full document to find answers."
            ),
        }
    ]

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False
    st.session_state.index_error = None
    try:
        idx, _chunks = load_index()
        if idx is not None:
            st.session_state.index_ready = True
        else:
            st.session_state.index_error = "No index found. Run `python embed.py` first."
    except Exception as e:
        st.session_state.index_error = str(e)

if "waiting" not in st.session_state:
    st.session_state.waiting = False

if "conv_id" not in st.session_state:
    st.session_state.conv_id = None
    st.session_state.conv_token = None


st.markdown('<div class="flag-bar"></div>', unsafe_allow_html=True)
cols = st.columns([2.5, 1])
with cols[0]:
    st.markdown(
        '<div class="main-header">'
        "<h1>Kenya Finance Bill 2026</h1>"
        '<span class="header-badge">RAG Analyst</span>'
        "</div>"
        '<div style="font-size:0.8rem;color:#94a3b8;margin-top:-6px;margin-bottom:8px;">'
        'Created by <strong style="color:#e2e8f0;">Michael Moses</strong>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color:#64748b;font-size:0.82rem;margin-bottom:0;">'
        f"Searching <strong>{html.escape(PDF_PATH.name)}</strong> via vector embeddings"
        "</div>",
        unsafe_allow_html=True,
    )

if not st.session_state.index_ready:
    st.error(f"Index not found: {st.session_state.index_error}")
    st.stop()


chat_col, info_col = st.columns([2.5, 1])

with info_col:
    st.markdown(
        '<div class="glass-card">'
        "<h3>About</h3>"
        '<div style="font-size:0.78rem;color:#94a3b8;line-height:1.7;">'
        "<strong style='color:#e2e8f0;'>Published:</strong> 30 April 2026<br>"
        "<strong style='color:#e2e8f0;'>Status:</strong> Public participation to Parliamentary debate<br>"
        "<strong style='color:#e2e8f0;'>Target Assent:</strong> End of June 2026<br>"
        "<strong style='color:#e2e8f0;'>Revenue Target:</strong> KES 3.533 trillion"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    try:
        _visitor_count = requests.get(
            "https://api.countapi.xyz/hit/micymike-animation/visits",
            timeout=3,
        ).json().get("value", 0)
    except Exception:
        _visitor_count = None
    if _visitor_count is not None:
        st.markdown(
            f'<div class="glass-card" style="margin-top:12px;text-align:center;">'
            f'<div style="font-size:1.6rem;font-weight:700;color:#e2e8f0;">{_visitor_count:,}</div>'
            f'<div style="font-size:0.72rem;color:#94a3b8;">visitors</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="glass-card" style="margin-top:12px;">'
        "<h3>How It Works</h3>"
        '<div style="font-size:0.78rem;color:#94a3b8;line-height:1.7;">'
        "1. PDF is chunked and embedded locally<br>"
        "2. Your question is matched to passages<br>"
        "3. Context is sent to Copilot Studio<br>"
        "4. Guardrails verify the answer is Finance Bill-specific"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


with chat_col:
    chat_container = st.container(height=480)
    with chat_container:
        for msg in st.session_state.messages:
            st.markdown(_message_start(msg), unsafe_allow_html=True)
            if msg["role"] == "assistant":
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.markdown(html.escape(msg["content"]), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.waiting:
        st.markdown(
            '<div class="thinking-indicator">'
            '<span class="thinking-text">chill kiasi nafikiria</span>'
            '<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>'
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size:0.7rem;color:#64748b;margin:8px 0 4px;font-weight:500;">'
            "SUGGESTED QUESTIONS"
            "</div>",
            unsafe_allow_html=True,
        )
        suggestion_cols = st.columns(2)
        for i, suggestion in enumerate(_SUGGESTIONS):
            with suggestion_cols[i % 2]:
                if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    st.session_state.waiting = True
                    st.rerun()

    user_input = st.chat_input("Ask about the Finance Bill...", disabled=st.session_state.waiting)
    if user_input and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        st.session_state.waiting = True
        st.rerun()


if st.session_state.waiting and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    question = st.session_state.messages[-1]["content"]

    try:
        results = search(question, k=5)
        local_reply = answer_question(question, results)
        prompt = _build_copilot_prompt(question, results, local_reply)

        try:
            if st.session_state.conv_id is None:
                conv_id, conv_token = start_conversation()
                st.session_state.conv_id = conv_id
                st.session_state.conv_token = conv_token

            copilot_reply = send_message(
                st.session_state.conv_id,
                st.session_state.conv_token,
                prompt,
            )

            if _looks_like_canned_copilot_reply(copilot_reply):
                reply = _format_local_fallback(local_reply, "Copilot returned a generic fallback response")
            else:
                reply = _format_copilot_reply(copilot_reply)
        except CopilotError as e:
            st.session_state.conv_id = None
            st.session_state.conv_token = None
            reply = _format_local_fallback(local_reply, f"Copilot Studio returned an error: {e}")
    except Exception as e:
        reply = f"Error: {html.escape(str(e))}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.waiting = False
    st.rerun()
