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


def _inline_markdown(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def _markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    output = []
    list_type = None

    def close_list():
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            close_list()
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        numbered = re.match(r"^\d+\.\s+(.+)$", line)
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        citation = re.match(r"^\[\d+\]:\s*(.+)$", line)

        if heading:
            close_list()
            level = len(heading.group(1))
            output.append(f"<h{level}>{_inline_markdown(heading.group(2))}</h{level}>")
        elif numbered:
            if list_type != "ol":
                close_list()
                output.append("<ol>")
                list_type = "ol"
            output.append(f"<li>{_inline_markdown(numbered.group(1))}</li>")
        elif bullet:
            if list_type != "ul":
                close_list()
                output.append("<ul>")
                list_type = "ul"
            output.append(f"<li>{_inline_markdown(bullet.group(1))}</li>")
        elif citation:
            close_list()
            output.append(f'<div class="answer-muted">{_inline_markdown(raw_line)}</div>')
        else:
            close_list()
            output.append(f'<div class="msg-line">{_inline_markdown(line)}</div>')

    close_list()
    return "".join(output)


def _render_message(msg: dict) -> str:
    label = "You" if msg["role"] == "user" else "Finance Bill AI"
    if msg["role"] == "assistant":
        raw_content = msg["content"]
        content = raw_content if "<" in raw_content and ">" in raw_content else _markdown_to_html(raw_content)
    else:
        content = f'<div class="msg-line">{html.escape(msg["content"])}</div>'

    return (
        f'<div class="chat-message {msg["role"]}">'
        f'<div class="msg-label">{label}</div>'
        f'<div class="msg-content">{content}</div>'
        "</div>"
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
    return f'{_markdown_to_html(reply)}<div class="answer-muted">Answered through Copilot Studio.</div>'


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
            f'<div style="font-size:1.8rem;font-weight:800;color:#ffffff;">{_visitor_count:,}</div>'
            f'<div style="font-size:0.72rem;color:#ffffff;opacity:0.6;">visitors</div>'
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
            st.markdown(_render_message(msg), unsafe_allow_html=True)

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
