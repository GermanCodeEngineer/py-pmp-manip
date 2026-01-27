from datetime     import datetime, timedelta, timezone
from json         import loads, dumps, JSONDecodeError
from logging      import getLogger
from os           import path, makedirs
from pathlib      import Path
from pytest       import raises, fixture, mark, MonkeyPatch
from types        import SimpleNamespace
from typing       import Any

from pmp_manip.config          import get_config, init_config, get_default_config
from pmp_manip.utility         import (
    read_file_text, write_file_text, enforce_argument_types, ContentFingerprint,
    GU_FailedFileReadError, GU_FailedFileWriteError, MANIP_ThanksError, MANIP_NetworkFetchError, MANIP_ExtensionFetchError,
    MANIP_DirectExtensionInfoExtractionError, MANIP_SafeExtensionInfoExtractionError,
    MANIP_NoNodeJSInstalledError, MANIP_DirectExtensionInfoExtractionError, MANIP_ExtensionInfoConvertionError,
    MANIP_ExtensionExecutionErrorInJavascript, MANIP_BadExtensionCodeFormatError, MANIP_InvalidCustomBlockError,
)

import pmp_manip.ext_info_gen.manager as manager_mod

def _make_cache(file_name:str, js_code:str="some jsCode", py_code:str="some py_code", last_update:str=datetime.now(timezone.utc).isoformat()):
    return {file_name: {
        "jsFingerprint": ContentFingerprint.from_value(js_code).to_json(),
        "pyFingerprint": ContentFingerprint.from_value(py_code).to_json(),
        "lastUpdate"   : last_update,
    }}

   

def example_usage_generate_extension_info_py_file():
    init_config(get_default_config())
    for extension_id, extension in [
        ("asyncexample",        "example_extensions/asyncexample.js"),
        ("dumbExample",         "example_extensions/dumbExample.js"),
        ("truefantombase",      "https://extensions.turbowarp.org/true-fantom/base.js"),
        ("pmControlsExpansion", "https://raw.githubusercontent.com/PenguinMod/PenguinMod-Vm/refs/heads/develop/src/extensions/pm_controlsExpansion/index.js"),
        ("gpusb3",              "https://extensions.penguinmod.com/extensions/derpygamer2142/gpusb3.js"),
        ("P7BoxPhys",           "https://extensions.penguinmod.com/extensions/pooiod/Box2D.js"),
        ("griffpatch",          "https://extensions.turbowarp.org/box2d.js"),
    ]:
        manager_mod.generate_extension_info_py_file(extension, extension_id, tolerate_file_path=True, is_strict=True)


def test_is_trusted_extension_origin_without_handler():
    for source, should_be_trusted in [
        ("https://extensions.turbowarp.org/lab/text.js", True),
        ("https://extensions.penguinmod.com/extensions/ObviousAlexC/PenPlus.js", True),
        ("https://penguinmod-extensions-gallery.vercel.app/extensions/ObviousAlexC/PenPlus.js", True),
        ("https://sharkpools-extensions.vercel.app/extension-code/Added-Motion.js", True),
        ("https://pen-group.github.io/extensions/extensions/PenP/v7.js", True),
        ("https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js", False),
    ]:
        assert manager_mod._is_trusted_extension_origin(source) == should_be_trusted

def test_is_trusted_extension_origin_with_handler(monkeypatch: MonkeyPatch):    
    def is_trusted_handler(source: str) -> bool:
        return source.startswith("https://raw.githubusercontent.com/Logise1123/")

    modified_cfg = get_default_config()
    modified_cfg.ext_info_gen.is_trusted_extension_origin_handler = is_trusted_handler
    import pmp_manip.config.manager as cfg_manager_mod
    monkeypatch.setattr(cfg_manager_mod, "_config_instance", modified_cfg)
    
    source = "https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js"
    assert manager_mod._is_trusted_extension_origin(source) == True
    assert manager_mod._is_trusted_extension_origin(source.replace("Logise1123", "SomeUser")) == False

    

