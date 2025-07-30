from pytest import raises

from pmp_manip.utility import PP_ConversionError


from pmp_manip.core.enums import SRCodeEnum



class DummyEnum(SRCodeEnum):
    GÜNTHER_JAUCH = "gj"
    DIETER_BOHLEN = "dibo"
    


def test_SRCodeEnum_from_code():
    assert DummyEnum.from_code("gj"  ) == DummyEnum.GÜNTHER_JAUCH
    assert DummyEnum.from_code("dibo") == DummyEnum.DIETER_BOHLEN

def test_SRCodeEnum_from_code_invalid():
    with raises(PP_ConversionError):
        DummyEnum.from_code("something undefined")


def test_SRCodeEnum_to_code():
    assert DummyEnum.GÜNTHER_JAUCH.to_code() == "gj"
    assert DummyEnum.DIETER_BOHLEN.to_code() == "dibo"

from pmp_manip.core.enums import SRTTSLanguage, SRVideoState, SRSpriteRotationStyle, SRVariableMonitorReadoutMode



def test_SRTTSLanguage_from_code():
    assert SRTTSLanguage.from_code("zh-cn") == SRTTSLanguage.CHINESE_MANDARIN

def test_SRTTSLanguage_from_code_invalid():
    with raises(PP_ConversionError):
        SRTTSLanguage.from_code("something undefined")



def test_SRVideoState_from_code():
    assert SRVideoState.from_code("on flipped") == SRVideoState.ON_FLIPPED

def test_SRVideoState_from_code_invalid():
    with raises(PP_ConversionError):
        SRVideoState.from_code("something undefined")



def test_SRSpriteRotationStyle_from_code():
    assert SRSpriteRotationStyle.from_code("left-right") == SRSpriteRotationStyle.LEFT_RIGHT

def test_SRSpriteRotationStyle_from_code_invalid():
    with raises(PP_ConversionError):
        SRSpriteRotationStyle.from_code("something undefined")



def test_SRVariableMonitorReadoutMode_from_code():
    assert SRVariableMonitorReadoutMode.from_code("default") == SRVariableMonitorReadoutMode.NORMAL

def test_SRVariableMonitorReadoutMode_from_code_invalid():
    with raises(PP_ConversionError):
        SRVariableMonitorReadoutMode.from_code("something undefined")


