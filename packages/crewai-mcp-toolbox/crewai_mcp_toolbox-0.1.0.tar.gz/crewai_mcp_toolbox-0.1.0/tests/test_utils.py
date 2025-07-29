# src/crewai_mcp_toolbox/tests/test_utils.py
import logging
import unittest

from crewai_mcp_toolbox.utils import MCPConfiguration


class MCPConfigurationTests(unittest.TestCase):
    def test_valid_timeout_override(self):
        config = MCPConfiguration({"worker_startup_timeout": 120})
        self.assertEqual(config.worker_startup_timeout, 120)

    def test_invalid_timeout_negative(self):
        default = MCPConfiguration.DEFAULT_CONFIG["worker_startup_timeout"]
        with self.assertLogs(level="WARNING") as cm:
            config = MCPConfiguration({"worker_startup_timeout": -5})
        self.assertEqual(config.worker_startup_timeout, default)
        self.assertIn("Invalid timeout value", "".join(cm.output))

    def test_invalid_timeout_type(self):
        default = MCPConfiguration.DEFAULT_CONFIG["worker_startup_timeout"]
        with self.assertLogs(level="WARNING") as cm:
            config = MCPConfiguration({"worker_startup_timeout": "bad"})
        self.assertEqual(config.worker_startup_timeout, default)
        self.assertIn("Invalid timeout value", "".join(cm.output))

    def test_health_check_interval(self):
        config = MCPConfiguration()
        self.assertEqual(config.health_check_interval, 10.0)

        config = MCPConfiguration({"health_check_interval": 5.0})
        self.assertEqual(config.health_check_interval, 5.0)


if __name__ == "__main__":
    unittest.main()
