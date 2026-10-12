import html.parser
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        self.urls += [v for k, v in attrs if k in ('href', 'src')]

class NextModeSiteTest(unittest.TestCase):
    def test_pages_and_local_links(self):
        for name in ('index.html', 'privacy.html', 'data-deletion.html'):
            path = ROOT / 'nextmode' / name
            text = path.read_text()
            self.assertIn('NextMode', text)
            self.assertIn('asafmagen28@gmail.com', text)
            parser = Parser()
            parser.feed(text)
            for url in parser.urls:
                if not url.startswith(('https:', 'mailto:', '#')):
                    self.assertTrue((path.parent / url).is_file(), url)
            for forbidden in ('—', '–', '־', 'NEXTMODE_IG_ACCESS_TOKEN=', '<script', 'client_secret='):
                self.assertNotIn(forbidden, text)

    def test_privacy_is_specific_and_honest(self):
        text = (ROOT / 'nextmode/privacy.html').read_text()
        for phrase in ('@nextmode.il', 'Meta', 'configured AI service', 'Telegram', 'backups', 'no automatic fixed retention', 'currently being configured and tested'):
            self.assertIn(phrase, text)

    def test_manual_deletion_instructions(self):
        text = (ROOT / 'nextmode/data-deletion.html').read_text()
        for phrase in ('handled manually', 'Instagram username', 'password', 'status', 'does not automatically erase'):
            self.assertIn(phrase, text)

if __name__ == '__main__':
    unittest.main()
