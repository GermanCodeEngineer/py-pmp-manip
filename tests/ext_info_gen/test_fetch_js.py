from pytest                 import raises, MonkeyPatch
from requests               import HTTPError

from pmp_manip.utility            import (
    PP_InvalidExtensionCodeSourceError, 
    PP_NetworkFetchError, PP_UnexpectedFetchError, PP_FileFetchError, 
    PP_FileNotFoundError, PP_FailedFileReadError,
)


class FakeResponse:
    def __init__(self, text="", status_code=200):
        self.text        = text
        self.status_code = status_code
    
    def raise_for_status(self):
        if not(200 <= self.status_code < 300):
            raise HTTPError(f"Status code: {self.status_code}")

DATA_URI1_RAW = "data:text/javascript;base64,Ly8gU2ltcGxlIGZpbGUgc3RvcmFnZSBtYWRlIHdpdGggdG9vbHMgZnJvbSBTbmFwIQoKY2xhc3MgU2VydmVyRXh0ZW5zaW9uIHsKICBjb25zdHJ1Y3RvcihydW50aW1lKSB7CiAgICB0aGlzLnJ1bnRpbWUgPSBydW50aW1lOwogICAgdGhpcy5zZXJ2ZXJVUkwgPSAnaHR0cHM6Ly9zbmFwZXh0ZW5zaW9ucy51bmktZ29ldHRpbmdlbi5kZS9oYW5kbGVUZXh0ZmlsZS5waHAnOwogIH0KCiAgZ2V0SW5mbygpIHsKICAgIHJldHVybiB7CiAgICAgIGlkOiAnc2VydmVyRGF0YScsCiAgICAgIG5hbWU6ICdTZXJ2ZXIgRGF0YScsCiAgICAgIGNvbG9yMTogJyMzMWIzZDQnLAogICAgICBjb2xvcjI6ICcjMTc5ZmMyJywKICAgICAgYmxvY2tzOiBbCiAgICAgICAgewogICAgICAgICAgb3Bjb2RlOiAnc2F2ZVRvU2VydmVyJywKICAgICAgICAgIGJsb2NrVHlwZTogU2NyYXRjaC5CbG9ja1R5cGUuQ09NTUFORCwKICAgICAgICAgIHRleHQ6ICdTYXZlIFt2YXJpYWJsZU5hbWVdIHdpdGggY29udGVudCBbY29udGVudF0nLAogICAgICAgICAgYXJndW1lbnRzOiB7CiAgICAgICAgICAgIHZhcmlhYmxlTmFtZTogewogICAgICAgICAgICAgIHR5cGU6IFNjcmF0Y2guQXJndW1lbnRUeXBlLlNUUklORywKICAgICAgICAgICAgICBkZWZhdWx0VmFsdWU6ICdkZWZhdWx0LnR4dCcsCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgIGNvbnRlbnQ6IHsKICAgICAgICAgICAgICB0eXBlOiBTY3JhdGNoLkFyZ3VtZW50VHlwZS5TVFJJTkcsCiAgICAgICAgICAgICAgZGVmYXVsdFZhbHVlOiAnSGVsbG8sIFdvcmxkIScsCiAgICAgICAgICAgIH0sCiAgICAgICAgICB9LAogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgb3Bjb2RlOiAnbG9hZEZyb21TZXJ2ZXInLAogICAgICAgICAgYmxvY2tUeXBlOiBTY3JhdGNoLkJsb2NrVHlwZS5SRVBPUlRFUiwKICAgICAgICAgIHRleHQ6ICdMb2FkIFt2YXJpYWJsZU5hbWVdJywKICAgICAgICAgIGFyZ3VtZW50czogewogICAgICAgICAgICB2YXJpYWJsZU5hbWU6IHsKICAgICAgICAgICAgICB0eXBlOiBTY3JhdGNoLkFyZ3VtZW50VHlwZS5TVFJJTkcsCiAgICAgICAgICAgICAgZGVmYXVsdFZhbHVlOiAnZGF0YS50eHQnLAogICAgICAgICAgICB9LAogICAgICAgICAgfSwKICAgICAgICB9LAogICAgICBdLAogICAgfTsKICB9CgogIHNhdmVUb1NlcnZlcihhcmdzLCB1dGlsKSB7CiAgICBjb25zdCB2YXJpYWJsZU5hbWUgPSBhcmdzLnZhcmlhYmxlTmFtZTsKICAgIGNvbnN0IGNvbnRlbnQgPSBhcmdzLmNvbnRlbnQ7CgogICAgY29uc3QgdXJsID0KICAgICAgdGhpcy5zZXJ2ZXJVUkwgKwogICAgICAnP3R5cGU9d3JpdGUnICsKICAgICAgJyZjb250ZW50PScgKwogICAgICBlbmNvZGVVUklDb21wb25lbnQoY29udGVudCkgKwogICAgICAnJmZpbGVuYW1lPS4vdGV4dGZpbGVzLycgKwogICAgICBlbmNvZGVVUklDb21wb25lbnQodmFyaWFibGVOYW1lKTsKCiAgICByZXR1cm4gZmV0Y2godXJsKQogICAgICAudGhlbihyZXNwb25zZSA9PiByZXNwb25zZS50ZXh0KCkpCiAgICAgIC50aGVuKHJlc3VsdCA9PiAocmVzdWx0ID09PSAnb2snKSkKICAgICAgLmNhdGNoKGVycm9yID0+IHsKICAgICAgICBjb25zb2xlLmVycm9yKCdGYWlsZWQgdG8gc2F2ZSBkYXRhOicsIGVycm9yKTsKICAgICAgICByZXR1cm4gZmFsc2U7CiAgICAgIH0pOwogIH0KCiAgbG9hZEZyb21TZXJ2ZXIoYXJncywgdXRpbCkgewogICAgY29uc3QgdmFyaWFibGVOYW1lID0gYXJncy52YXJpYWJsZU5hbWU7CgogICAgY29uc3QgdXJsID0KICAgICAgdGhpcy5zZXJ2ZXJVUkwgKwogICAgICAnP3R5cGU9cmVhZCcgKwogICAgICAnJmZpbGVuYW1lPS4vdGV4dGZpbGVzLycgKwogICAgICBlbmNvZGVVUklDb21wb25lbnQodmFyaWFibGVOYW1lKTsKCiAgICByZXR1cm4gZmV0Y2godXJsKQogICAgICAudGhlbihyZXNwb25zZSA9PiByZXNwb25zZS50ZXh0KCkpCiAgICAgIC5jYXRjaChlcnJvciA9PiB7CiAgICAgICAgY29uc29sZS5lcnJvcignRmFpbGVkIHRvIGxvYWQgZGF0YTonLCBlcnJvcik7CiAgICAgICAgcmV0dXJuICJjYW4ndCBnZXQgZGF0YSI7CiAgICAgIH0pOwogIH0KfQoKU2NyYXRjaC5leHRlbnNpb25zLnJlZ2lzdGVyKG5ldyBTZXJ2ZXJFeHRlbnNpb24oKSk7"
DATA_URI1_PROCESSED = """// Simple file storage made with tools from Snap!

class ServerExtension {
  constructor(runtime) {
    this.runtime = runtime;
    this.serverURL = 'https://snapextensions.uni-goettingen.de/handleTextfile.php';
  }

  getInfo() {
    return {
      id: 'serverData',
      name: 'Server Data',
      color1: '#31b3d4',
      color2: '#179fc2',
      blocks: [
        {
          opcode: 'saveToServer',
          blockType: Scratch.BlockType.COMMAND,
          text: 'Save [variableName] with content [content]',
          arguments: {
            variableName: {
              type: Scratch.ArgumentType.STRING,
              defaultValue: 'default.txt',
            },
            content: {
              type: Scratch.ArgumentType.STRING,
              defaultValue: 'Hello, World!',
            },
          },
        },
        {
          opcode: 'loadFromServer',
          blockType: Scratch.BlockType.REPORTER,
          text: 'Load [variableName]',
          arguments: {
            variableName: {
              type: Scratch.ArgumentType.STRING,
              defaultValue: 'data.txt',
            },
          },
        },
      ],
    };
  }

  saveToServer(args, util) {
    const variableName = args.variableName;
    const content = args.content;

    const url =
      this.serverURL +
      '?type=write' +
      '&content=' +
      encodeURIComponent(content) +
      '&filename=./textfiles/' +
      encodeURIComponent(variableName);

    return fetch(url)
      .then(response => response.text())
      .then(result => (result === 'ok'))
      .catch(error => {
        console.error('Failed to save data:', error);
        return false;
      });
  }

  loadFromServer(args, util) {
    const variableName = args.variableName;

    const url =
      this.serverURL +
      '?type=read' +
      '&filename=./textfiles/' +
      encodeURIComponent(variableName);

    return fetch(url)
      .then(response => response.text())
      .catch(error => {
        console.error('Failed to load data:', error);
        return "can't get data";
      });
  }
}

Scratch.extensions.register(new ServerExtension());"""
DATA_URI2_RAW = "data:text/javascript,%28function%28Scratch%29%20%7B%0A%20%20%27use%20strict%27%3B%0A%0A%20%20if%20%28%21Scratch.extensions.unsandboxed%29%20%7B%0A%20%20%20%20throw%20new%20Error%28%27This%20Hello%20World%20example%20must%20run%20unsandboxed%27%29%3B%0A%20%20%7D%0A%0A%20%20class%20HelloWorld%20%7B%0A%20%20%20%20getInfo%28%29%20%7B%0A%20%20%20%20%20%20return%20%7B%0A%20%20%20%20%20%20%20%20id%3A%20%27helloworldunsandboxed%27%2C%0A%20%20%20%20%20%20%20%20name%3A%20%27Unsandboxed%20Hello%20World%27%2C%0A%20%20%20%20%20%20%20%20blocks%3A%20%5B%0A%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20opcode%3A%20%27hello%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20blockType%3A%20Scratch.BlockType.REPORTER%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20text%3A%20%27Hello%21%27%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%5D%0A%20%20%20%20%20%20%7D%3B%0A%20%20%20%20%7D%0A%20%20%20%20hello%28%29%20%7B%0A%20%20%20%20%20%20return%20%27World%21%27%3B%0A%20%20%20%20%7D%0A%20%20%7D%0A%20%20Scratch.extensions.register%28new%20HelloWorld%28%29%29%3B%0A%7D%29%28Scratch%29%3B"
DATA_URI2_PROCESSED = """(function(Scratch) {
  'use strict';

  if (!Scratch.extensions.unsandboxed) {
    throw new Error('This Hello World example must run unsandboxed');
  }

  class HelloWorld {
    getInfo() {
      return {
        id: 'helloworldunsandboxed',
        name: 'Unsandboxed Hello World',
        blocks: [
          {
            opcode: 'hello',
            blockType: Scratch.BlockType.REPORTER,
            text: 'Hello!'
          }
        ]
      };
    }
    hello() {
      return 'World!';
    }
  }
  Scratch.extensions.register(new HelloWorld());
})(Scratch);"""
    


