import http.client
import threading
import unittest
from pathlib import Path

from app import make_server


class AppServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def fetch(self, path):
        connection = http.client.HTTPConnection("127.0.0.1", self.port)
        connection.request("GET", path)
        response = connection.getresponse()
        body = response.read()
        connection.close()
        return response, body

    def test_home_serves_encounter_product(self):
        response, body = self.fetch("/")
        self.assertEqual(response.status, 200)
        self.assertIn(b"Encounter a Penguin", body)
        self.assertNotIn(b"Find a Penguin", body)
        self.assertEqual(response.getheader("Cache-Control"), "no-store")
        self.assertIn(b'href="./"', body)

    def test_public_professor_derivative_is_present_without_raw_source(self):
        derivative = Path("assets/professor-adelie-transparent.png")
        self.assertTrue(derivative.is_file())
        self.assertGreater(derivative.stat().st_size, 500_000)
        self.assertTrue(derivative.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertFalse(Path("assets/source").exists())

    def test_ui_contains_complete_encounter_loop(self):
        markup = Path("index.html").read_text()
        script = Path("app-ui.js").read_text()
        self.assertIn("Encounter a Penguin", markup)
        self.assertIn("Save this encounter", markup)
        self.assertIn("Professor Adelie is visiting", script)
        self.assertIn("Professor Adelie is leaving", script)
        self.assertIn("toBlob", script)
        self.assertIn('if(side==="left")', script)
        self.assertIn("professor-adelie-transparent.png", script)
        self.assertNotIn("professor-adelie-transparent.svg", script)
        self.assertIn('download hidden', markup)
        self.assertNotIn("Penguinness", markup + script)
        self.assertNotIn("Give me a hint", markup + script)

    def test_javascript_and_asset_have_correct_content_types(self):
        js_response, _ = self.fetch("/app-ui.js")
        png_response, png = self.fetch("/assets/professor-adelie-transparent.png")
        self.assertIn("javascript", js_response.getheader("Content-Type"))
        self.assertIn("png", png_response.getheader("Content-Type"))
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_missing_file_is_404(self):
        response, _ = self.fetch("/not-here")
        self.assertEqual(response.status, 404)

    def test_cloud_deployment_workflow_is_main_driven(self):
        workflow = Path(".github/workflows/deploy-pages.yml").read_text()
        self.assertIn("branches: [main]", workflow)
        self.assertIn("python3 scripts/build_static.py", workflow)
        self.assertIn("actions/upload-pages-artifact@v4", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)
        self.assertIn("path: dist", workflow)


if __name__ == "__main__":
    unittest.main()
