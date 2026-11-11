
"""Simple, explainable phishing indicators.
This is not a phishing verdict or an AI model.
"""

from dataclasses import dataclass
import ipaddress
import re
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Finding:
    label: str
    explanation: str
    points: int


# Regelbasierte Erkennung verdächtiger Formulierungen
RULES = (
    (
        r"\b(?:sofort|unverzüglich|innerhalb von 24 stunden|urgent|immediately)\b",
        "Zeitdruck",
        "Die Nachricht fordert eine besonders schnelle Reaktion.",
        20,
    ),
    (
        r"\b(?:konto|account|zugang)\b.{0,45}\b(?:gesperrt|sperren|deaktiviert|blocked|suspended)\b",
        "Drohung mit Sperrung",
        "Die Nachricht stellt eine Kontosperrung in Aussicht.",
        20,
    ),
    (
        r"\b(?:passwort|password|tan|pin|anmeldedaten)\b.{0,55}\b(?:eingeben|bestätigen|senden|mitteilen|verify|confirm)\b",
        "Aufforderung zu sensiblen Daten",
        "Es werden möglicherweise Zugangsdaten angefordert.",
        25,
    ),
)


# Erkennt HTTP- und HTTPS-Links im Text
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+",
    re.IGNORECASE
)


def is_ip_address(hostname: str) -> bool:
    """Prüft, ob ein Hostname eine IPv4- oder IPv6-Adresse ist."""
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def analyze_email(message: str) -> tuple[int, list[Finding]]:
    """Analysiert E-Mails anhand erklärbarer Sicherheitsregeln."""

    if not isinstance(message, str):
        raise TypeError("message muss eine Zeichenkette sein")

    text = message.strip()

    if not text:
        return 0, []

    findings: list[Finding] = []

    # 1. Verdächtige Formulierungen erkennen
    for pattern, label, explanation, points in RULES:
        if re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(
                Finding(label, explanation, points)
            )

    # 2. URLs aus der E-Mail extrahieren
    urls = [
        candidate.rstrip(".,;!?)")
        for candidate in URL_PATTERN.findall(text)
    ]

    if urls:
        findings.append(
            Finding(
                "Externer Link",
                "Die Nachricht enthält einen Link. Prüfe die tatsächliche Domain vor dem Öffnen.",
                10,
            )
        )

    # 3. Einzelne URLs untersuchen
    for url in urls:
        hostname = (urlsplit(url).hostname or "").lower()

        # Neue Funktion: IP-Adresse als Linkziel erkennen
        if is_ip_address(hostname):
            findings.append(
                Finding(
                    "IP-Adresse im Link",
                    "Der Link verwendet eine direkte IP-Adresse statt eines Domainnamens.",
                    25,
                )
            )
            break

    # 4. Punycode-Domains erkennen
    for url in urls:
        hostname = (urlsplit(url).hostname or "").lower()

        if hostname.startswith("xn--") or ".xn--" in hostname:
            findings.append(
                Finding(
                    "Punycode-Domain",
                    "Die Domain verwendet Punycode; eine Verwechslungsgefahr ist möglich.",
                    25,
                )
            )
            break

    # 5. Ungewöhnlich viele Links erkennen
    if len(urls) >= 3:
        findings.append(
            Finding(
                "Viele Links",
                "Die Nachricht enthält mehrere Links; prüfe die Ziele sorgfältig.",
                10,
            )
        )

    # 6. Gesamtscore berechnen
    score = min(
        100,
        sum(finding.points for finding in findings)
    )

    return score, findings


def risk_level(score: int) -> str:
    """Ordnet den heuristischen Score einer Risikostufe zu."""

    if score >= 60:
        return "Erhöhte Auffälligkeit"

    if score >= 25:
        return "Einige Auffälligkeiten"

    return "Wenige Auffälligkeiten"