def test_consider_state_file_doesnt_exist(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: False)
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache={"someExt.py": ...}, js_fetch_expensive=True,
    ) == manager_mod.STATUS_REGEN

def test_consider_state_file_not_in_cache(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache={}, js_fetch_expensive=True,
    ) == manager_mod.STATUS_REGEN

def test_consider_state_file_file_read_error(monkeypatch: MonkeyPatch):
    def fake_read_file_text(*args, **kwargs): raise GU_FailedFileReadError()
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", fake_read_file_text)
    cache = _make_cache("someExt.py")
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=True,
    ) == manager_mod.STATUS_REGEN

def test_consider_state_file_invalid_py_fingerprint(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "some py_code")
    cache = _make_cache("someExt.py")
    cache["someExt.py"]["pyFingerprint"] = ...
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=True,
    ) == manager_mod.STATUS_REGEN

def test_consider_state_file_no_match(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "some py_code")
    cache = _make_cache("someExt.py", 
        py_code="some diff py_code", # matches will be False
    ) 
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=True,
    ) == manager_mod.STATUS_REGEN

def test_consider_state_file_matches_not_expensive(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "some py_code")
    cache = _make_cache("someExt.py", 
        py_code="some py_code", # matches will be True
    ) 
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=False,
    ) == manager_mod.STATUS_CHECK_JS

def test_consider_state_file_matches_expensive_invalid_last_update(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "some py_code")
    cache = _make_cache("someExt.py", 
        py_code="some py_code", # matches will be True
        last_update="some-invalid-date",
    )
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=True,
    ) == manager_mod.STATUS_CHECK_JS

def test_consider_state_file_matches_exensive_too_old(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "some py_code")
    last_update = datetime.now(timezone.utc) - get_config().ext_info_gen.js_fetch_interval - timedelta(minutes=5)
    cache = _make_cache("someExt.py", 
        py_code="some py_code", # matches will be True
        last_update=last_update.isoformat(), # => 5 minutes after timeout
    ) 
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=True,
    ) == manager_mod.STATUS_CHECK_JS

def test_consider_state_file_matches_expensive_not_too_old(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "some py_code")
    last_update = datetime.now(timezone.utc) - get_config().ext_info_gen.js_fetch_interval + timedelta(minutes=5)
    cache = _make_cache("someExt.py", 
        py_code="some py_code", # matches will be True
        last_update=last_update.isoformat(), # => 5 minutes before timeout
    ) 
    assert manager_mod._consider_state(
        "someExt.py", "some_dir/someExt.py",
        cache=cache, js_fetch_expensive=True,
    ) == manager_mod.STATUS_KEEP



def test_get_cache_file_doesnt_exist(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: False)
    manager_mod._get_cache(cache_file_path="cache.json") == {}

def test_get_cache_file_file_read_error(monkeypatch: MonkeyPatch):
    def fake_read_file_text(*args, **kwargs): raise GU_FailedFileReadError()
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", fake_read_file_text)
    manager_mod._get_cache(cache_file_path="cache.json") == {}

def test_get_cache_file_decode_error(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: '{"x": 1,}') # invalid json
    manager_mod._get_cache(cache_file_path="cache.json") == {}

def test_get_cache_file_success(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(manager_mod, "file_exists", lambda p: True)
    cache = _make_cache(file_name="myExt.py")
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: dumps(cache)) # invalid json
    assert manager_mod._get_cache(cache_file_path="cache.json") == cache



def test_update_cache_write_error(monkeypatch: MonkeyPatch):
    def fake_write_file_text(*args, **kwargs): raise GU_FailedFileWriteError()
    monkeypatch.setattr(manager_mod, "write_file_text", fake_write_file_text)
    cache = _make_cache(file_name="myExt.py")
    with raises(GU_FailedFileWriteError):
        manager_mod._update_cache(
            cache, cache_file_path="cache.json", dest_file_name="myExt.py",
            js_code="some jsCode", py_code="some py_code",
        )

