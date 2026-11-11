"""MailScout v0.1: interactive rule-based phishing demo built with Streamlit."""

import streamlit as st
from analyzer import analyze_email, risk_level

EXAMPLE = """Betreff: Ihr Konto wird sofort gesperrt!

Bitte bestätigen Sie Ihre Zugangsdaten innerhalb von 24 Stunden.
Öffnen Sie dazu https://login-konto.example/verify
"""

st.set_page_config(page_title="MailScout | E-Mail-Sicherheitscheck", page_icon="🛡️", layout="centered")

st.title("🛡️ MailScout")
st.caption("Ein erklärbarer Phishing-Analyzer · Portfolio-Demo v0.1")
st.write(
    "Prüfe eine **fiktive E-Mail** auf einfache Phishing-Warnsignale. "
    "Dieses Lernprojekt verwendet bislang **Regeln, keine KI**."
)

with st.form("analyze_form"):
    message = st.text_area(
        "E-Mail-Text",
        value=EXAMPLE,
        height=200,
        max_chars=20000,
        help="Keine echten vertraulichen E-Mails oder Zugangsdaten eingeben.",
    )
    submitted = st.form_submit_button("🔎 E-Mail prüfen", type="primary", use_container_width=True)

if submitted:
    if not message.strip():
        st.warning("Bitte gib zuerst einen E-Mail-Text ein.")
    else:
        score, findings = analyze_email(message)
        st.subheader("Analyseergebnis")
        st.metric("Heuristischer Auffälligkeitswert", f"{score} / 100")
        st.progress(score / 100)
        st.write(f"**Einstufung:** {risk_level(score)}")
        st.caption("Der Wert ist keine Wahrscheinlichkeit und beweist weder Phishing noch Sicherheit.")

        if findings:
            st.write("**Gefundene Warnsignale**")
            for finding in findings:
                with st.expander(f"⚠️ {finding.label} (+{finding.points})", expanded=True):
                    st.write(finding.explanation)
        else:
            st.info("Keine der aktuell programmierten Regeln hat angeschlagen. Das bedeutet nicht, dass die E-Mail sicher ist.")

        st.divider()
        st.write("**Sicher handeln:** Keine Links aus verdächtigen Nachrichten öffnen, sondern die offizielle Website selbst aufrufen und Absender bzw. Anfrage unabhängig prüfen.")

st.divider()
st.caption("Lokal analysiert durch Python-Regeln. Keine E-Mails werden durch den App-Code gespeichert oder weitergeleitet. Bei öffentlichem Hosting keine vertraulichen Inhalte eingeben.")
