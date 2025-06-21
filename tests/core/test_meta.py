from pytest import raises

from pypenguin.utility import ThanksError

from pypenguin.core.meta import FRMeta, FRPenguinModPlatformMeta, PENGUINMOD_META_DATA, SCRATCH_META_DATA



def test_FRMeta_from_data_penguinmod():
    meta_data = PENGUINMOD_META_DATA
    meta = FRMeta.from_data(meta_data)
    assert isinstance(meta, FRMeta)
    assert meta.semver == meta_data["semver"]
    assert meta.vm == meta_data["vm"]
    assert meta.agent == meta_data["agent"]
    assert isinstance(meta.platform, FRPenguinModPlatformMeta)

def test_FRMeta_from_data_scratch():
    meta_data = SCRATCH_META_DATA
    meta = FRMeta.from_data(meta_data)
    assert isinstance(meta, FRMeta)
    assert meta.semver == meta_data["semver"]
    assert meta.vm == meta_data["vm"]
    assert meta.agent == meta_data["agent"]
    assert meta.platform is None

def test_FRMeta_from_data_post_init_invalid():
    with raises(ThanksError):
        FRMeta.from_data(PENGUINMOD_META_DATA | {"semver": "2.0.0"})
    with raises(ThanksError):
        FRMeta.from_data(PENGUINMOD_META_DATA | {"vm": "5.0.0"})


def test_FRMeta_new_scratch_meta():
    assert FRMeta.new_scratch_meta() == FRMeta.from_data(SCRATCH_META_DATA)


def test_FRMeta_new_penguinmod_meta():
    assert FRMeta.new_penguinmod_meta() == FRMeta.from_data(PENGUINMOD_META_DATA)


def test_FRPenguinModPlatformMeta_from_data():
    platform_meta_data = PENGUINMOD_META_DATA["platform"]
    platform_meta = FRPenguinModPlatformMeta.from_data(platform_meta_data)
    assert isinstance(platform_meta, FRPenguinModPlatformMeta)
    assert platform_meta.name == platform_meta_data["name"]
    assert platform_meta.url == platform_meta_data["url"]
    assert platform_meta.version == platform_meta_data["version"]

def test_FRPenguinModPlatformMeta_from_data_invalid():
    with raises(ThanksError):
        FRPenguinModPlatformMeta.from_data(PENGUINMOD_META_DATA["platform"] | {"name": "MyScratchMod"})
    with raises(ThanksError):
        FRPenguinModPlatformMeta.from_data(PENGUINMOD_META_DATA["platform"] | {"url": "https://my.scratchmod/"})
    with raises(ThanksError):
        FRPenguinModPlatformMeta.from_data(PENGUINMOD_META_DATA["platform"] | {"version": "99.12.34"})

