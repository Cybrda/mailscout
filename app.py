
"""MailScout – Explainable Email Security Analyzer."""

import re
import streamlit as st

from analyzer import analyze_email, risk_level, URL_PATTERN


st.set_page_config(
    page_title="MailScout | Email Security Analyzer",
    page_icon="🛡️",
    layout="centered",
)

EXAMPLE = """Betreff: Ihr Konto wird sofort gesperrt!

Bitte bestätigen Sie Ihre Zugangsdaten innerhalb von 24 Stunden.
Öffnen Sie dazu https://login-konto.example/verify
"""


# ---------------------------------------
# 1. Kopfbereich
# ---------------------------------------

st.title("🛡️ MailScout")
st.caption("Email Security Analyzer | Version 0.2")

st.write(
    "Analysiere E-Mail-Texte auf mögliche Phishing-Merkmale. "
    "MailScout verwendet aktuell **regelbasierte Sicherheitsprüfungen**."
)


# ---------------------------------------
# 2. E-Mail-Eingabe
# ---------------------------------------

with st.form("analyze_form"):

    message = st.text_area(
        "E-Mail-Text eingeben",
        value=EXAMPLE,
        height=200,
        max_chars=20000,
        help="Bitte keine vertraulichen E-Mails oder Zugangsdaten eingeben.",
    )

    submitted = st.form_submit_button(
        "🔎 E-Mail analysieren",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------
# 3. Sicherheitsanalyse
# ---------------------------------------

if submitted:

    if not message.strip():
        st.warning("Bitte zuerst einen E-Mail-Text eingeben.")

    else:

        score, findings = analyze_email(message)

        st.divider()
        st.subheader("📊 Analyseergebnis")

        st.metric(
            label="Auffälligkeitswert",
            value=f"{score} / 100",
        )

        st.progress(score / 100)

        # Risikostufe anzeigen
        if score >= 60:
            st.error("🔴 Erhöhte Auffälligkeit")

        elif score >= 25:
            st.warning("🟠 Einige Auffälligkeiten")

        else:
            st.success("🟢 Wenige Auffälligkeiten")

        st.caption(
            "Die Bewertung basiert auf einfachen Regeln. "
            "Der Score ist keine statistische Wahrscheinlichkeit."
        )

        # ---------------------------------------
        # 4. Erkannte Sicherheitswarnungen
        # ---------------------------------------

        st.subheader("🛡️ Sicherheitswarnungen")

        if findings:

            for finding in findings:

                with st.expander(
                    f"⚠️ {finding.label} (+{finding.points})",
                    expanded=True,
                ):
                    st.write(finding.explanation)

        else:
            st.info(
                "Keine Auffälligkeiten anhand der aktuellen "
                "Prüfregeln erkannt. Das bedeutet nicht, "
                "dass die E-Mail garantiert sicher ist."
            )

        # ---------------------------------------
        # 5. Neutrale Informationen
        # ---------------------------------------

        st.subheader("ℹ️ Weitere Informationen")

        urls = [
            url.rstrip(".,;!?)")
            for url in URL_PATTERN.findall(message)
        ]

        st.write(f"**Gefundene Links:** {len(urls)}")

        if urls:
            st.info(
                "Links sind nicht grundsätzlich verdächtig. "
                "MailScout bewertet konkrete Auffälligkeiten "
                "wie direkte IP-Adressen oder irreführende Domains."
            )

            for index, url in enumerate(urls, start=1):
                st.code(f"{index}. {url}", language=None)

        else:
            st.write("Keine HTTP- oder HTTPS-Links gefunden.")

        # ---------------------------------------
        # 6. Sicherheitsempfehlungen
        # ---------------------------------------

        st.divider()
        st.subheader("💡 Sicherheitsempfehlungen")

        st.write(
            "• Prüfe die tatsächliche Domain von Links.\n"
            "• Gib Zugangsdaten nicht über ungeprüfte Links ein.\n"
            "• Öffne bei Unsicherheit die offizielle Website selbst.\n"
            "• Überprüfe ungewöhnliche Anfragen unabhängig."
        )

        st.caption(
            "MailScout untersucht derzeit nur Text und bestimmte "
            "URL-Merkmale. Es prüft keine Anhänge, tatsächlichen "
            "Absenderidentitäten oder die Reputation von Domains."
        )


# ---------------------------------------
# 7. Fußbereich
# ---------------------------------------

st.divider()

st.caption(
    "MailScout v0.2 | Python & Streamlit | "
    "Open-Source-Portfolio-Projekt"
)

st.caption(
    "Die Analyse erfolgt durch Python-Regeln. "
    "Der Anwendungscode speichert oder versendet keine E-Mail-Inhalte. "
    "Bei öffentlichem Hosting keine vertraulichen Daten eingeben."
)
