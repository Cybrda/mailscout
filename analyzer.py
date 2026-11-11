
"""MailScout – Explainable Email Security Analyzer.

Rule-based detection of phishing indicators.
This is not an AI model or a definitive phishing verdict.
"""

from dataclasses import dataclass
import ipaddress
import re
from urllib.parse import urlsplit


# ------------------------------------------
# 1. Datenstruktur für Sicherheitswarnungen
# ------------------------------------------

@dataclass(frozen=True)
class Finding:
    label: str
    explanation: str
    points: int


# ------------------------------------------
# 2. Regeln für verdächtige Formulierungen
# ------------------------------------------

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


# ------------------------------------------
# 3. URL-Erkennung
# ------------------------------------------

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+",
    re.IGNORECASE
)


# ------------------------------------------
# 4. IP-Adressen erkennen
# ------------------------------------------

def is_ip_address(hostname: str) -> bool:
    """Prüft, ob ein Hostname eine IPv4- oder IPv6-Adresse ist."""

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


# ------------------------------------------
# 5. Verdächtige Subdomains erkennen
# ------------------------------------------

def has_suspicious_subdomain(hostname: str) -> bool:
    """Erkennt bekannte Unternehmensdomains innerhalb fremder Hostnamen."""

    trusted_domains = (
        "amazon.de",
        "paypal.com",
        "google.com",
    )

    hostname = hostname.lower().rstrip(".")

    for domain in trusted_domains:

        # Echte Domains und ihre Subdomains nicht markieren
        if hostname == domain or hostname.endswith("." + domain):
            continue

        # Bekannte Domain vor einer fremden Domain erkennen
        if hostname.startswith(domain + "."):
            return True

        if "." + domain + "." in hostname:
            return True

    return False


# ------------------------------------------
# 6. Hauptfunktion: E-Mail analysieren
# ------------------------------------------

def analyze_email(message: str) -> tuple[int, list[Finding]]:
    """Analysiert E-Mails anhand erklärbarer Sicherheitsregeln."""

    if not isinstance(message, str):
        raise TypeError("message muss eine Zeichenkette sein")

    text = message.strip()

    if not text:
        return 0, []

    findings: list[Finding] = []

    # Verdächtige Formulierungen erkennen
    for pattern, label, explanation, points in RULES:
        if re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(
                Finding(label, explanation, points)
            )

    # URLs aus dem Text extrahieren
    urls = [
        candidate.rstrip(".,;!?)")
        for candidate in URL_PATTERN.findall(text)
    ]

    

    # IP-Adressen in Links erkennen
    for url in urls:
        hostname = (urlsplit(url).hostname or "").lower()

        if is_ip_address(hostname):
            findings.append(
                Finding(
                    "IP-Adresse im Link",
                    "Der Link verwendet eine direkte IP-Adresse "
                    "statt eines Domainnamens.",
                    25,
                )
            )
            break

    # Verdächtige Marken-Subdomains erkennen
    for url in urls:
        hostname = (urlsplit(url).hostname or "").lower()

        if has_suspicious_subdomain(hostname):
            findings.append(
                Finding(
                    "Verdächtige Subdomain",
                    "Eine bekannte Unternehmensdomain erscheint "
                    "innerhalb eines fremden Domainnamens.",
                    25,
                )
            )
            break

    # Punycode-Domains erkennen
    for url in urls:
        hostname = (urlsplit(url).hostname or "").lower()

        if hostname.startswith("xn--") or ".xn--" in hostname:
            findings.append(
                Finding(
                    "Punycode-Domain",
                    "Die Domain verwendet Punycode; "
                    "eine Verwechslungsgefahr ist möglich.",
                    25,
                )
            )
            break

    # Ungewöhnlich viele Links erkennen
    if len(urls) >= 3:
        findings.append(
            Finding(
                "Viele Links",
                "Die Nachricht enthält mehrere Links; "
                "prüfe die Ziele sorgfältig.",
                10,
            )
        )

    # Gesamtscore berechnen (maximal 100 Punkte)
    score = min(
        100,
        sum(finding.points for finding in findings)
    )

    return score, findings


# ------------------------------------------
# 7. Risikostufe bestimmen
# ------------------------------------------

def risk_level(score: int) -> str:
    """Ordnet den heuristischen Score einer Risikostufe zu."""

    if score >= 60:
        return "Erhöhte Auffälligkeit"

    if score >= 25:
        return "Einige Auffälligkeiten"

    return "Wenige Auffälligkeiten"
