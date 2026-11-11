"""Run: python -m unittest discover -s tests -v"""

import unittest
from analyzer import analyze_email, risk_level


class AnalyzerTests(unittest.TestCase):
    def test_empty_message(self):
        self.assertEqual(analyze_email(""), (0, []))

    def test_normal_message(self):
        score, findings = analyze_email("Hallo, unser Treffen ist morgen um 14 Uhr.")
        self.assertEqual(score, 0)
        self.assertEqual(findings, [])

    def test_suspicious_message(self):
        score, findings = analyze_email(
            "Ihr Konto wird sofort gesperrt! Bitte bestätigen Sie Ihr Passwort. "
            "https://login-konto.example/verify"
        )
        self.assertGreater(score, 0)
        self.assertTrue(any(f.label == "Zeitdruck" for f in findings))

    def test_punycode(self):
        score, findings = analyze_email("Besuche https://xn--example-9za.test")
        self.assertTrue(any(f.label == "Punycode-Domain" for f in findings))

    def test_score_is_bounded(self):
        text = (
            "Sofort! Ihr Konto wird gesperrt. Passwort eingeben! "
            "https://xn--fake-1xa.test https://another.example https://third.example"
        )
        score, _ = analyze_email(text)
        self.assertLessEqual(score, 100)

    def test_labels(self):
        self.assertEqual(risk_level(0), "Wenige Auffälligkeiten")
        self.assertEqual(risk_level(60), "Erhöhte Auffälligkeit")


if __name__ == "__main__":
    unittest.main()
