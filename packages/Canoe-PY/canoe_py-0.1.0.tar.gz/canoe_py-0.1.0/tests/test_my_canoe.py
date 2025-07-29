"""
Tests for the MyCANoe library
"""

import unittest
import os
import sys

# Add the parent directory to the path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_canoe_lib import MyCANoe, MyCANoeException

class TestMyCANoe(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.canoe = MyCANoe()
        except MyCANoeException:
            self.skipTest("CANoe not running or accessible")
    
    def test_get_version(self):
        """Test getting CANoe version"""
        version = self.canoe.get_version()
        self.assertIsNotNone(version)
        self.assertIsInstance(version, str)
        # Version should be in format like "15.6.6"
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
    
    def test_get_status(self):
        """Test getting CANoe status"""
        status = self.canoe.get_status()
        self.assertIsNotNone(status)
        self.assertIsInstance(status, dict)
        self.assertIn("version", status)
        self.assertIn("measurement_running", status)
        self.assertIn("configuration", status)
        self.assertIn("timestamp", status)
    
    def test_is_measurement_running(self):
        """Test checking if measurement is running"""
        is_running = self.canoe.is_measurement_running()
        self.assertIsInstance(is_running, bool)
    
    def tearDown(self):
        """Tear down test fixtures"""
        if hasattr(self, 'canoe'):
            self.canoe.close()

if __name__ == "__main__":
    unittest.main()