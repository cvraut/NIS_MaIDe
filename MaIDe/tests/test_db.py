# test_db.py

import os
import unittest
from MaIDe import globals
from MaIDe import db

class TestModule(unittest.TestCase):
    def test_no_db_file(self):
        # delete the dbfile if it exists
        try:
            os.remove(globals.dbfile)
        except FileNotFoundError:
            pass
        last_run_status = db.get_last_run_status(globals.dbfile)
        self.assertEqual(last_run_status, {})

if __name__ == "__main__":
    unittest.main()