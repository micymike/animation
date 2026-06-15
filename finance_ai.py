import html
import re

from data import EFFECTIVE_DATES, IMPACT, PROVISIONS, SUMMARY_METRICS


STOPWORDS = {
    "about", "after", "again", "against", "bill", "does", "from", "have",
    "income", "into", "kenya", "kenyan", "new", "rate", "tax", "tell",
    "that", "the", "this", "what",
    "when", "where", "which", "with", "work", "works", "would", "your",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in STOPWORDS
    }


def _provision_text(provision: dict) -> str:
    return " ".join(
        str(provision.get(field, ""))
        for field in (
            "title",
            "summary",
            "current_law",
            "proposed_law",
            "affected",
            "details",
            "tax_type",
        )
    )


def _matching_provisions(question: str, limit: int = 5) -> list[dict]:
    q_tokens = _tokens(question)
    scored = []

    for provision in PROVISIONS:
        text = _provision_text(provision).lower()
        p_tokens = _tokens(text)
        score = len(q_tokens & p_tokens)

        phrase = question.lower().strip()
        if phrase and phrase in text:
            score += 5
        if "vat" in question.lower() and provision["tax_type"].value == "VAT Act":
            score += 2
        if "rental" in question.lower() and "rental" in text:
            score += 3
        if "digital" in question.lower() and "digital" in text:
            score += 3
        if "deadline" in question.lower() and ("deadline" in text or "return" in text):
            score += 2
        if "amnesty" in question.lower() and "amnesty" in text:
            score += 4

        if score:
            scored.append((score, provision))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [provision for _, provision in scored[:limit]]


def _impact_label(provision: dict) -> str:
    return IMPACT[provision["impact"]]["label"]


def _effective_date(provision: dict) -> str:
    return EFFECTIVE_DATES[provision["effective"]]


def _provision_li(provision: dict) -> str:
    return (
        "<li>"
        f"<strong>{html.escape(provision['title'])}</strong>: "
        f"{html.escape(provision['summary'])} "
        f"<span class=\"answer-muted\">Effective: {html.escape(_effective_date(provision))}; "
        f"impact: {html.escape(_impact_label(provision))}.</span>"
        "</li>"
    )


def _summary_answer() -> str:
    high_impact = [p for p in PROVISIONS if p["impact"] == "high"][:8]
    items = "".join(_provision_li(p) for p in high_impact)
    return (
        "<p>The main Finance Bill 2026 tax changes are:</p>"
        f"<ul>{items}</ul>"
        "<p class=\"answer-muted\">"
        f"The tracker currently highlights {SUMMARY_METRICS['total_provisions']} provisions "
        f"across {SUMMARY_METRICS['tax_types_affected']} tax law areas, including "
        f"{SUMMARY_METRICS['high_impact']} high-impact measures."
        "</p>"
    )


def _specific_answer(question: str) -> str:
    matches = _matching_provisions(question)
    if not matches:
        return ""

    primary = matches[0]
    related = matches[1:4]
    related_html = "".join(_provision_li(p) for p in related)

    answer = (
        f"<p><strong>{html.escape(primary['title'])}</strong></p>"
        f"<p>{html.escape(primary['summary'])}</p>"
        "<ul>"
        f"<li><strong>Current position:</strong> {html.escape(primary['current_law'])}</li>"
        f"<li><strong>Proposed change:</strong> {html.escape(primary['proposed_law'])}</li>"
        f"<li><strong>Who is affected:</strong> {html.escape(primary['affected'])}</li>"
        f"<li><strong>Effective date:</strong> {html.escape(_effective_date(primary))}</li>"
        "</ul>"
        f"<p>{html.escape(primary['details'])}</p>"
    )

    if related_html:
        answer += f"<p><strong>Related provisions:</strong></p><ul>{related_html}</ul>"

    return answer


def _passage_answer(results: list[dict]) -> str:
    if not results:
        return (
            "<p>I could not find a strong matching passage in the Finance Bill index. "
            "Try asking with the tax type or the exact subject, for example rental income, VAT, "
            "excise duty, tax amnesty, or virtual assets.</p>"
        )

    items = []
    for result in results[:3]:
        text = re.sub(r"\s+", " ", result["text"]).strip()
        if len(text) > 520:
            text = text[:520].rsplit(" ", 1)[0] + "..."
        items.append(
            "<li>"
            f"<span class=\"answer-muted\">{html.escape(result['source'])}, score "
            f"{result['score']:.2f}</span><br>"
            f"{html.escape(text)}"
            "</li>"
        )

    return (
        "<p>I found these closest Finance Bill passages. The Bill text is technical, "
        "so I am showing the relevant extracts directly:</p>"
        f"<ul>{''.join(items)}</ul>"
    )


def answer_question(question: str, results: list[dict]) -> str:
    q = question.lower()
    if any(word in q for word in ("summarise", "summarize", "summary", "key changes", "overview")):
        return _summary_answer()

    answer = _specific_answer(question)
    if answer:
        return answer

    return _passage_answer(results)
