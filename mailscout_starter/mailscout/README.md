# 🛡️ MailScout

**MailScout** ist eine kleine, erklärbare Demo zur Erkennung einfacher Phishing-Merkmale in E-Mail-Texten.

> **Version 0.1 ist regelbasiert, nicht KI-basiert.** Ein hoher Score beweist kein Phishing; ein niedriger Score bedeutet nicht, dass eine E-Mail sicher ist. Die Punktwerte sind nicht kalibriert.

## Was kann es?

- Erkennen von Zeitdruck, angedrohter Kontosperrung und Aufforderungen zu Zugangsdaten
- Hinweise auf externe Links und Punycode-Domains
- Einfache heuristische Bewertung mit Erklärungen
- Browser-Oberfläche mit Streamlit
- Automatisierte Unit-Tests (inklusive GitHub Actions)

## Lokal starten (Windows)

1. Installiere Python 3.12 und VS Code.
2. Öffne den Projektordner in VS Code, dann **Terminal → Neues Terminal**.
3. Gib nacheinander ein:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Falls du eine andere unterstützte Python-Version installiert hast, nutze statt `py -3.12` einfach `py`.

Streamlit öffnet normalerweise `http://localhost:8501`.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## GitHub und Live-Demo

1. Repository `mailscout` auf GitHub erstellen.
2. Dateien hochladen (auch `.github/workflows/tests.yml`; **nicht** `.venv`, `.env` oder Zugangsdaten).
3. Auf https://share.streamlit.io/ anmelden und **Create app** auswählen.
4. Repository, Branch `main`, Entry Point `app.py` auswählen, dann **Deploy**.
5. Die ausgegebene `*.streamlit.app`-URL im GitHub-Repository unter **About → Website** und im Lebenslauf ergänzen.

## Sicherheits- und Datenschutz-Hinweise

- Keine echten privaten oder geschäftlich vertraulichen E-Mails eingeben.
- App lädt keine Ziel-URLs herunter und klickt keine Links.
- Die App selbst schreibt eingegebene Texte nicht in Dateien oder Datenbanken; öffentliche Hosting-Infrastruktur ist trotzdem kein Ort für vertrauliche Daten.
- Für den produktiven Einsatz wären deutlich umfangreichere Validierung, Tests, Datenschutzmaßnahmen und Evaluierung notwendig.

## Roadmap

- [x] Version 0.1: Regelbasierte Textanalyse
- [x] Unit-Tests und GitHub Actions
- [ ] Version 0.2: Mehr Regeln und echte Tests mit synthetischen Beispielen
- [ ] Version 0.3: Optional lokales KI-Modell zur Erklärung von Befunden
- [ ] Version 1.0: Messbare Evaluation (Precision, Recall, False Positives) mit geeignetem Testdatensatz

## Tech Stack

Python · Streamlit · unittest · GitHub Actions