def test_update_cache_new_entry(monkeypatch: MonkeyPatch):
    def fake_write_file_text(file_path: str, text: str):
        assert file_path == "cache.json"
        cache_data: dict[str, dict[str, Any]] = loads(text)
        assert set(cache_data.keys()) == {"_", "myExt.py"}
        assert set(cache_data["myExt.py"].keys()) == {"jsFingerprint", "pyFingerprint", "lastUpdate"}
        assert ContentFingerprint.from_json(cache_data["myExt.py"]["jsFingerprint"]).matches("some jsCode")
        assert ContentFingerprint.from_json(cache_data["myExt.py"]["pyFingerprint"]).matches("some py_code")
        assert (datetime.fromisoformat(cache_data["myExt.py"]["lastUpdate"]) - datetime.now(timezone.utc)) < timedelta(minutes=1)

    monkeypatch.setattr(manager_mod, "write_file_text", fake_write_file_text)
    cache = {}
    manager_mod._update_cache(
        cache, cache_file_path="cache.json", dest_file_name="myExt.py",
        js_code="some jsCode", py_code="some py_code",
    )

def test_update_cache_update_entry(monkeypatch: MonkeyPatch):
    def fake_write_file_text(file_path: str, text: str):
        assert file_path == "cache.json"
        cache_data: dict[str, dict[str, Any]] = loads(text)
        assert set(cache_data.keys()) == {"_", "myExt.py"}
        assert set(cache_data["myExt.py"].keys()) == {"jsFingerprint", "pyFingerprint", "lastUpdate"}
        assert cache_data["myExt.py"]["jsFingerprint"] == old_cache["myExt.py"]["jsFingerprint"]
        assert cache_data["myExt.py"]["pyFingerprint"] == old_cache["myExt.py"]["pyFingerprint"]
        assert (datetime.fromisoformat(cache_data["myExt.py"]["lastUpdate"]) - datetime.now(timezone.utc)) < timedelta(minutes=1)

    monkeypatch.setattr(manager_mod, "write_file_text", fake_write_file_text)
    last_update = datetime.now() - timedelta(days=1)
    old_cache = _make_cache(file_name="myExt.py", last_update=last_update.isoformat())
    manager_mod._update_cache(
        old_cache, cache_file_path="cache.json", dest_file_name="myExt.py",
        js_code=None, py_code=None,
    )



def test_generate_extension_info_py_file_kept_unconditionally(monkeypatch: MonkeyPatch):
    def fake_update_cache(
        old_cache: dict[str, dict[str, Any]], cache_file_path: str, dest_file_name: str, 
        js_code: str | None, py_code: str | None,
    ):
        assert old_cache == made_cache
        assert cache_file_path == path.join("gen_ext_opcode_info", "cache.json")
        assert dest_file_name == "myExt.py"
        assert js_code is None
        assert py_code is None
    made_cache = _make_cache("myExt.py")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_KEEP)
    monkeypatch.setattr(manager_mod, "_update_cache", fake_update_cache)

    dest_file_path = manager_mod.generate_extension_info_py_file(
        source="https://someurl.cool/myExt.js", extension_id="myExt",
        tolerate_file_path=False, bundle_errors=True,
    )
    assert dest_file_path == path.join("gen_ext_opcode_info", "myExt.py")

