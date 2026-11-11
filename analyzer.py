"""Simple, explainable phishing indicators. This is not a phishing verdict or an AI model."""

from dataclasses import dataclass
import re
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Finding:
    label: str
    explanation: str
    points: int


# Explicitly limited to a few beginner-friendly patterns. Extend and test over time.
RULES = (
    (r"\b(?:sofort|unverzüglich|innerhalb von 24 stunden|urgent|immediately)\b",
     "Zeitdruck", "Die Nachricht fordert eine besonders schnelle Reaktion.", 20),
    (r"\b(?:konto|account|zugang)\b.{0,45}\b(?:gesperrt|sperren|deaktiviert|blocked|suspended)\b",
     "Drohung mit Sperrung", "Die Nachricht stellt eine Kontosperrung in Aussicht.", 20),
    (r"\b(?:passwort|password|tan|pin|anmeldedaten)\b.{0,55}\b(?:eingeben|bestätigen|senden|mitteilen|verify|confirm)\b",
     "Aufforderung zu sensiblen Daten", "Es werden möglicherweise Zugangsdaten angefordert.", 25),
)

URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


def analyze_email(message: str) -> tuple[int, list[Finding]]:
    """Return a heuristic 0-100 score and human-readable risk indicators."""
    if not isinstance(message, str):
        raise TypeError("message muss eine Zeichenkette sein")

    text = message.strip()
    if not text:
        return 0, []

    findings: list[Finding] = []
    for pattern, label, explanation, points in RULES:
        if re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(Finding(label, explanation, points))

    urls = [candidate.rstrip(".,;!?)") for candidate in URL_PATTERN.findall(text)]
    if urls:
        findings.append(Finding(
            "Externer Link", "Die Nachricht enthält einen Link. Prüfe die tatsächliche Domain vor dem Öffnen.", 10
        ))

    for url in urls:
        hostname = (urlsplit(url).hostname or "").lower()
        if hostname.startswith("xn--") or ".xn--" in hostname:
            findings.append(Finding(
                "Punycode-Domain", "Die Domain verwendet Punycode; eine Verwechslungsgefahr ist möglich.", 25
            ))
            break

    if len(urls) >= 3:
        findings.append(Finding(
            "Viele Links", "Die Nachricht enthält mehrere Links; prüfe die Ziele sorgfältig.", 10
        ))

    score = min(100, sum(finding.points for finding in findings))
    return score, findings


def risk_level(score: int) -> str:
    """Illustrative score bands; not statistically calibrated probabilities."""
    if score >= 60:
        return "Erhöhte Auffälligkeit"
    if score >= 25:
        return "Einige Auffälligkeiten"
    return "Wenige Auffälligkeiten"
