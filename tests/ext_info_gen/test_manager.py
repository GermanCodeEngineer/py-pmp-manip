from datetime     import datetime, timedelta, timezone
from json         import loads, dumps, JSONDecodeError
from logging      import getLogger
from os           import path, makedirs
from pathlib      import Path
from pytest       import raises, fixture, mark, MonkeyPatch
from typing       import Any

from pmp_manip.config          import get_config, init_config, get_default_config
from pmp_manip.utility         import (
    read_file_text, write_file_text, enforce_argument_types, ContentFingerprint,
    PP_Error, PP_FailedFileWriteError, PP_ThanksError, PP_ExtensionFetchError,
    PP_DirectExtensionInfoExtractionError, PP_SafeExtensionInfoExtractionError,
    PP_NoNodeJSInstalledError, PP_ExtensionInfoConvertionError,
)

from   pmp_manip.ext_info_gen.manager import is_trusted_extension_origin, generate_extension_info_py_file
import pmp_manip.ext_info_gen.manager as manager_mod

@fixture(autouse=True)
def reset_config(monkeypatch: MonkeyPatch, tmp_path: Path):
    """Reset config for each test and point gen_opcode_info_dir to tmpdir."""
    cfg = get_default_config()
    cfg.ext_info_gen.gen_opcode_info_dir = str(tmp_path)
    monkeypatch.setattr("pmp_manip.config.manager._config_instance", cfg)
    monkeypatch.setattr("pmp_manip.config.get_config", lambda: cfg)
    yield

   

def test_is_trusted_extension_origin_without_handler():
    for source, should_be_trusted in [
        ("https://extensions.turbowarp.org/lab/text.js", True),
        ("https://extensions.penguinmod.com/extensions/ObviousAlexC/PenPlus.js", True),
        ("https://penguinmod-extensions-gallery.vercel.app/extensions/ObviousAlexC/PenPlus.js", True),
        ("https://sharkpools-extensions.vercel.app/extension-code/Added-Motion.js", True),
        ("https://pen-group.github.io/extensions/extensions/PenP/v7.js", True),
        ("https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js", False),
    ]:
        assert is_trusted_extension_origin(source) == should_be_trusted

def test_is_trusted_extension_origin_with_handler(monkeypatch: MonkeyPatch):    
    def is_trusted_handler(source: str) -> bool:
        return source.startswith("https://raw.githubusercontent.com/Logise1123/")

    modified_cfg = get_default_config()
    modified_cfg.ext_info_gen.is_trusted_extension_origin_handler = is_trusted_handler
    import pmp_manip.config.manager as manager_mod
    monkeypatch.setattr(manager_mod, "_config_instance", modified_cfg)
    
    source = "https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js"
    assert is_trusted_extension_origin(source) == True
    assert is_trusted_extension_origin(source.replace("Logise1123", "SomeUser")) == False

    

def _make_cache_file(tmp_path: Path, name, py_code, js_code, last_update=None):
    """Helper to create a valid cache file."""
    if last_update is None:
        last_update = datetime.now(timezone.utc).isoformat()
    cache_data = {
        f"{name}.py": {
            "jsFingerprint": ContentFingerprint.from_value(js_code).to_json(),
            "pyFingerprint": ContentFingerprint.from_value(py_code).to_json(),
            "lastUpdate": last_update,
        }
    }
    cache_path = tmp_path / manager_mod.CACHE_FILENAME
    print("AT", cache_path, cache_data)
    cache_path.write_text(dumps(cache_data))
    return cache_path


def test_generate_extension_info_py_file_keep_branch(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Prepare cache + destination file
    py_code = "print('hello')"
    js_code = "console.log('hi')"
    ext_id = "ext1"
    dest_file = tmp_path / f"{ext_id}.py"
    dest_file.write_text(py_code)
    _make_cache_file(tmp_path, ext_id, py_code, js_code)

    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: py_code)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: js_code)

    # Force consider_state to return KEEP
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda info: ("grp", "in", "dr"))
    monkeypatch.setattr(manager_mod, "generate_file_code", lambda *a: "code")
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda js: {"ok": True})
    monkeypatch.setattr(manager_mod, "extract_extension_info_safely", lambda js: {"ok": True})

    # Actually run
    result = manager_mod.generate_extension_info_py_file("https://some.url/ext.js", ext_id, tolerate_file_path=True)
    assert result.endswith(f"{ext_id}.py")
    # Should not overwrite the file
    assert dest_file.read_text() == py_code

