from pytest import fixture, raises

from pypenguin.utility import ThanksError

from pypenguin.core.monitor import FRMonitor



def test_FRMonitor_post_init():
    with raises(ThanksError):
        FRMonitor(
            
        )



