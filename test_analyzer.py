
from analyzer import analyze_email


def test_harmless_email():
    score, findings = analyze_email(
        "Hallo Max, vielen Dank für das Gespräch!"
    )

    assert score == 0
    assert len(findings) == 0


def test_normal_domain():
    score, findings = analyze_email(
        "Informationen: https://shop.amazon.de"
    )

    assert score == 0
    assert len(findings) == 0


def test_suspicious_subdomain():
    score, findings = analyze_email(
        "Bitte prüfen Sie https://amazon.de.login.example.com"
    )

    assert score == 25
    assert any(
        f.label == "Verdächtige Subdomain"
        for f in findings
    )


def test_ip_address():
    score, findings = analyze_email(
        "Bitte besuchen Sie http://192.0.2.15/login"
    )

    assert score == 25
    assert any(
        f.label == "IP-Adresse im Link"
        for f in findings
    )


def test_urgent_account_warning():
    score, findings = analyze_email(
        "Ihr Konto wird sofort gesperrt!"
    )

    assert score == 40
    assert len(findings) == 2
