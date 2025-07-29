import logging

import pytest

from crewai_mcp_toolbox.utils import MCPConfiguration


def test_valid_timeout_override():
    config = MCPConfiguration({"worker_startup_timeout": 10})
    assert config.worker_startup_timeout == 10


def test_invalid_timeout_does_not_override():
    config = MCPConfiguration({"worker_startup_timeout": -5})
    assert (
        config.worker_startup_timeout
        == MCPConfiguration.DEFAULT_CONFIG["worker_startup_timeout"]
    )


def test_non_timeout_negative_ignored_without_warning(caplog):
    caplog.set_level(logging.WARNING)
    config = MCPConfiguration({"some_value": -5})
    assert "some_value" not in config._config
    # Ensure no invalid timeout warning emitted for non-timeout key
    assert not any("Invalid timeout" in rec.message for rec in caplog.records)


def test_health_check_interval_property():
    config = MCPConfiguration()
    assert config.health_check_interval == 10.0

    config = MCPConfiguration({"health_check_interval": 20.0})
    assert config.health_check_interval == 20.0
