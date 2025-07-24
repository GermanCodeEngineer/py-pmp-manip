# conftest.py
from pypenguin.config import init_config, get_default_config

def pytest_configure(config):
    init_config(get_default_config())
