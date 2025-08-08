from pytest       import raises, MonkeyPatch
from subprocess   import run as run_subprocess, TimeoutExpired

from pmp_manip.utility import (
    delete_file,
    PP_FailedFileWriteError, PP_FailedFileDeleteError, 
    PP_NoNodeJSInstalledError, 
    PP_ExtensionExecutionTimeoutError, PP_ExtensionExecutionErrorInJavascript, PP_UnexpectedExtensionExecutionError,
    PP_ExtensionJSONDecodeError, 
)

EXAMPLE_EXTENSION_CODE = """// Name: Base
// ID: truefantombase
// Description: Convert numbers between bases.
// By: TrueFantom <https://scratch.mit.edu/users/TrueFantom/>
// License: MIT
// Context: "Base" refers to the mathematical definition eg. base 2 is binary, base 10 is decimal, base 16 is hex.

/* generated l10n code */Scratch.translate.setup({"de":{"_Base":"Basis"},"fi":{"_Base":"Kantaluvut","_[A] from base [B] to base [C]":"[A] kantaluvusta [B] kantalukuun [C]","_is base [B] [A]?":"onko luvun [A] kantaluku [B]?"},"it":{"_Base":"Basi"},"ja":{"_Base":"進数","_[A] from base [B] to base [C]":"[B]進数の数[A]を[C]進数に変換する","_is base [B] [A]?":"[A]は[B]進数で表現できる"},"ko":{"_Base":"진법","_[A] from base [B] to base [C]":"[A]을(를) [B]진법에서 [C]진법으로","_is base [B] [A]?":"[A](이)가 [B]진법인가?"},"nb":{"_[A] from base [B] to base [C]":"[A] fra base [B] til base [C]","_is base [B] [A]?":"er base [B] [A]?"},"nl":{"_[A] from base [B] to base [C]":"zet [A] om van base-[B] naar base-[C]","_is base [B] [A]?":"is [A] base-[B]?"},"ru":{"_Base":"База","_[A] from base [B] to base [C]":"[A] из базы [B] в базу [C]","_is base [B] [A]?":"база [B] [A]?"},"zh-cn":{"_Base":"进制转换","_[A] from base [B] to base [C]":"把[B]进制的[A]转换成[C]","_is base [B] [A]?":"[A]是[B]进制吗？"}});/* end generated l10n code */((Scratch) => {
  "use strict";

  const icon =
    "data:image/svg+xml;base64,PHN2ZyB...LS0+";

  const cast = Scratch.Cast;

  const bases = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
  ];
  const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  class ScratchBase {
    getInfo() {
      return {
        id: "truefantombase",
        name: Scratch.translate("Base"),

        color1: "#e200ca",

        menuIconURI: icon,

        blocks: [
          {
            opcode: "is_base_block",
            blockType: Scratch.BlockType.BOOLEAN,
            text: Scratch.translate({
              default: "is base [B] [A]?",
              description:
                "[B] will be the base like 'base 10', [A] is the text we want to check if it is in that base",
            }),
            arguments: {
              A: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: "10",
              },
              B: {
                type: Scratch.ArgumentType.STRING,
                menu: "base_menu",
                defaultValue: "10",
              },
            },
          },
          {
            opcode: "base_block",
            blockType: Scratch.BlockType.REPORTER,
            text: Scratch.translate({
              default: "[A] from base [B] to base [C]",
              description:
                "[A] is the original number, [B] is the base it is currently in, [C] is the base it will be converted to.",
            }),
            arguments: {
              A: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: "10",
              },
              B: {
                type: Scratch.ArgumentType.STRING,
                menu: "base_menu",
                defaultValue: "10",
              },
              C: {
                type: Scratch.ArgumentType.STRING,
                menu: "base_menu",
              },
            },
          },
        ],
        menus: {
          base_menu: {
            acceptReporters: true,
            items: bases,
          },
        },
      };
    }

    is_base_block({ A, B }) {
      if (bases.includes(cast.toString(B))) {
        return new RegExp(
          "^[" + chars.substring(0, cast.toNumber(B)) + "]+$"
        ).test(cast.toString(A));
      }
      return false;
    }
    base_block({ A, B, C }) {
      if (
        bases.includes(cast.toString(B)) &&
        bases.includes(cast.toString(C))
      ) {
        if (
          new RegExp("^[" + chars.substring(0, cast.toNumber(B)) + "]+$").test(
            cast.toString(A)
          )
        ) {
          return (
            parseInt(cast.toString(A), cast.toNumber(B))
              .toString(cast.toNumber(C))
              .toUpperCase() || "0"
          ); // Return string zero because toString() function always return strings
        }
      }
      return "0"; // Return string zero because toString() function always return strings
    }
  }

  Scratch.extensions.register(new ScratchBase());
})(Scratch);"""
   