def test_fetch_js_code_data_uri_with_b64():
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    code = fetch_js_code(DATA_URI1_RAW, tolerate_file_path=False)
    assert code == DATA_URI1_PROCESSED

def test_fetch_js_code_data_uri_without_b64():
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    code = fetch_js_code(DATA_URI2_RAW, tolerate_file_path=False)
    assert code == DATA_URI2_PROCESSED

def test_fetch_js_code_data_uri_invalid():
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    data_uri = DATA_URI1_RAW.replace(",", "#") # "," is required
    with raises(PP_InvalidExtensionCodeSourceError):
        fetch_js_code(data_uri, tolerate_file_path=False)


def test_fetch_js_code_url_invalid():
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    url = "https://extensions...penguinmod.com/extensions/MubiLop/toastnotifs.js" # "..."
    with raises(PP_InvalidExtensionCodeSourceError):
        fetch_js_code(url, tolerate_file_path=False)

def test_fetch_js_code_url_request_exception(monkeypatch: MonkeyPatch):
    def fake_requests_get(*args, **kwargs) -> str:
        # works offline too :)
        return FakeResponse(text="Hi :)", status_code=404)
        
    from pmp_manip.ext_info_gen import fetch_js as fetch_js_mod
    monkeypatch.setattr(fetch_js_mod, "requests_get", fake_requests_get)

    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    url = "https://extensions.penguinmod.com/extensions/NonExistantUser/NonExistantExt.js"
    with raises(PP_NetworkFetchError):
        fetch_js_code(url, tolerate_file_path=False) # internal 404

