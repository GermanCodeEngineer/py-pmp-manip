from pytest import fixture

from pypenguin.utility import ValidationConfig, TypeValidationError

from pypenguin.core.asset import FRCostume, FRSound, SRCostume, SRSound

from tests.utility import execute_attr_validation_tests

@fixture
def config():
    return ValidationConfig()


# FRCostume
RAW_COSTUME_DATA_1 = {
    "name": "my costume", 
    "assetId": "051321321c93ae7b61222de62e77ae40", 
    "dataFormat": "svg", 
    "md5ext": "051321321c93ae7b61222de62e77ae40.svg", 
    "rotationCenterX": 381.2306306306307, 
    "rotationCenterY": 197.11651651651664,
    "bitmapResolution": 1, 
}
RAW_COSTUME_DATA_2 = {
    "name": "my costume", 
    "assetId": "051321321c93ae7b61222de62e77ae40", 
    "dataFormat": "svg", 
    "md5ext": "051321321c93ae7b61222de62e77ae40.svg", 
    "rotationCenterX": 381.2306306306307, 
    "rotationCenterY": 197.11651651651664,
}

def test_frcostume_from_data():
    costume_data = RAW_COSTUME_DATA_1
    costume = FRCostume.from_data(costume_data)
    assert isinstance(costume, FRCostume)
    assert costume.name == costume_data["name"]
    assert costume.asset_id == costume_data["assetId"]
    assert costume.data_format == costume_data["dataFormat"]
    assert costume.md5ext == costume_data["md5ext"]
    assert costume.rotation_center_x == costume_data["rotationCenterX"]
    assert costume.rotation_center_y == costume_data["rotationCenterY"]
    assert costume.bitmap_resolution == costume_data["bitmapResolution"]

def test_frcostume_from_data_bitmap_resolution():
    costume_data = RAW_COSTUME_DATA_2
    costume = FRCostume.from_data(costume_data)
    assert costume.bitmap_resolution == None

def test_frcostume_step():
    frcostume = FRCostume.from_data(RAW_COSTUME_DATA_1)
    srcostume = frcostume.step()
    assert isinstance(srcostume, SRCostume)
    assert srcostume.name == frcostume.name
    assert srcostume.file_extension == frcostume.data_format
    assert srcostume.rotation_center == (frcostume.rotation_center_x, frcostume.rotation_center_y)
    assert srcostume.bitmap_resolution == frcostume.bitmap_resolution

def test_frcostume_step_bitmap_resolution():
    frcostume = FRCostume.from_data(RAW_COSTUME_DATA_2)
    srcostume = frcostume.step()
    assert srcostume.bitmap_resolution == 1

# FRSound
RAW_SOUND_DATA = {
    "name": "pop", 
    "assetId": "83a9787d4cb6f3b7632b4ddfebf74367", 
    "dataFormat": "wav",
    "md5ext": "83a9787d4cb6f3b7632b4ddfebf74367.wav", 
    "rate": 48000, 
    "sampleCount": 1123, 
}

def test_frsound_from_data():
    sound_data = RAW_SOUND_DATA
    sound = FRSound.from_data(sound_data)
    assert isinstance(sound, FRSound)
    assert sound.name == sound_data["name"]
    assert sound.asset_id == sound_data["assetId"]
    assert sound.data_format == sound_data["dataFormat"]
    assert sound.md5ext == sound_data["md5ext"]
    assert sound.rate == sound_data["rate"]
    assert sound.sample_count == sound_data["sampleCount"]

def test_frsound_step():
    frsound = FRSound.from_data(RAW_SOUND_DATA)
    srsound = frsound.step()
    assert isinstance(srsound, SRSound)
    assert srsound.name == frsound.name
    assert srsound.file_extension == frsound.data_format

# SRCostume
def test_srcostume_validate(config):
    costume = SRCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(-20, 15.6),
        bitmap_resolution=1,
    )
    costume.validate(path=[], config=config)
    
    execute_attr_validation_tests(
        obj=costume,
        attr_tests=[
            ("name", 5, TypeValidationError),
            ("file_extension", {}, TypeValidationError),
            ("rotation_center", [], TypeValidationError),
            ("bitmap_resolution", "hi", TypeValidationError),
        ],
        validate_func=SRCostume.validate,
        func_args=[[], config],
    )

# SRSound
def test_srsound_validate(config):
    sound = SRSound(
        name="Hello there!",
        file_extension="wav",
    )
    sound.validate(path=[], config=config)
    
    execute_attr_validation_tests(
        obj=sound,
        attr_tests=[
            ("name", 5, TypeValidationError),
            ("file_extension", {}, TypeValidationError),
        ],
        validate_func=SRSound.validate,
        func_args=[[], config],
    )