def test_extract_extension_info_directly():
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    extension_info = extract_extension_info_directly(EXAMPLE_EXTENSION_CODE)
    assert extension_info == {
        "id": "truefantombase",
        "name": "Base",
        "color1": "#e200ca",
        "menuIconURI": "data:image/svg+xml;base64,PHN2ZyB...LS0+",
        "blocks": [
            {
                "opcode": "is_base_block",
                "blockType": "Boolean",
                "text": "is base [B] [A]?",
                "arguments": {
                    "A": {
                        "type": "string",
                        "defaultValue": "10",
                    },
                    "B": {
                        "type": "string",
                        "menu": "base_menu",
                        "defaultValue": "10",
                    },
                },
            }, 
            {
                "opcode": "base_block",
                "blockType": "reporter",
                "text": "[A] from base [B] to base [C]",
                "arguments": {
                    "A": {
                        "type": "string",
                        "defaultValue": "10",
                    },
                    "B": {
                        "type": "string",
                        "menu": "base_menu",
                        "defaultValue": "10",
                    },
                    "C": {
                        "type": "string",
                        "menu": "base_menu",
                    },
                },
            },
        ],
        "menus": {
            "base_menu": {
                "acceptReporters": True,
                "items": [
                    "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", 
                    "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", 
                    "31", "32", "33", "34", "35", "36",
                ],
            },
        },
    }

def test_extract_extension_info_directly_write_error():
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    # Contains an unpaired high surrogate (U+D800)
    with raises(PP_FailedFileWriteError):
        extract_extension_info_directly("this will fail: \ud800")
        
def test_extract_extension_info_directly_not_installed(monkeypatch: MonkeyPatch):
    def fake_run_subprocess(*args, **kwargs):
        raise FileNotFoundError()

    import pmp_manip.ext_info_gen.direct_extractor as direct_extractor_mod
    monkeypatch.setattr(direct_extractor_mod, "run_subprocess", fake_run_subprocess)
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    
    with raises(PP_NoNodeJSInstalledError):
        extract_extension_info_directly(EXAMPLE_EXTENSION_CODE)

def test_extract_extension_info_directly_timeout_expired(monkeypatch: MonkeyPatch):
    def fake_run_subprocess(*args, **kwargs):
        raise TimeoutExpired("some command", 1)

    import pmp_manip.ext_info_gen.direct_extractor as direct_extractor_mod
    monkeypatch.setattr(direct_extractor_mod, "run_subprocess", fake_run_subprocess)
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    
    with raises(PP_ExtensionExecutionTimeoutError):
        extract_extension_info_directly(EXAMPLE_EXTENSION_CODE)

def test_extract_extension_info_directly_unexpected_error(monkeypatch: MonkeyPatch):
    def fake_run_subprocess(*args, **kwargs):
        raise PermissionError()

    import pmp_manip.ext_info_gen.direct_extractor as direct_extractor_mod
    monkeypatch.setattr(direct_extractor_mod, "run_subprocess", fake_run_subprocess)
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    
    with raises(PP_UnexpectedExtensionExecutionError):
        extract_extension_info_directly(EXAMPLE_EXTENSION_CODE)

def test_extract_extension_info_directly_temp_delete_error(monkeypatch: MonkeyPatch):
    temp_file_path = None
    def fake_delete_file(file, *args, **kwargs):
        nonlocal temp_file_path
        temp_file_path = file
        raise PP_FailedFileDeleteError()

    import pmp_manip.ext_info_gen.direct_extractor as direct_extractor_mod
    monkeypatch.setattr(direct_extractor_mod, "delete_file", fake_delete_file)
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    
    try:
        with raises(PP_FailedFileDeleteError):
            extract_extension_info_directly(EXAMPLE_EXTENSION_CODE)
    finally:
        delete_file(temp_file_path)

def test_extract_extension_info_directly_not_registered():
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    with raises(PP_ExtensionExecutionErrorInJavascript):
        extract_extension_info_directly("")

def test_extract_extension_info_directly_some_other_js_error():
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    code = EXAMPLE_EXTENSION_CODE.replace("const icon =\n    \"data:image/svg+xml;base64,PHN2ZyB...LS0+\";\n", "")
    with raises(PP_ExtensionExecutionErrorInJavascript):
        extract_extension_info_directly(code)

def test_extract_extension_info_directly_json_decode_error(monkeypatch: MonkeyPatch):
    def fake_run_subprocess(*args, **kwargs):
        result = run_subprocess(*args, **kwargs)
        result.stdout = ""
        return result

    import pmp_manip.ext_info_gen.direct_extractor as direct_extractor_mod
    monkeypatch.setattr(direct_extractor_mod, "run_subprocess", fake_run_subprocess)
    from pmp_manip.ext_info_gen.direct_extractor import extract_extension_info_directly
    
    with raises(PP_ExtensionJSONDecodeError):
        extract_extension_info_directly(EXAMPLE_EXTENSION_CODE)
