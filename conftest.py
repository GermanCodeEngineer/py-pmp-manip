# conftest.py
from pmp_manip.config import init_config, get_default_config

def pytest_configure(config):
    init_config(get_default_config())
