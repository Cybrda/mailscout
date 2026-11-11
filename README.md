# 🛡️ MailScout
### Erklärbarer E-Mail-Sicherheitsanalysator

**MailScout** ist eine Python-basierte Webanwendung zur Erkennung und nachvollziehbaren Bewertung potenzieller Phishing-Merkmale in E-Mail-Texten.

Das Projekt verbindet grundlegende Methoden der **E-Mail-Sicherheit, Phishing-Erkennung, sicheren Softwareentwicklung und automatisierten Qualitätssicherung**.

Ziel ist es, verdächtige Merkmale zu identifizieren, verständlich zu erklären und die Sicherheitsanalyse schrittweise zu verbessern.

🌐 **[MailScout live ausprobieren](https://mailscout-cybrda.streamlit.app/)**

💻 **[GitHub-Repository](https://github.com/Cybrda/mailscout)**

---

## 📌 Projektübersicht

Phishing zählt zu den verbreiteten Bedrohungen der IT-Sicherheit. Angreifer nutzen häufig psychologische Manipulation, künstlichen Zeitdruck und irreführende Internetadressen, um Nutzer zur Preisgabe sensibler Informationen zu bewegen.

MailScout analysiert eingegebene E-Mail-Texte anhand definierter Sicherheitsregeln und zeigt erkannte Auffälligkeiten mit verständlichen Erklärungen an.

**Die Anwendung bietet:**

- Regelbasierte Analyse verdächtiger E-Mail-Inhalte
- Erkennung ausgewählter URL- und Domain-Auffälligkeiten
- Nachvollziehbare Risikobewertung von 0 bis 100
- Individuelle Erklärungen zu erkannten Warnsignalen
- Interaktive Weboberfläche
- Automatisierte Softwaretests

> **Hinweis:** MailScout v0.2 arbeitet regelbasiert und verwendet noch keine künstliche Intelligenz. Der berechnete Auffälligkeitswert stellt keine statistisch ermittelte Phishing-Wahrscheinlichkeit dar. Auch eine Bewertung von 0 Punkten garantiert keine sichere E-Mail.

---

## 🔍 Funktionen

### 1. Erkennung verdächtiger Formulierungen

MailScout untersucht E-Mail-Texte auf typische Social-Engineering-Merkmale.

Dazu gehören:

- Künstlicher Zeitdruck und dringende Handlungsaufforderungen
- Drohungen mit einer Kontosperrung
- Aufforderungen zur Eingabe oder Weitergabe sensibler Zugangsdaten

Jedes erkannte Merkmal wird einzeln erläutert.

### 2. Erkennung von IP-Adressen in URLs

MailScout überprüft, ob ein Link eine direkte IPv4- oder IPv6-Adresse anstelle eines üblichen Domainnamens verwendet.

**Beispiel:**

`http://192.0.2.15/login`

Direkte IP-Adressen sind nicht grundsätzlich gefährlich. In bestimmten E-Mail-Kontexten können sie jedoch ein zusätzliches Warnsignal darstellen.

### 3. Erkennung irreführender Subdomains

MailScout erkennt ausgewählte Muster, bei denen bekannte Unternehmensdomains innerhalb fremder Hostnamen verwendet werden.

**Beispiel:**

`https://amazon.de.login.example.com`

Obwohl die Adresse `amazon.de` enthält, gehört die tatsächlich registrierbare Domain in diesem Beispiel zu `example.com`.

Die aktuelle Implementierung berücksichtigt ausgewählte Domains von Amazon, PayPal und Google.

Die Erkennung ist bewusst begrenzt und stellt noch keine vollständige Prüfung auf Markenimitation dar.

### 4. Erkennung von Punycode-Domains

MailScout erkennt Hostnamen mit Punycode-Kennzeichnungen.

Punycode wird regulär zur Darstellung internationalisierter Domainnamen verwendet. In bestimmten Angriffsszenarien können jedoch ähnlich aussehende Zeichen zur Täuschung eingesetzt werden.

Das Vorhandensein von Punycode ist deshalb allein kein Nachweis für Phishing.

### 5. Erklärbare Risikobewertung

Die Anwendung berechnet anhand der erkannten Sicherheitsmerkmale einen heuristischen Auffälligkeitswert.

| Sicherheitsmerkmal | Punkte |
|---|---:|
| Künstlicher Zeitdruck | +20 |
| Drohung mit Kontosperrung | +20 |
| Aufforderung zu sensiblen Daten | +25 |
| Direkte IP-Adresse im Link | +25 |
| Irreführende Marken-Subdomain | +25 |
| Punycode-Domain | +25 |
| Mindestens drei Links | +10 |

**Einstufung:**

| Punktzahl | Bewertung |
|---|---|
| 0–24 | Wenige Auffälligkeiten |
| 25–59 | Einige Auffälligkeiten |
| 60–100 | Erhöhte Auffälligkeit |

Der Score ist auf 100 Punkte begrenzt. Die Punktwerte sind bislang nicht statistisch kalibriert.

**Wichtige Verbesserung in Version 0.2:** Gewöhnliche HTTP- und HTTPS-Links erhöhen den Auffälligkeitswert nicht mehr automatisch. Dadurch sollen unnötige Warnungen reduziert werden.

### 6. Interaktive Weboberfläche

Die Benutzeroberfläche wurde mit Streamlit entwickelt und ermöglicht:

- Eingabe eigener E-Mail-Texte
- Anzeige des Auffälligkeitswerts
- Verständliche Sicherheitseinstufung
- Aufklappbare Erklärungen zu Warnsignalen
- Neutrale Anzeige gefundener URLs
- Allgemeine Sicherheitsempfehlungen

---

## 🧪 Automatisierte Tests

Zur Qualitätssicherung verwendet MailScout das Python-Testframework **pytest**.

Aktuell wurden fünf automatische Tests implementiert und über GitHub Actions erfolgreich ausgeführt.

| Testfall | Erwartetes Ergebnis | Status |
|---|---|---|
| Harmlose E-Mail | 0 Punkte | Bestanden |
| Reguläre Amazon-Subdomain | 0 Punkte | Bestanden |
| Irreführende Subdomain | 25 Punkte | Bestanden |
| Direkte IP-Adresse | 25 Punkte | Bestanden |
| Zeitdruck und Kontosperrungsdrohung | 40 Punkte | Bestanden |

Die Tests überprüfen ausgewählte Funktionen. Sie stellen noch keinen Nachweis einer allgemein zuverlässigen Phishing-Erkennung dar.

### Continuous Integration mit GitHub Actions

Bei Änderungen am Repository kann GitHub Actions die automatisierten Tests selbstständig ausführen.

Der Ablauf:

1. GitHub lädt den aktuellen Quellcode.
2. Eine Python-Umgebung wird eingerichtet.
3. pytest wird installiert.
4. Die Sicherheitsfunktionen werden getestet.
5. GitHub zeigt den erfolgreichen oder fehlgeschlagenen Testlauf an.

**[Automatisierte Testläufe ansehen](https://github.com/Cybrda/mailscout/actions)**

---

## 💻 Installation und lokaler Start

### Voraussetzungen

- Python 3.12
- Visual Studio Code oder ein vergleichbarer Editor
- Git (optional)

### 1. Repository herunterladen

```bash
git clone https://github.com/Cybrda/mailscout.git
cd mailscout
```

Alternativ kann das Repository als ZIP-Datei heruntergeladen werden.

### 2. Virtuelle Python-Umgebung erstellen

Unter Windows:

```powershell
py -3.12 -m venv .venv
```

### 3. Abhängigkeiten installieren

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Anwendung starten

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Die Anwendung ist anschließend normalerweise unter folgender Adresse erreichbar:

`http://localhost:8501`

### 5. Automatisierte Tests ausführen

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest -v test_analyzer.py
```

---

## 📁 Projektstruktur

```text
mailscout/
│
├── app.py
├── analyzer.py
├── test_analyzer.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .github/
    └── workflows/
        └── main.yml
```

**Dateierklärung:**

- `app.py`: Benutzeroberfläche und Darstellung der Analyseergebnisse
- `analyzer.py`: Sicherheitsregeln und Risikobewertung
- `test_analyzer.py`: Automatisierte Funktionstests
- `requirements.txt`: Benötigte Python-Bibliotheken
- `main.yml`: Automatisierte Testausführung über GitHub Actions

---

## 🔐 Sicherheits- und Datenschutzhinweise

MailScout ist ein Lern- und Portfolio-Projekt und derzeit nicht für den produktiven Einsatz vorgesehen.

**Aktuelle Einschränkungen:**

- Keine Analyse von Dateianhängen
- Keine Überprüfung der tatsächlichen Absenderidentität
- Keine SPF-, DKIM- oder DMARC-Prüfung
- Keine Live-Abfrage von Domain-Reputation
- Keine vollständige Erkennung sämtlicher Phishing-Techniken
- Noch keine KI-basierte Analyse

Der Anwendungscode speichert eingegebene E-Mail-Inhalte nicht bewusst in einer Datenbank und leitet sie nicht an externe Analyse-APIs weiter.

Da MailScout öffentlich gehostet wird, sollten grundsätzlich keine vertraulichen, sensiblen oder personenbezogenen Inhalte eingegeben werden.

---

## 🗺️ Entwicklungsverlauf und Roadmap

### Version 0.1 – Grundlegender Prototyp

- [x] Regelbasierte E-Mail-Analyse
- [x] Erkennung verdächtiger Formulierungen
- [x] Einfache Risikobewertung
- [x] Erste Streamlit-Weboberfläche
- [x] Öffentliche Bereitstellung der Anwendung

### Version 0.2 – Erweiterte Sicherheitsanalyse

- [x] Erkennung von IPv4- und IPv6-Adressen in Links
- [x] Erkennung ausgewählter irreführender Subdomains
- [x] Prüfung auf Punycode-Kennzeichnungen
- [x] Entfernung pauschaler Risikopunkte für gewöhnliche Links
- [x] Verbesserung der Benutzeroberfläche
- [x] Automatisierte Tests mit pytest
- [x] GitHub Actions zur kontinuierlichen Qualitätssicherung

### Version 0.3 – Verbesserte Domainanalyse

- [ ] Zuverlässigere Bestimmung registrierbarer Domains
- [ ] Erkennung von Tippfehler-Domains (Typosquatting)
- [ ] Erweiterung der Sicherheitsregeln
- [ ] Zusätzliche automatische Tests
- [ ] Systematische Untersuchung von Fehlalarmen

### Version 0.4 – KI-Unterstützung

- [ ] Optionale KI-gestützte Erklärung von Warnsignalen
- [ ] Vergleich zwischen regelbasierter und KI-gestützter Analyse
- [ ] Untersuchung der Zuverlässigkeit und Grenzen des KI-Modells

### Version 1.0 – Evaluation und Dokumentation

- [ ] Aufbau eines strukturierten Testdatensatzes
- [ ] Messung von Precision und Recall
- [ ] Untersuchung der False-Positive-Rate
- [ ] Erweiterte Testabdeckung
- [ ] Sicherheitsüberprüfung und verbesserte Dokumentation

---

## 🛠️ Verwendete Technologien

| Technologie | Einsatzbereich |
|---|---|
| Python | Sicherheitslogik und Analyse |
| Streamlit | Weboberfläche |
| Reguläre Ausdrücke (Regex) | Erkennung von Textmustern |
| ipaddress | Prüfung von IPv4- und IPv6-Adressen |
| urllib.parse | Verarbeitung und Analyse von URLs |
| pytest | Automatisierte Softwaretests |
| GitHub Actions | Continuous Integration |
| GitHub | Versionsverwaltung und Dokumentation |
| Streamlit Community Cloud | Öffentliches Hosting |

---

## 🎯 Projektziel

MailScout wird als eigenständiges Cyber-Security-Portfolio-Projekt entwickelt, um praktische Kenntnisse in folgenden Bereichen aufzubauen:

- E-Mail-Sicherheit und Phishing-Erkennung
- Python-Programmierung
- Security Engineering
- Sichere Softwareentwicklung
- Automatisierte Qualitätssicherung
- Continuous Integration
- Nachvollziehbare Sicherheitsanalysen

Langfristig soll die Anwendung durch zusätzliche Erkennungsmethoden, erweiterte Tests und optionale KI-Unterstützung ausgebaut werden.

---

## ⚠️ Haftungshinweis

MailScout ist ein experimentelles Lernprojekt und kein zertifiziertes oder produktionsreifes Sicherheitsprodukt.

Die Ergebnisse dienen ausschließlich der Orientierung. Eine eigenständige Überprüfung verdächtiger E-Mails bleibt erforderlich.

**Eigenständig entwickeltes Cyber-Security-Portfolio-Projekt.**