def test_generate_extension_info_py_file_check_js_fingerprint_match(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Force STATUS_CHECK_JS
    py_code = "print('hi')"
    js_code = "console.log('hi')"
    ext_id = "ext2"
    dest_file = tmp_path / f"{ext_id}.py"
    dest_file.write_text(py_code)
    _make_cache_file(tmp_path, ext_id, py_code, js_code,
                    last_update=(datetime.now(timezone.utc) - timedelta(days=10)).isoformat())

    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: py_code)
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: js_code)
    monkeypatch.setattr(manager_mod, "ContentFingerprint.from_json", ContentFingerprint.from_json)

    result = manager_mod.generate_extension_info_py_file("https://some.url/ext.js", ext_id, True)
    assert result.endswith(f"{ext_id}.py")

@mark.parametrize("trusted", [True, False])
def test_generate_extension_info_py_file_regen_branch_success(monkeypatch: MonkeyPatch, tmp_path: Path, trusted):
    ext_id = "ext3"
    js_code = "console.log('hi')"
    py_code = "print('py')"

    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "anything")
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: js_code)
    monkeypatch.setattr(manager_mod, "is_trusted_extension_origin", lambda s: trusted)
    if trusted:
        monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda js: {"info": 1})
    else:
        monkeypatch.setattr(manager_mod, "extract_extension_info_safely", lambda js: {"info": 1})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda info: ("grp", "in", "dr"))
    monkeypatch.setattr(manager_mod, "generate_file_code", lambda *a: py_code)
    monkeypatch.setattr(manager_mod, "write_file_text", lambda p, t: None)

    result = manager_mod.generate_extension_info_py_file("https://whatever.js", ext_id, True)
    assert path.exists(result)


@mark.parametrize("exc,wrapped", [
    (PP_Error("x"), PP_ExtensionFetchError),
    (PP_NoNodeJSInstalledError("x"), PP_NoNodeJSInstalledError),
])
def test_generate_extension_info_py_file_fetch_errors(monkeypatch: MonkeyPatch, tmp_path: Path, exc, wrapped):
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "anything")
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: (_ for _ in ()).throw(exc))

    if issubclass(wrapped, PP_Error):
        with raises(wrapped):
            manager_mod.generate_extension_info_py_file("https://whatever.js", "extid", True)
    else:
        with raises(wrapped):
            manager_mod.generate_extension_info_py_file("https://whatever.js", "extid", True, bundle_errors=False)


@mark.parametrize("funcname,wrapped", [
    ("extract_extension_info_directly", PP_DirectExtensionInfoExtractionError),
    ("extract_extension_info_safely", PP_SafeExtensionInfoExtractionError),
])
def test_generate_extension_info_py_file_extraction_errors(monkeypatch: MonkeyPatch, tmp_path: Path, funcname, wrapped):
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "anything")
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: "js")
    monkeypatch.setattr(manager_mod, "is_trusted_extension_origin", lambda s: funcname.endswith("directly"))
    monkeypatch.setattr(manager_mod, funcname, lambda js: (_ for _ in ()).throw(PP_Error("x")))

    with raises(wrapped):
        manager_mod.generate_extension_info_py_file("https://whatever.js", "extid", True)


def test_generate_extension_info_py_file_conversion_error(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "anything")
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: "js")
    monkeypatch.setattr(manager_mod, "is_trusted_extension_origin", lambda s: True)
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda js: {"ok": 1})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda info: (_ for _ in ()).throw(PP_Error("bad")))

    with raises(PP_ExtensionInfoConvertionError):
        manager_mod.generate_extension_info_py_file("https://whatever.js", "extid", True)


def test_generate_extension_info_py_file_thanks_error_passes(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(manager_mod, "read_file_text", lambda p: "anything")
    monkeypatch.setattr(manager_mod, "fetch_js_code", lambda s, t: "js")
    monkeypatch.setattr(manager_mod, "is_trusted_extension_origin", lambda s: True)
    monkeypatch.setattr(manager_mod, "extract_extension_info_directly", lambda js: {"ok": 1})
    monkeypatch.setattr(manager_mod, "generate_opcode_info_group", lambda info: (_ for _ in ()).throw(PP_ThanksError("thx")))

    with raises(PP_ThanksError):
        manager_mod.generate_extension_info_py_file("https://whatever.js", "extid", True)

# Stopped in tpgTAHc; above is TRASH