def test_fetch_js_code_url_unexpected_exception(monkeypatch: MonkeyPatch):
    def fake_requests_get(*args, **kwargs) -> str:
        raise Exception() # simulate some other exception being raised
    
    from pmp_manip.ext_info_gen import fetch_js as fetch_js_mod
    monkeypatch.setattr(fetch_js_mod, "requests_get", fake_requests_get)
        
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    url = "https://raw.githubusercontent.com/Logise1123/FirebaseDB-/refs/heads/main/db.js"
    with raises(PP_UnexpectedFetchError):
        fetch_js_code(url, tolerate_file_path=False)

def test_fetch_js_code_url_working(monkeypatch: MonkeyPatch):
    code = DATA_URI2_PROCESSED
    def fake_requests_get(*args, **kwargs) -> str:
        # works offline too :)
        return FakeResponse(text=code, status_code=200)
        
    from pmp_manip.ext_info_gen import fetch_js as fetch_js_mod
    monkeypatch.setattr(fetch_js_mod, "requests_get", fake_requests_get)
        
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    url = "https://xxx.yyy.zzz/aaa/bbb/ccc/iii.js"
    assert fetch_js_code(url, tolerate_file_path=False) == code


def test_fetch_js_code_file_invalid_path(monkeypatch: MonkeyPatch):
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    with raises(PP_InvalidExtensionCodeSourceError):
        fetch_js_code(25953, tolerate_file_path=True)
    
