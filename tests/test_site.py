import html.parser
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ("index.html", "privacy.html", "terms.html")


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for key, value in attrs if key == "href")


class OAuthSiteTest(unittest.TestCase):
    def test_pages_exist_and_link_each_other(self):
        for page in PAGES:
            text = (ROOT / page).read_text(encoding="utf-8")
            links = Links()
            links.feed(text)
            self.assertIn("privacy.html", links.hrefs, page)
            self.assertIn("terms.html", links.hrefs, page)
            self.assertIn("index.html", links.hrefs, page)

    def test_home_describes_actual_google_integrations(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for word in ("Gmail", "Calendar", "Drive", "Sheets", "Docs", "Contacts", "Google Health"):
            self.assertIn(word, html)
        self.assertIn("personal", html.lower())

    def test_privacy_describes_actual_data_flows(self):
        html = (ROOT / "privacy.html").read_text(encoding="utf-8").lower()
        for word in ("oauth", "local", "ai provider", "telegram", "revoke", "not sold"):
            self.assertIn(word, html)

    def test_no_personal_records_or_secrets_in_public_pages(self):
        for page in PAGES:
            text = (ROOT / page).read_text(encoding="utf-8")
            for forbidden in ("refresh_token", "client_secret", "asafmagen28.github", "myfitnesspal"):
                self.assertNotIn(forbidden, text.lower())


if __name__ == "__main__":
    unittest.main()