def test_generate_extension_info_py_file_fetch_error(monkeypatch: MonkeyPatch):
    def fake_fetch_js_code(source: str, tolerate_file_path: bool):
        raise MANIP_NetworkFetchError()
    made_cache = _make_cache("myExt.py")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_CHECK_JS)
    monkeypatch.setattr(manager_mod, "fetch_js_code", fake_fetch_js_code)
    
    with raises(MANIP_ExtensionFetchError):
        manager_mod.generate_extension_info_py_file(
            source="https://someurl.cool/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )
    with raises(MANIP_NetworkFetchError):
        manager_mod.generate_extension_info_py_file(
            source="https://someurl.cool/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=False,
        )

def test_generate_extension_info_py_file_kept_conditionally(monkeypatch: MonkeyPatch):
    def fake_update_cache(
        old_cache: dict[str, dict[str, Any]], cache_file_path: str, dest_file_name: str, 
        js_code: str | None, py_code: str | None,
    ):
        assert old_cache == made_cache
        assert cache_file_path == path.join("gen_ext_opcode_info", "cache.json")
        assert dest_file_name == "myExt.py"
        assert js_code is None
        assert py_code is None
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_CHECK_JS)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "_update_cache", fake_update_cache)

    dest_file_path = manager_mod.generate_extension_info_py_file(
        source="https://someurl.cool/myExt.js", extension_id="myExt",
        tolerate_file_path=False, bundle_errors=True,
    )
    assert dest_file_path == path.join("gen_ext_opcode_info", "myExt.py")

def test_generate_extension_info_py_file_trusted_no_nodejs_error(monkeypatch: MonkeyPatch):
    def fake_extract_extension_info_directly(js_code: str, code_encoding: str = "utf-8"):
        raise MANIP_NoNodeJSInstalledError()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", fake_extract_extension_info_directly)
    
    with raises(MANIP_NoNodeJSInstalledError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=False,
        )
    with raises(MANIP_NoNodeJSInstalledError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_direct_ext_exec_error(monkeypatch: MonkeyPatch):
    def fake_extract_extension_info_directly(js_code: str, code_encoding: str = "utf-8"):
        assert js_code == "js code of myExt"
        assert code_encoding == "utf-8"
        raise MANIP_ExtensionExecutionErrorInJavascript()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", fake_extract_extension_info_directly)
    
    with raises(MANIP_ExtensionExecutionErrorInJavascript):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=False,
        )
    with raises(MANIP_DirectExtensionInfoExtractionError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_safe_bad_ext_code_error(monkeypatch: MonkeyPatch):
    def fake_extract_extension_info_safely(js_code: str, code_encoding: str = "utf-8"):
        assert js_code == "js code of myExt"
        assert code_encoding == "utf-8"
        raise MANIP_BadExtensionCodeFormatError()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_safely", fake_extract_extension_info_safely)
    
    with raises(MANIP_BadExtensionCodeFormatError):
        manager_mod.generate_extension_info_py_file(
            source="https://untrusted.example.com/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=False,
        )
    with raises(MANIP_SafeExtensionInfoExtractionError):
        manager_mod.generate_extension_info_py_file(
            source="https://untrusted.example.com/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_generator_thanks_error(monkeypatch: MonkeyPatch):
    def fake_generate_opcode_info_group(extension_info: dict[str, Any]): raise MANIP_ThanksError()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda c: {"msg": "some ext info"})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", fake_generate_opcode_info_group)    
    
    with raises(MANIP_ThanksError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=False,
        )
    with raises(MANIP_ThanksError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_generator_convertion_error(monkeypatch: MonkeyPatch):
    def fake_generate_opcode_info_group(extension_info: dict[str, Any]): raise MANIP_InvalidCustomBlockError()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda c: {"msg": "some ext info"})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", fake_generate_opcode_info_group)    
    
    with raises(MANIP_InvalidCustomBlockError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=False,
        )
    with raises(MANIP_ExtensionInfoConvertionError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_make_file_dir_error(monkeypatch: MonkeyPatch):
    def fake_makedirs(p, exist_ok=False): raise OSError()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda c: {"msg": "some ext info"})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda e: (None, None, None))
    monkeypatch.setattr(manager_mod, "generate_file_code", lambda ig, it, dt: "py code of myExt")  
    monkeypatch.setattr(manager_mod, "makedirs", fake_makedirs)  
    
    with raises(GU_FailedFileWriteError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_write_file_error(monkeypatch: MonkeyPatch):
    def fake_write_file_text(p, t):
        assert p == path.join("gen_ext_opcode_info", "myExt.py")
        assert t == "py code of myExt"
        raise GU_FailedFileWriteError()
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda c: {"msg": "some ext info"})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda e: (None, None, None))
    monkeypatch.setattr(manager_mod, "generate_file_code", lambda ig, it, dt: "py code of myExt")  
    monkeypatch.setattr(manager_mod, "makedirs", lambda p, exist_ok: None)
    monkeypatch.setattr(manager_mod, "write_file_text", fake_write_file_text)
    
    with raises(GU_FailedFileWriteError):
        manager_mod.generate_extension_info_py_file(
            source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
            tolerate_file_path=False, bundle_errors=True,
        )

