# test_dependency_installer.py

import os
import unittest
from MaIDe import dependency_installer

class TestModule(unittest.TestCase):
    def test_check_predownloaded_packages(self):
        predowloaded_packages = dependency_installer.grab_predownloaded_dependencies()
        intended_predownloads = ['certifi', 'charset_normalizer', 'idna', 'requests', 'toml', 'urllib3']
        for pkg in intended_predownloads:
            self.assertIn(pkg, predowloaded_packages)

if __name__ == "__main__":
    unittest.main()