from pytest import raises

from pypenguin.utility import ConversionError

from pypenguin.core.enums import SRTTSLanguage, SRVideoState, SRSpriteRotationStyle, SRVariableMonitorReadoutMode



def test_SRTTSLanguage_from_code():
    assert SRTTSLanguage.from_code("zh-cn") == SRTTSLanguage.CHINESE_MANDARIN

def test_SRTTSLanguage_from_code_invalid():
    with raises(ConversionError):
        SRTTSLanguage.from_code("something undefined")



def test_SRVideoState_from_code():
    assert SRVideoState.from_code("on flipped") == SRVideoState.ON_FLIPPED

def test_SRVideoState_from_code_invalid():
    with raises(ConversionError):
        SRVideoState.from_code("something undefined")



def test_SRSpriteRotationStyle_from_code():
    assert SRSpriteRotationStyle.from_code("left-right") == SRSpriteRotationStyle.LEFT_RIGHT

def test_SRSpriteRotationStyle_from_code_invalid():
    with raises(ConversionError):
        SRSpriteRotationStyle.from_code("something undefined")



def test_SRVariableMonitorReadoutMode_from_code():
    assert SRVariableMonitorReadoutMode.from_code("default") == SRVariableMonitorReadoutMode.NORMAL

def test_SRVariableMonitorReadoutMode_from_code_invalid():
    with raises(ConversionError):
        SRVariableMonitorReadoutMode.from_code("something undefined")


