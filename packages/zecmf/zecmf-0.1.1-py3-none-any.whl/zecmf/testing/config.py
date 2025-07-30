"""Used by ZecMF-internal tests as app_config_module."""

from zecmf.config.base import BaseTestingConfig


class TestingConfig(BaseTestingConfig):
    """Testing configuration for unit and integration tests."""

    pass
