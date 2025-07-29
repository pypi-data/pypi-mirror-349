import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any
from typing import Dict

from pycmd2.common.settings import (
    Settings,  # Assuming the class is named SettingsManager
)


class SettingsTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_init_with_existing_config_file(self):
        """Test initialization when config file exists"""
        # Create a config file with test data
        config_data: Dict[str, Any] = {"key1": "value1", "key2": 42}
        config_file = self.config_dir / "config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)

        # Initialize with default config that shouldn't be used
        default_config = {"should": "not_be_used"}
        settings = Settings(self.config_dir, default_config)

        # Verify config was loaded from file, not default
        self.assertEqual(settings.config, config_data)
        self.assertNotEqual(settings.config, default_config)


if __name__ == "__main__":
    unittest.main()
