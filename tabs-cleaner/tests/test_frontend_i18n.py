import unittest
from pathlib import Path


ADDON_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ADDON_ROOT / "rootfs" / "opt" / "tabs_cleaner" / "static"


class FrontendI18nTests(unittest.TestCase):
    def test_html_defaults_to_chinese_and_has_language_picker(self):
        html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")

        self.assertIn('<html lang="zh-CN">', html)
        self.assertIn('id="languageSelect"', html)

    def test_frontend_declares_chinese_and_english_catalogs(self):
        app_js = (STATIC_DIR / "app.js").read_text(encoding="utf-8")

        self.assertIn('DEFAULT_LOCALE = "zh-CN"', app_js)
        self.assertIn('"zh-CN":', app_js)
        self.assertIn('"en":', app_js)
        self.assertIn('"nav.smart": "智能清理"', app_js)
        self.assertIn('"nav.smart": "Smart Clean"', app_js)
        self.assertIn('"recommendation.recommended": "推荐清理"', app_js)
        self.assertIn('"recommendation.not_recommended": "Not recommended"', app_js)


if __name__ == "__main__":
    unittest.main()
