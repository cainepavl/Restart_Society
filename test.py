import os
import shutil
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the functions from your main script
# Assuming your script is named vital_download.py
import vital_download as vd

class TestVitalArchiver(unittest.TestCase):

    def setUp(self):
        """Set up a dummy environment for testing."""
        vd.BASE_DIR = "./test_vital_articles/"
        vd.TEMP_DIR = os.path.join(vd.BASE_DIR, "current_run")
        vd.LOG_FILE = os.path.join(vd.BASE_DIR, "download_log.json")
        
        if not os.path.exists(vd.BASE_DIR):
            os.makedirs(vd.BASE_DIR)

    def tearDown(self):
        """Clean up the dummy environment after tests."""
        if os.path.exists(vd.BASE_DIR):
            shutil.rmtree(vd.BASE_DIR)

    def test_disk_space_pass(self):
        """Verify check_disk_space returns True when limit is high."""
        vd.MAX_DISK_USAGE_MB = 9999999 # Setting a huge limit
        self.assertTrue(vd.check_disk_space())

    def test_disk_space_fail(self):
        """Verify check_disk_space returns False when limit is exceeded."""
        vd.MAX_DISK_USAGE_MB = 0 # Force a fail
        self.assertFalse(vd.check_disk_space())

    @patch('vital_download.requests.get')
    def test_get_article_list(self, mock_get):
        """Mock the Wikipedia list page and check if it parses titles correctly."""
        mock_html = """
        <div id="mw-content-text">
            <a href="/wiki/Earth" title="Earth">Earth</a>
            <a href="/wiki/Biology" title="Biology">Biology</a>
            <a href="/wiki/Wikipedia:Vital_articles/Level/3" title="Level 3">Link to avoid</a>
        </div>
        """
        mock_get.return_value.text = mock_html
        articles = vd.get_article_list()
        
        self.assertIn("Earth", articles)
        self.assertIn("Biology", articles)
        self.assertNotIn("Level 3", articles) # Should be filtered out by the 'Level/3' check

    @patch('vital_download.requests.get')
    def test_download_article(self, mock_get):
        """Verify the API download returns the correct content and ETag."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>Content</html>"
        mock_response.headers = {'ETag': '12345'}
        mock_get.return_value = mock_response
        
        content, etag = vd.download_article("Earth")
        self.assertEqual(content, "<html>Content</html>")
        self.assertEqual(etag, "12345")

    def test_zip_creation(self):
        """Manually trigger the zipping logic to ensure files are bundled and deleted."""
        # 1. Create a dummy file in the temp directory
        os.makedirs(vd.TEMP_DIR, exist_ok=True)
        dummy_file = os.path.join(vd.TEMP_DIR, "test_article.html")
        with open(dummy_file, "w") as f:
            f.write("test data")

        # 2. Run a simplified version of the zip logic
        timestamp = datetime.now().strftime("%Y-%m-%d")
        zip_name = f"test_archive_{timestamp}.zip"
        zip_path = os.path.join(vd.BASE_DIR, zip_name)

        with vd.zipfile.ZipFile(zip_path, 'w', vd.zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(vd.TEMP_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file)
                    os.remove(file_path)

        # 3. Assertions
        self.assertTrue(os.path.exists(zip_path))
        self.assertFalse(os.path.exists(dummy_file)) # File should be deleted after zipping

if __name__ == "__main__":
    unittest.main()