def test_generate_extension_info_py_file_success(monkeypatch: MonkeyPatch):
    def fake_update_cache(
        old_cache: dict[str, dict[str, Any]], cache_file_path: str, dest_file_name: str, 
        js_code: str | None, py_code: str | None,
    ):
        assert old_cache == made_cache
        assert cache_file_path == path.join("gen_ext_opcode_info", "cache.json")
        assert dest_file_name == "myExt.py"
        assert js_code == "js code of myExt"
        assert py_code == "py code of myExt"
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_REGEN)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda c: {"msg": "some ext info"})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda e: (None, None, None))
    monkeypatch.setattr(manager_mod, "generate_file_code", lambda ig, it, dt: "py code of myExt")  
    monkeypatch.setattr(manager_mod, "makedirs", lambda p, exist_ok: None)
    monkeypatch.setattr(manager_mod, "write_file_text", lambda p, t: None)
    monkeypatch.setattr(manager_mod, "_update_cache", fake_update_cache)
    
    dest_file_path = manager_mod.generate_extension_info_py_file(
        source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
        tolerate_file_path=False, bundle_errors=True,
    )
    assert dest_file_path == path.join("gen_ext_opcode_info", "myExt.py")

def test_generate_extension_info_py_file_invalid_js_fingerprint(monkeypatch: MonkeyPatch):
    def fake_update_cache(
        old_cache: dict[str, dict[str, Any]], cache_file_path: str, dest_file_name: str, 
        js_code: str | None, py_code: str | None,
    ):
        assert old_cache == made_cache
        assert cache_file_path == path.join("gen_ext_opcode_info", "cache.json")
        assert dest_file_name == "myExt.py"
        assert js_code == "js code of myExt"
        assert py_code == "py code of myExt"
    made_cache = _make_cache("myExt.py", js_code="js code of myExt")
    made_cache["myExt.py"]["jsFingerprint"] = ...
    monkeypatch.setattr(manager_mod, "_get_cache", lambda p: made_cache)
    monkeypatch.setattr(manager_mod, "_consider_state", lambda dn, dp, c, js_fetch_expensive: manager_mod.STATUS_CHECK_JS)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, tolerate_file_path: "js code of myExt")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda c: {"msg": "some ext info"})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda e: (None, None, None))
    monkeypatch.setattr(manager_mod, "generate_file_code", lambda ig, it, dt: "py code of myExt")  
    monkeypatch.setattr(manager_mod, "makedirs", lambda p, exist_ok: None)
    monkeypatch.setattr(manager_mod, "write_file_text", lambda p, t: None)
    monkeypatch.setattr(manager_mod, "_update_cache", fake_update_cache)
    
    dest_file_path = manager_mod.generate_extension_info_py_file(
        source="https://extensions.penguinmod.com/extensions/myUser/myExt.js", extension_id="myExt",
        tolerate_file_path=False, bundle_errors=True,
    )
    assert dest_file_path == path.join("gen_ext_opcode_info", "myExt.py")

