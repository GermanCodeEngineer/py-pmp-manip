from pytest import fixture

from pypenguin.config import init_config, get_default_config


@fixture(scope="session", autouse=True)
def setup_config():
    init_config(get_default_config())
    raise Exception()

raise Exception()
