CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    * { font-family: 'Inter', -apple-system, sans-serif; }
    .mono { font-family: 'JetBrains Mono', monospace; }

    .stApp {
        background: linear-gradient(135deg, #0c0f1a 0%, #1a1a2e 50%, #0c0f1a 100%);
        color: #f1f5f9 !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"] {
        background: transparent !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stMarkdownContainer"] {
        color: inherit !important;
    }
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu {
        display: none !important;
    }
    .block-container {
        padding-top: 1.25rem !important;
    }

    .main-header {
        display: flex; align-items: center; gap: 16px; padding: 8px 0 4px 0;
    }
    .main-header h1 {
        font-size: 1.5rem; font-weight: 800; margin: 0;
        background: linear-gradient(135deg, #1a8a3a, #2ecc71);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .header-badge {
        background: rgba(26, 138, 58, 0.12);
        border: 1px solid rgba(26, 138, 58, 0.25);
        border-radius: 6px; padding: 2px 10px;
        font-size: 0.65rem; font-weight: 600; color: #6ee7a7;
        letter-spacing: 0.3px; text-transform: uppercase;
    }
    .flag-bar {
        height: 4px;
        background: linear-gradient(90deg, #1a1a2e 0%, #1a1a2e 33%,
                    #dc2626 33%, #dc2626 38%,
                    #ffffff 38%, #ffffff 44%,
                    #dc2626 44%, #dc2626 49%,
                    #16a34a 49%, #16a34a 100%);
        border-radius: 2px; margin: 0 0 12px 0;
    }

    .provision-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .provision-card:hover {
        background: rgba(255,255,255,0.06);
        border-color: rgba(255,255,255,0.12);
    }
    .provision-card .tax-type {
        font-size: 0.65rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .provision-card .title {
        font-size: 0.95rem; font-weight: 600; color: #f1f5f9;
        margin: 4px 0 6px 0;
    }
    .provision-card .summary {
        font-size: 0.8rem; color: #94a3b8; line-height: 1.5;
    }

    .impact-badge {
        display: inline-block; padding: 2px 8px;
        border-radius: 4px; font-size: 0.65rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.3px;
    }
    .impact-badge.high { background: rgba(239,68,68,0.12); color: #fca5a5; }
    .impact-badge.medium { background: rgba(245,158,11,0.12); color: #fcd34d; }
    .impact-badge.low { background: rgba(34,197,94,0.12); color: #86efac; }

    .comparison-table {
        width: 100%; border-collapse: separate; border-spacing: 0;
        border-radius: 10px; overflow: hidden;
    }
    .comparison-table th {
        background: rgba(255,255,255,0.04);
        padding: 10px 14px; font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px;
        color: #94a3b8; border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .comparison-table td {
        padding: 10px 14px; font-size: 0.82rem; color: #e2e8f0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    .comparison-table tr:last-child td { border-bottom: none; }

    .stat-ring {
        display: flex; align-items: center; justify-content: center;
        flex-direction: column;
        width: 100px; height: 100px; border-radius: 50%;
        background: conic-gradient(#16a34a 0% var(--pct), rgba(255,255,255,0.06) var(--pct) 100%);
    }
    .stat-ring-inner {
        width: 76px; height: 76px; border-radius: 50%;
        background: #0c0f1a;
        display: flex; align-items: center; justify-content: center;
        flex-direction: column;
    }
    .stat-ring-value { font-size: 1.2rem; font-weight: 700; color: #f1f5f9; }
    .stat-ring-label { font-size: 0.55rem; color: #94a3b8; text-transform: uppercase; }

    .timeline-item {
        display: flex; gap: 14px; padding: 12px 0;
        border-left: 2px solid rgba(255,255,255,0.06);
        padding-left: 16px; margin-left: 8px;
        position: relative;
    }
    .timeline-item::before {
        content: ''; position: absolute; left: -5px; top: 16px;
        width: 8px; height: 8px; border-radius: 50%;
        background: #16a34a;
    }
    .timeline-item .date {
        font-size: 0.75rem; font-weight: 600; color: #6ee7a7;
        min-width: 80px;
    }
    .timeline-item .desc {
        font-size: 0.82rem; color: #e2e8f0;
    }

    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px; padding: 16px; text-align: center;
    }
    .metric-card .value {
        font-size: 1.8rem; font-weight: 700;
        background: linear-gradient(135deg, #2ecc71, #16a34a);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-card .label {
        font-size: 0.7rem; color: #94a3b8; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px;
    }
    .glass-card h3 {
        font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin: 0 0 12px 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2px; background: rgba(255,255,255,0.02);
        border-radius: 10px; padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 6px 16px; font-size: 0.78rem;
        font-weight: 500; color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(22, 163, 74, 0.15) !important;
        color: #86efac !important;
    }

    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important; font-size: 0.85rem !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #16a34a !important;
        box-shadow: 0 0 0 2px rgba(22,163,74,0.12) !important;
    }
    [data-testid="stChatInput"] {
        background: transparent !important;
    }
    [data-testid="stChatInput"] > div {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #e2e8f0 !important;
        -webkit-text-fill-color: #e2e8f0 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }
    [data-testid="stChatInput"] button {
        background: rgba(34,197,94,0.14) !important;
        color: #86efac !important;
    }

    .stSelectbox>div>div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 8px !important; color: #e2e8f0 !important;
    }

    .stButton>button {
        background: rgba(22, 163, 74, 0.1);
        border: 1px solid rgba(22, 163, 74, 0.2);
        border-radius: 8px; color: #86efac;
        font-size: 0.78rem; font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: rgba(22, 163, 74, 0.2);
        border-color: rgba(22, 163, 74, 0.35);
        color: #a7f3d0;
    }

    .stExpander {
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        background: rgba(255,255,255,0.02) !important;
    }

    .suggestion-chip {
        display: inline-block;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 5px 14px;
        margin: 3px 4px; font-size: 0.75rem;
        color: #94a3b8; cursor: pointer;
        transition: all 0.2s ease;
    }
    .suggestion-chip:hover {
        background: rgba(22,163,74,0.1);
        border-color: rgba(22,163,74,0.2);
        color: #86efac;
    }
    .chat-message {
        padding: 10px 14px; border-radius: 12px;
        margin-bottom: 8px; font-size: 0.85rem; line-height: 1.6;
        animation: fadeSlideIn 0.3s ease;
        overflow: hidden;
    }
    .chat-message.user {
        background: rgba(96,165,250,0.1);
        border: 1px solid rgba(96,165,250,0.12);
        color: #e0f2fe;
    }
    .chat-message.assistant {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        color: #f1f5f9 !important;
    }
    .chat-message h1, .chat-message h2, .chat-message h3 {
        font-size: 1rem;
        line-height: 1.35;
        margin: 6px 0 8px;
        color: #f8fafc !important;
    }
    .chat-message .msg-content {
        color: #f1f5f9 !important;
    }
    .chat-message p,
    .chat-message .msg-line {
        margin: 6px 0;
        color: #f1f5f9 !important;
    }
    .chat-message ul, .chat-message ol {
        margin: 6px 0 8px 1.1rem;
        padding-left: 0.9rem;
        color: #f1f5f9 !important;
    }
    .chat-message li {
        margin: 4px 0;
        color: #f1f5f9 !important;
    }
    .chat-message strong { color: #ffffff !important; }
    .chat-message a { color: #60a5fa; }
    .chat-message .msg-label {
        font-size: 0.65rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.5px; margin-bottom: 4px;
    }
    .chat-message.user .msg-label { color: #60a5fa; }
    .chat-message.assistant .msg-label { color: #2ecc71; }
    .answer-muted {
        color: #cbd5e1 !important;
        font-size: 0.78rem;
        margin-top: 8px;
    }
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .thinking-indicator {
        display: flex; align-items: center; gap: 8px;
        padding: 10px 14px; margin-top: 4px;
    }
    .thinking-text {
        font-size: 0.82rem; color: #94a3b8; font-style: italic;
    }
    .thinking-dots span {
        font-size: 1.4rem; font-weight: 700; color: #2ecc71;
        animation: dotPulse 1.4s infinite;
    }
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes dotPulse {
        0%, 60%, 100% { opacity: 0.2; transform: translateY(0); }
        30% { opacity: 1; transform: translateY(-4px); }
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.08);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }
</style>
"""
