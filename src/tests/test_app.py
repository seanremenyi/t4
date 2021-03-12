import unittest
from app import app

class TestappClass(unittest.TestCase):
    """Test app.py"""

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_files_page(self):
        response = self.app.get('/files', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_scan_page(self):
        response = self.app.get('/scan', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()