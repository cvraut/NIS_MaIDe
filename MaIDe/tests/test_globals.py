# globals.py

import os
import unittest
from MaIDe import globals

class TestModule(unittest.TestCase):
    def test_required_settings_can_be_loaded(self):
        required_settings = ["version", "contact", "maid_files_loc", "default_image_dir", "user", "dbfile"]
        assert all([rs in globals.__dict__ for rs in required_settings])

if __name__ == "__main__":
    unittest.main()