def test_fetch_js_code_file_not_allowed(monkeypatch: MonkeyPatch):
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    with raises(PP_InvalidExtensionCodeSourceError):
        fetch_js_code("vvv/aaa.xxx", tolerate_file_path=False)

def test_fetch_js_code_file_doesnt_exist(monkeypatch: MonkeyPatch):
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    with raises(PP_FileNotFoundError):
        fetch_js_code("www/bbb.yyy", tolerate_file_path=True)

def test_fetch_js_code_file_couldnt_read(monkeypatch: MonkeyPatch):
    def fake_read_file_text(*args, **kwargs) -> str:
        raise PP_FailedFileReadError()
    
    from pmp_manip.ext_info_gen import fetch_js as fetch_js_mod
    monkeypatch.setattr(fetch_js_mod, "read_file_text", fake_read_file_text)
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    
    with raises(PP_FileFetchError):
        fetch_js_code(__file__, tolerate_file_path=True)
    # i needed a file that exists, so ...

def test_fetch_js_code_file_success(monkeypatch: MonkeyPatch):
    def fake_read_file_text(*args, **kwargs) -> str:
        return "Günther Jauch"

    from pmp_manip.ext_info_gen import fetch_js as fetch_js_mod
    monkeypatch.setattr(fetch_js_mod, "read_file_text", fake_read_file_text)
    from pmp_manip.ext_info_gen.fetch_js import fetch_js_code
    
    assert fetch_js_code(__file__, tolerate_file_path=True) == "Günther Jauch"
# TODO: optimize