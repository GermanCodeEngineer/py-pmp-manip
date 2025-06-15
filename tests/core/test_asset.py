from copy   import copy
from io     import BytesIO
from lxml   import etree
from PIL    import Image
from pydub  import AudioSegment
from pytest import fixture, raises

from pypenguin.utility import (
    xml_equal, image_equal, generate_md5, ValidationConfig,
    TypeValidationError, InvalidValueError, ThanksError,
)

from pypenguin.core.asset import (
    FRCostume, FRSound, SRCostume, SRVectorCostume, SRBitmapCostume, SRSound, 
    EMPTY_SVG_COSTUME_XML, EMPTY_SVG_COSTUME_ROTATION_CENTER,
)

from tests.utility import execute_attr_validation_tests


SIMPLE_BITMAP_EXAMPLE = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xcf\xc0\xf0\x1f\x00\x05\x00\x01\xff\x89\x99=\x1d\x00\x00\x00\x00IEND\xaeB`\x82"

SIMPLE_SVG_EXAMPLE = b'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">\n  <circle cx="50" cy="50" r="40" fill="red" />\n</svg>'

SIMPLE_SOUND_EXAMPLE = b'RIFF\xec\x0b\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\xbb\x00\x00\x00w\x01\x00\x02\x00\x10\x00data\xc8\x0b\x00\x00^\x02V\x03\xc6\x04\xda\x06P\x08E\x08\x15\x07K\x05\x89\x03H\x02`\x01J\x00\xc8\xfe5\xfd\xfa\xfbS\xfb\x10\xfb^\xfa\x17\xf9\xbf\xf7`\xf7\x99\xf8\xf9\xfaJ\xfd\xc4\xfe\x92\xff2\x00\r\x01\xcb\x01\xf3\x01\x7f\x01r\x00\x9c\xff\xe9\xff+\x01\xa3\x02\xcc\x03~\x04\xb9\x04i\x04\xa2\x03\x93\x022\x01\xd2\xff=\xff\x8c\xffP\x00\xbb\x00\xd1\x00\n\x01v\x01\x86\x01\n\x01[\x00\xe0\xff\x99\xff3\xff\x92\xfe\xe3\xfdC\xfd~\xfc\x95\xfb\xbd\xfaR\xfa~\xfa5\xfb~\xfcj\xfe\x0f\x01h\x04\xfe\x07\xcb\ni\x0c\\\r\x1c\rG\n\xe0\x04\x93\xfe7\xf9H\xf5\xbf\xf2A\xf1\xaf\xf07\xf1\xf1\xf2\x9f\xf5\xf9\xf8\xdc\xfc!\x01\x89\x05\xe6\t\xc1\rS\x10\xf5\x10\xea\x0f5\r3\tO\x04\x15\xffa\xfa\xa1\xf6\x14\xf4\xd4\xf2\xad\xf2\x7f\xf3\x80\xf5<\xf8{\xfb\xc9\xfe\xb7\x018\x047\x06\xb5\x07\xb5\x08\xfb\x08~\x08\x8d\x07o\x06Q\x05>\x04\xd3\x02\xe9\x00\xe0\xfeH\xfdn\xfc\xf4\xfbz\xfb\x06\xfb\x04\xfb\xa6\xfb\x9c\xfc_\xfd\xaa\xfd\xcb\xfd\x0b\xfe\x98\xfeG\xff\xc1\xff\xe2\xff\xe2\xff\xf2\xff\x0e\x00D\x00\xae\x00C\x01\xc5\x01\n\x02H\x02\xdb\x02\xa5\x038\x04\x0b\x04D\x03\x1e\x02\xcf\x00\x86\xff~\xfe\x87\xfd\x01\xfc4\xf9x\xf5\x14\xf3\xc2\xf4\xd4\xf9=\xfem\x01U\x05\xfa\t\xcb\r\x9f\x0fF\x0f\x9d\rs\x0b@\t\x85\x06\x87\x02\xfb\xfd\xaf\xf90\xf6\x9c\xf3\xc5\xf1\xa1\xf0\xbd\xf06\xf2$\xf5s\xf9h\xfe\xef\x02C\x06\x06\x08J\x08\xee\x07Z\x07P\x06\x93\x046\x02\xa6\xff\xa9\xfdi\xfc\xe1\xfb\xfd\xfb\xad\xfc\xaf\xfd\xbc\xfe\xe8\xffQ\x01g\x02\xe1\x02#\x03\xbc\x03s\x04\x8b\x04\x82\x03\x1e\x02\x1e\x01\x93\x00$\x00\x86\xff\xd9\xfe^\xfe4\xfeN\xfes\xfe\x81\xfeo\xfe\\\xfeo\xfe\x9d\xfe\x92\xfe%\xfeF\xfdc\xfc\x86\xfc\x0e\xfe\xa7\x00}\x03\xc0\x05\xd2\x07\x8c\t\\\t\xbd\x06\xee\x02c\xff\x8f\xfc\n\xfa\xc3\xf7\t\xf6O\xf5\xbc\xf5\xcf\xf6\x0e\xf8\xd3\xf9s\xfc\xfe\xff)\x04\xcd\x07\\\n\xe8\x0br\x0c\xd8\x0b\n\n\x13\x07E\x03,\xffn\xfb~\xf8\xcf\xf6g\xf6\xdd\xf6-\xf8z\xfa\x19\xfdk\xff\x1c\x01U\x02V\x03\x04\x04O\x04*\x04\x96\x03\xd2\x02*\x02\xc6\x01g\x01\xe5\x00X\x00\xe8\xff\x88\xff.\xff\xfe\xfe3\xff\xb6\xff(\x00:\x00\xdf\xff]\xff\t\xff\x03\xff\xf4\xfe\xa0\xfe\xfc\xfd1\xfd\x8a\xfc?\xfcH\xfc\x8f\xfc\x18\xfd\xf2\xfd\x0c\xffC\x00\x82\x01\xeb\x02\xb2\x04h\x06O\x07!\x07%\x06\x00\x05\xeb\x03\xc3\x021\x01\x03\xff^\xfc*\xf9\xf8\xf4|\xf1c\xf1\x0b\xf5\xa0\xf9c\xfd\x96\x01\xb7\x06L\x0b\x0e\x0e\xc3\x0e\x0c\x0e\xc2\x0cl\x0b\x9c\tZ\x06\xbd\x01\x0e\xfd\xe0\xf8\xd0\xf5i\xf3x\xf1Z\xf0K\xf0\x83\xf1i\xf4\xc1\xf8\xb4\xfd\x08\x02,\x05K\x07h\x08\xbf\x08\x1a\x08.\x04P\x05E\x08\xc3\n\x0b\x0c\xfd\x0b\x03\x0bx\t!\x07\xc2\x03\xec\xff\x12\xfc\xd8\xf8Z\xf6\x8d\xf4\xf4\xf3\x1e\xf5\x91\xf7\xd3\xfaE\xfet\x01-\x04S\x06\xcf\x07M\x08\xdd\x07\xc1\x06*\x05\x8a\x03C\x02-\x01\x06\x00\xc2\xfe\x8a\xfd\x8d\xfc\xdb\xfb\x8c\xfb\xb4\xfbK\xfcZ\xfd\x9b\xfe\xad\xff~\x00\xee\x00\x12\x01\xe5\x00U\x00\x85\xff\xc3\xfeL\xfe?\xfeu\xfe\xab\xfe\xe8\xfe[\xff2\x00R\x01\x96\x02\xad\x03\x86\x04Y\x05"\x06}\x06\x17\x06\xde\x04\x15\x03\xf8\x00M\xfe\xb6\xfa\x06\xf6\xd7\xf1Z\xf1\xc7\xf4\x15\xf9\x1d\xfc\x90\xff\x81\x04\xe5\t\xaa\r\x1d\x0f\x98\x0eD\r\xa1\x0c\x0e\x0c\xc4\t\x1d\x05\xea\xfet\xf9+\xf6#\xf4\xa5\xf1\xfb\xee\x87\xed\xec\xee\xc4\xf2\x03\xf8k\xfd\xbf\x01C\x05I\x08\x97\n{\x0b\xcf\n\xb9\x08\xf0\x05*\x03\xd2\x00\xe1\xfe!\xfd\xc5\xfb\xf6\xfa\xc7\xfa^\xfb\x8c\xfc*\xfei\x00\xe8\x02\xad\x04m\x05\xa2\x05\xc6\x05\x8a\x05\x89\x04\xc7\x02\xd1\x00;\xff\xe0\xfd[\xfc\xd2\xfa\xc9\xf9\x99\xf9\x94\xfa\xb5\xfc/\xffS\x01\xfa\x02?\x04\xe7\x04\xcd\x04\x97\x03:\x01\xae\xfe\xed\xfc\x92\xfc\xa0\xfd?\xff\xac\x00\x02\x02?\x03\x8e\x03_\x02?\x00\x1d\xfeb\xfc1\xfb\x98\xfaX\xfa\x8c\xfaa\xfbZ\xfc^\xfd\xc5\xfe\xd4\x00|\x03.\x06/\x08*\tD\t\xdc\x08#\x08\xae\x06A\x04\x06\x01z\xfdi\xfa!\xf8\xdd\xf6\xb8\xf6\x83\xf7\x16\xf9o\xfby\xfe\xd1\x01\xab\x04\x8b\x06^\x07\x1f\x07:\x06\xf5\x04\\\x03\xc3\x01J\x00\xe5\xfe\xb1\xfd\xc0\xfc8\xfc\x00\xfc\xd1\xfb\xd9\xfbA\xfc\xfd\xfc\xf7\xfd\xec\xfe\xc9\xffx\x00\x92\x00<\x00\xb7\xff\x1e\xff\x9b\xfeP\xfe_\xfe\xe9\xfe\xa9\xffh\x00+\x01\xcf\x01S\x02\xfb\x02\xec\x03\xf8\x04\xcc\x05A\x06\x08\x06\xe1\x04\x0b\x03\x89\x00?\xfd\x10\xf9a\xf4\x0c\xf1c\xf1\x10\xf5\x07\xf9\xf6\xfc\xf8\x01\xa1\x077\x0c\xb3\x0e\x10\x0fS\x0e\xb0\rd\r\xeb\x0bH\x08\xca\x02\x88\xfc\xbd\xf7\xea\xf4\xd5\xf2\xa7\xf0\xca\xeen\xeeF\xf0,\xf4?\xf9<\xfey\x02\x17\x06\xe8\x08\xc8\n\x9a\x0b\xcb\ni\x08r\x05\x87\x02G\x00\x8d\xfeA\xfdg\xfc\x13\xfc\x7f\xfc\xb5\xfdM\xff\xcc\x00\xf1\x01\xc3\x021\x03\xce\x02W\x02V\x02p\x02\xd8\x01Q\x00\x8c\xfe\x90\xfd\xdb\xfc\x9c\xfb%\xfa\x95\xf9\xc9\xfa;\xfd\x01\x00E\x02\x16\x04\xd5\x05*\x07:\x07\t\x06\x83\x03B\x00\x9e\xfdp\xfc\x96\xfc\xe9\xfc\xde\xfc\\\xfd\x96\xfes\xff\xd4\xfe\x94\xfd\xc4\xfc\x9a\xfc\xc9\xfc\x0c\xfd\x0e\xfd3\xfd\xdd\xfd\xf9\xfe\x8f\x005\x02d\x03c\x04d\x050\x06\x82\x06<\x06\xa5\x05\xbe\x04D\x038\x01\xdc\xfe\xb5\xfc\r\xfb\xd4\xf9"\xf9\x16\xf9\x9e\xf9\xf6\xfa?\xfd\x13\x00\xde\x02\xe4\x04\x08\x06\x93\x06\x8a\x06\x0b\x06\x06\x05u\x03\x99\x01\xca\xffq\xfe\x8f\xfd\x0e\xfd\x11\xfd\x93\xfd\x13\xfe.\xfe\xc8\xfd`\xfd\\\xfdy\xfdX\xfd\x0f\xfd\xda\xfc\xee\xfc.\xfd4\xfd/\xfdu\xfd\xe5\xfdK\xfe\xc1\xfeZ\xff`\x00\xc1\x01*\x03\x7f\x04\xbc\x05\xd7\x06\xb1\x07\x08\x08\x99\x07\xa4\x06A\x05\xa1\x03\xbe\x01B\xff\xcc\xfb\x93\xf6+\xf0s\xec\xdd\xee#\xf5\xf8\xf9\xcf\xfdL\x03\x83\nu\x10\x92\x13Y\x13\'\x11\xec\x0f\x1d\x10\xe4\x0e\x97\t\xbc\x00S\xf7\xe6\xf0\xc3\xedJ\xebT\xe8\xe0\xe5S\xe6\x0c\xea\xd1\xf0\xd8\xf9%\x02\xd4\x07T\x0b_\x0es\x11&\x13\xc5\x11O\x0c\xe6\x04\xeb\xfd\xce\xf8\xff\xf5O\xf4}\xf3\xd5\xf3T\xf6X\xfbo\x01=\x06\x05\t4\x0b\xda\r:\x10q\x10W\x0e\xda\n\xfa\x06\xce\x02H\xfe\xf6\xf9*\xf6\xed\xf2w\xf0\xf1\xee\xdc\xee\x91\xf0\x02\xf4\xcd\xf8[\xfe\x92\x03\xe0\x07\xd2\n\x14\x0c\x95\x0b\x19\t;\x05\x00\x02\x18\x01d\x02\xa3\x03\xce\x03\xbc\x04l\x06\x8c\x054\x01\xf5\xfb\xd7\xf7\xa4\xf4\x1a\xf2e\xf0\x8b\xef\xd0\xf0\xd6\xf3t\xf7}\xfb\xda\xff-\x04W\x08b\x0c\xf0\x0fQ\x12F\x13\x9b\x12\xaa\x10U\rL\x08\x19\x02B\xfc\x98\xf7\x01\xf4\x87\xf0p\xeb\'\xe6\xf7\xe4\xba\xeb\xc4\xf3\xd6\xfaB\x02\xe1\x08\xa1\r\xc7\x118\x14e\x14M\x14\t\x14\x9f\x12{\x0e\xea\x06o\xfd\x8f\xf5\xbf\xf0S\xee\x8d\xec?\xea\xb6\xe8E\xe9\x8b\xecw\xf2\x84\xf9m\x00)\x06h\n\x12\x0e\x00\x11\xfe\x11\x9d\x0f\x14\x0b\xfd\x05q\x01\xa4\xfd\xa9\xfa\xed\xf8\xc4\xf8\xd8\xf9\xb5\xfb\x16\xfe\xc9\x00N\x03-\x05A\x06\x9e\x06\xe6\x06\xc5\x06G\x05\xc7\x01\x9f\xfcw\xf6\xd7\xf0\x00\xef"\xf2m\xf7#\xfc\xb8\x00\x01\x06\xc2\x0b\x97\x10q\x12\x85\x11\x8b\x10?\x11\xd3\x10[\x0c\x0b\x04N\xfav\xf24\xed\xc6\xe9\xeb\xe6\xa4\xe3R\xe2\x19\xe5\x14\xebX\xf2\xed\xf9/\x01\xd0\x07\xb0\r\xf9\x12h\x175\x1a\xa8\x1a\xa3\x17\xfd\x10P\x08]\xff6\xf7\xfa\xefJ\xeb\xe7\xea\x94\xec\x9c\xee}\xf2\xe8\xf8a\x01\x0e\t\xc7\rM\x100\x12,\x16\xe9\x18\xb8\x17z\x13\xfd\x0b\xac\x02b\xfa\xb3\xf3\xc1\xee^\xeb\xfc\xe78\xe4\xaf\xe2\xbe\xe4/\xea\xa1\xf2\xac\xfb\xb5\x03\xcd\t0\x0ed\x11]\x13\xa5\x14j\x15\xe4\x14\x82\x12\xc4\x0e]\n\x8e\x04~\xfd\t\xf7\xe9\xf1\x1d\xee`\xeb\x07\xe9\x1e\xe8\x1d\xea\x04\xef\x01\xf6\xa8\xfd\xee\x04g\x0b\x87\x103\x15\xbc\x19o\x1cL\x1aW\x13c\x08S\xfe\x91\xf6f\xeex\xe9\x04\xe9,\xe8\xc0\xe8\xad\xee~\xf8X\x01\xb8\x07|\x0b\x18\x0e\xeb\x13\xb1\x1a\x8b\x1d\xc6\x18\xc5\x0cj\x00Z\xf8i\xf3^\xf0\x0f\xec\x80\xe4\x0b\xe0\xfc\xe0X\xe6\xeb\xf0P\xfc\x8a\x04\x9f\n\x04\x10L\x16r\x1c\xd7\x1eY\x1b1\x13\x0c\nv\x01e\xfal\xf5\x1c\xf2\xc3\xef\xa6\xed\x89\xecu\xee.\xf3W\xf8\xac\xfcD\x00\xb4\x03\x07\x07E\tK\nV\nD\t\r\x08A\x07:\x07\xd1\x07\x8c\x07,\x06\xcf\x05\xa7\x075\n\xc6\n\xbb\x07\xe3\x01\xbd\xfa\xf0\xf3\xeb\xee\xd3\xea)\xe8\xe4\xe6\xb5\xe6\x14\xe8\xa6\xea\x85\xee|\xf4I\xfbv\x02)\nZ\x11\xb5\x17"\x1c\x91\x1d\xe2\x1c\xb5\x19I\x143\x0c\x15\x02\x9c\xf8\x80\xf0\xfa\xeb\xad\xeb\xec\xeb\xaf\xect\xf0l\xf6l\xfdm\x03\xd2\x07^\x0b\x86\r\xee\x0f2\x13\xae\x14\xb0\x13\x05\x10\xd2\t\xb7\x02\x04\xfb\xca\xf3|\xee\xfc\xea\xc0\xe9\x0c\xebM\xec\xb4\xebO\xe9s\xe7x\xe9\x02\xf1\xf3\xfb\x87\x066\x0e5\x13j\x16q\x19\xa9\x1e\x94!\x9b\x1e5\x1bI\x151\n\xd8\xfe\x0c\xf6\xfe\xee\xe2\xe9\xbd\xe6\x1c\xe5\x9f\xe5\xce\xe8\x17\xee\x98\xf5t\xffx\t\xc1\x12\xb2\x19\x03\x1c\x96\x1a<\x14W\t"\xfd\x07\xf2\x8a\xeb\x8d\xe8R\xe6H\xe71\xefI\xfa\xd5\x03M\n\xe5\r\x8f\x12/\x1aH\x1ed\x1b\x01\x11 \x03X\xf9.\xf3g\xef@\xed\xe2\xe9\xd1\xe3\xec\xf0\x11\xf0\x9d\xed\xd4\xeeJ\xf0\xe5\xef\xf0\xef8\xf3\xb3\xf7\\\xfa\xa9\xfc#\x00|\x04\x1b\x08&\t\x9e\t\x95\x0b\xf4\r\xc4\x0f\xd3\x0f7\rQ\nF\nv\x0bI\n)\x06\x9d\x01\x1d\xfd&\xf9\xc2\xf5\x97\xf2\xec\xef\x1c\xee\xcc\xec\x0f\xeb\xbe\xe8\x99\xe7\x91\xea\x1c\xf2\x05\xfb4\x01T\x07\xa7\x0e\r\x15W\x19(\x1al\x19\xe7\x1a\xfa\x1c\x03\x1c\x0c\x16\xff\x0b,\x023\xfa\x06\xf3\x94\xed\x86\xea\xd9\xe8\xbe\xe8F\xe6\xa7\xe0k\xdf\x17\xe6\x08\xf2\n\xfff\x08!\r\xf0\x0fz\x12\xdc\x14\x14\x18~\x1cK!\x0e#\x1e\x1a\xd6\n8\xfeZ\xf5\xdb\xf0\xbb\xed\xb7\xe9\xd1\xe5\xdc\xdf\\\xda6\xdb\xea\xe3\x9b\xf2\xed\xff0\tx\x0f\x0e\x14\xd2\x17\x88\x1d\xf7$q%R\x1d\xc9\x104\x03\x9a\xfa\x89\xf5<\xf1\x11\xed\xdb\xe6q\xe1b\xe0L\xe4`\xed\xe2\xf8\xbf\x02\x19\n\\\x0fr\x13w\x17\r\x1c\xb1\x1e\xc9\x1bj\x14r\x0b\xd2\x02u\xfcz\xf7F\xf17\xebS\xe7d\xe6\xeb\xe7<\xeb\x86\xf1\xf2\xf9\xc4\xff\xfc\x01\xa9\x02\xfb\x04|\x08\xf4\tz\x07M\x03\x1f\x03\xd6\t\xc0\x13:\x16Q\x0f\xd8\x0ba\x0e\x1e\x0c\x18\x03\xc0\xf9\x88\xf5\xfc\xf6\xaa\xf8\x1c\xf6n\xf1\x8a\xf1\x1a\xf5\xf4\xf7"\xfa\xc4\xff\xa0\x061\x08\xd9\x02v\xfb,\xf68\xf2\xfd\xee[\xf0\x9b\xf40\xf9\x87\x01t\n\xc6\x0fV\x13\xfc\x15\xc7\x17m\x1b\xc0"y"@\x17\xa0\x08\xb4\xfb\xb4\xf2\x86\xed7\xe9\x91\xe4\xb0\xde\xfe\xd8\x9b\xd7\xb4\xde\xb5\xedZ\xfc,\x07\x82\r\xf6\x11%\x16I\x1c\xad$\xd0&\xd6\x1e\xe6\x10\xe5\x026\xfa\x01\xf6\xb5\xf2\x98\xee\xb8\xeah\xe5\x0f\xdd=\xdd\xed\xe8\x8b\xf7\xc9\x03\xba\x0b\xd4\x0fn\x13\x1c\x17|\x1b\xe2 )#\xe7\x1d\t\x12S\x04\xd7\xf9\x9a\xf3\x08\xefs\xeb\x99\xe6-\xe4\x80\xe5\x9f\xe5$\xe7\x12\xf0\x0e\xfeL\x0b\xe0\x11\xe6\x11Z\x10>\r\x93\t\x0e\x07+\x05@\x01R\xfe\xbb\x00\xbb\x05\xbc\n_\x0bz\x0b\xe3\x10\xf3\x13\xc4\rS\x034\xf7\x96\xef]\xed=\xeb\xba\xe6&\xe3)\xe4\xa5\xe5\xe9\xe7d\xf0\xbd\xfe\xc9\x0c2\x15\xbb\x15\x15\x15\xd8\x14s\x12\x84\x0f\x97\x0b\xb6\x04t\xfeh\xfcG\xfdk\x00k\x04\xfb\x04\x99\x02\xcc\x02\x05\x07\xb3\n\x1d\x0c\xf8\x08\xb8\xff\x8d\xf8x\xf6J\xf4\xfe\xee\x8c\xe7@\xe1\x0c\xe1\xb4\xea\xba\xf94\x05\xe6\x0b\xd0\x0f\xa8\x13\xc3\x19\xda \xc1"c\x1cY\x0f\xb4\x01w\xf8\\\xf3\xc1\xf0K\xec\xe7\xe3O\xe1d\xe5\xa6\xebe\xf6\xc3\x01\xfd\x08i\x0ew\x12\xcf\x15\xaa\x1c\xff#(\x1fI\x11'
# TODO: import from constants

@fixture
def config():
    return ValidationConfig()

@fixture
def bitmap_example():
    content = Image.open(BytesIO(SIMPLE_BITMAP_EXAMPLE))
    content.load()
    return content

@fixture
def sound_example():
    return AudioSegment.from_file(
        BytesIO(SIMPLE_SOUND_EXAMPLE),
        format="wav",
    )



def test_FRCostume_from_data():
    costume_data = {
        "name": "my costume", 
        "assetId": "051321321c93ae7b61222de62e77ae40", 
        "dataFormat": "svg", 
        "md5ext": "051321321c93ae7b61222de62e77ae40.svg", 
        "rotationCenterX": 381.2306306306307, 
        "rotationCenterY": 197.11651651651664,
        "bitmapResolution": 1, 
    }
    frcostume = FRCostume.from_data(costume_data)
    assert isinstance(frcostume, FRCostume)
    assert frcostume.name == costume_data["name"]
    assert frcostume.asset_id == costume_data["assetId"]
    assert frcostume.data_format == costume_data["dataFormat"]
    assert frcostume.md5ext == costume_data["md5ext"]
    assert frcostume.rotation_center_x == costume_data["rotationCenterX"]
    assert frcostume.rotation_center_y == costume_data["rotationCenterY"]
    assert frcostume.bitmap_resolution == costume_data["bitmapResolution"]

def test_FRCostume_from_data_missing_md5ext():
    costume_data = {
        "name": "my costume", 
        "assetId": "051321321c93ae7b61222de62e77ae40", 
        "dataFormat": "svg", 
        "rotationCenterX": 381.2306306306307, 
        "rotationCenterY": 197.11651651651664,
        "bitmapResolution": 1, 
    }
    frcostume = FRCostume.from_data(costume_data)
    assert isinstance(frcostume, FRCostume)
    assert frcostume.md5ext == "051321321c93ae7b61222de62e77ae40.svg"


def test_FRCostume_from_data_missing_bitmap_resolution():
    costume_data = {
        "name": "my costume", 
        "assetId": "051321321c93ae7b61222de62e77ae40", 
        "dataFormat": "svg", 
        "md5ext": "051321321c93ae7b61222de62e77ae40.svg", 
        "rotationCenterX": 381.2306306306307, 
        "rotationCenterY": 197.11651651651664,
    }
    srcostume = FRCostume.from_data(costume_data)
    assert srcostume.bitmap_resolution == None


def test_FRCostume_to_second_vector():
    frcostume = FRCostume(
        name="my costume",
        asset_id="051321321c93ae7b61222de62e77ae40",
        data_format="svg",
        md5ext="051321321c93ae7b61222de62e77ae40.svg",
        rotation_center_x=381.2306306306307,
        rotation_center_y=197.11651651651664,
        bitmap_resolution=1,
    )
    srcostume = frcostume.to_second(asset_files={"051321321c93ae7b61222de62e77ae40.svg": SIMPLE_SVG_EXAMPLE})
    assert isinstance(srcostume, SRVectorCostume)
    assert srcostume.name == frcostume.name
    assert srcostume.file_extension == frcostume.data_format
    assert srcostume.rotation_center == (frcostume.rotation_center_x, frcostume.rotation_center_y)
    assert isinstance(srcostume.content, etree._Element)
    assert xml_equal(srcostume.content, etree.fromstring(SIMPLE_SVG_EXAMPLE))

def test_FRCostume_to_second_double_resolution():
    frcostume = FRCostume(
        name="Puppy Back",
        asset_id="05630bfa94501a3e5d61ce443a0cea70",
        data_format="png",
        md5ext="05630bfa94501a3e5d61ce443a0cea70.png",
        rotation_center_x=234,
        rotation_center_y=94,
        bitmap_resolution=2,
    )
    srcostume = frcostume.to_second(asset_files={"05630bfa94501a3e5d61ce443a0cea70.png": SIMPLE_BITMAP_EXAMPLE})
    assert isinstance(srcostume, SRBitmapCostume)
    assert srcostume.name == frcostume.name
    assert srcostume.file_extension == frcostume.data_format
    assert srcostume.rotation_center == (frcostume.rotation_center_x, frcostume.rotation_center_y)
    assert srcostume.has_double_resolution
    assert isinstance(srcostume.content, Image.Image)
    expected = Image.open(BytesIO(SIMPLE_BITMAP_EXAMPLE))
    expected.load()
    assert image_equal(srcostume.content, expected)

def test_FRCostume_to_second_simple_resolution():
    frcostume = FRCostume(
        name="Puppy Back",
        asset_id="05630bfa94501a3e5d61ce443a0cea70",
        data_format="png",
        md5ext="05630bfa94501a3e5d61ce443a0cea70.png",
        rotation_center_x=234,
        rotation_center_y=94,
        bitmap_resolution=1,
    )
    srcostume = frcostume.to_second(asset_files={"05630bfa94501a3e5d61ce443a0cea70.png": SIMPLE_BITMAP_EXAMPLE})
    assert isinstance(srcostume, SRBitmapCostume)
    assert not srcostume.has_double_resolution

def test_FRCostume_to_second_other_resolution():
    frcostume = FRCostume(
        name="Puppy Back",
        asset_id="05630bfa94501a3e5d61ce443a0cea70",
        data_format="png",
        md5ext="05630bfa94501a3e5d61ce443a0cea70.png",
        rotation_center_x=234,
        rotation_center_y=94,
        bitmap_resolution=3,
    )
    with raises(ThanksError):
        frcostume.to_second(asset_files={"05630bfa94501a3e5d61ce443a0cea70.png": SIMPLE_BITMAP_EXAMPLE})

def test_FRCostume_to_second_invalid_format():
    frcostume = FRCostume(
        name="Puppy Back",
        asset_id="05630bfa94501a3e5d61ce443a0cea70",
        data_format="png",
        md5ext="05630bfa94501a3e5d61ce443a0cea70.png",
        rotation_center_x=234,
        rotation_center_y=94,
        bitmap_resolution=2,
    )
    with raises(ThanksError):
        frcostume.to_second(asset_files={
            "05630bfa94501a3e5d61ce443a0cea70.png": b"\xc4;#\xb2\xff \xa2e\xa6hJc#*>\x02\x01V\x1c#\x8e)\xe0sZ\x16S_B\xad\xb2p\xfd\xe0\x96\xe0\x06\xc9)mKu\x17\x08jmq\xf9\x83\xe0U\xee\xe5a\xb6'xC\x9e8S\xcbgeq\x1f\x0b\r\x115~\x8d\xd0\x0e\xc5",
        })



def test_FRSound_from_data():
    sound_data = {
        "name": "pop", 
        "assetId": "83a9787d4cb6f3b7632b4ddfebf74367", 
        "dataFormat": "wav",
        "md5ext": "83a9787d4cb6f3b7632b4ddfebf74367.wav", 
        "rate": 48000, 
        "sampleCount": 1123, 
    }
    frsound = FRSound.from_data(sound_data)
    assert isinstance(frsound, FRSound)
    assert frsound.name == sound_data["name"]
    assert frsound.asset_id == sound_data["assetId"]
    assert frsound.data_format == sound_data["dataFormat"]
    assert frsound.md5ext == sound_data["md5ext"]
    assert frsound.rate == sound_data["rate"]
    assert frsound.sample_count == sound_data["sampleCount"]


def test_FRSound_to_second():
    frsound = FRSound(
        name="pop",
        asset_id="83a9787d4cb6f3b7632b4ddfebf74367",
        data_format="wav",
        md5ext="83a9787d4cb6f3b7632b4ddfebf74367.wav",
        rate=48000,
        sample_count=1123,
    )
    srsound = frsound.to_second(asset_files={"83a9787d4cb6f3b7632b4ddfebf74367.wav": SIMPLE_SOUND_EXAMPLE})
    assert isinstance(srsound, SRSound)
    assert srsound.name == frsound.name
    assert srsound.file_extension == frsound.data_format
    assert isinstance(srsound.content, AudioSegment)
    expected = AudioSegment.from_file(BytesIO(SIMPLE_SOUND_EXAMPLE))
    assert srsound.content == expected


def test_SRCostume_init():
    with raises(TypeError):
        SRCostume(
            name="my costume",
            file_extension="png",
            rotation_center=(-20, 15.6),
        )



def test_SRVectorCostume_create_empty(config):
    srcostume = SRVectorCostume.create_empty(name="some costume name")
    assert isinstance(srcostume, SRVectorCostume)
    assert srcostume.name == "some costume name"
    assert srcostume.file_extension == "svg"
    assert srcostume.rotation_center == EMPTY_SVG_COSTUME_ROTATION_CENTER
    assert isinstance(srcostume.content, etree._Element)
    assert xml_equal(srcostume.content, etree.fromstring(EMPTY_SVG_COSTUME_XML))


def test_SRVectorCostume_eq_equal():
    a = SRVectorCostume.create_empty(name="c")
    b = SRVectorCostume.create_empty(name="c")
    assert a == b

def test_SRVectorCostume_eq_super():
    a = SRVectorCostume.create_empty(name="Bob")
    b = SRVectorCostume.create_empty(name="Anne")
    assert a != b

def test_SRVectorCostume_eq_different_content():
    a = SRVectorCostume.create_empty()
    a.content = etree.fromstring('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="2" height="2" viewBox="-1 -1 2 2">  <!-- Exported by Scratch - http://scratch.mit.edu/ --><circle cx="0" cy="0" r="0.5" fill="red"/></svg>')
    b = SRVectorCostume.create_empty()
    b.content = etree.fromstring('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="2" height="2" viewBox="-1 -1 2 2">  <!-- Exported by Scratch - http://scratch.mit.edu/ --><circle cx="0" cy="0" r="0.5" fill="blue"/></svg>')
    assert a != b


def test_SRVectorCostume_validate(config):
    srcostume = SRVectorCostume(
        name="my costume",
        file_extension="svg",
        rotation_center=(-20, 15.6),
        content=etree.fromstring(EMPTY_SVG_COSTUME_XML),
    )
    srcostume.validate([], config)
    
    execute_attr_validation_tests(
        obj=srcostume,
        attr_tests=[
            ("name", 5, TypeValidationError),
            ("file_extension", {}, TypeValidationError),
            ("file_extension", "jpg", InvalidValueError),
            ("rotation_center", [], TypeValidationError),
            ("content", "<svg></svg>", TypeValidationError),
        ],
        validate_func=SRVectorCostume.validate,
        func_args=[[], config],
    )


def test_SRVectorCostume_to_first():
    content = etree.fromstring(SIMPLE_SVG_EXAMPLE)
    srcostume = SRVectorCostume(
        name="my costume",
        file_extension="svg",
        rotation_center=(381.2306306306307, 197.11651651651664),
        content=content,
    )
    frcostume, file_bytes = srcostume.to_first()
    md5 = generate_md5(file_bytes)
    assert isinstance(frcostume, FRCostume)
    assert frcostume.name == frcostume.name
    assert frcostume.asset_id == md5
    assert frcostume.data_format == srcostume.file_extension
    assert frcostume.md5ext == f"{md5}.svg"
    assert frcostume.rotation_center_x == srcostume.rotation_center[0]
    assert frcostume.rotation_center_y == srcostume.rotation_center[1]
    assert frcostume.bitmap_resolution is None
    assert xml_equal(etree.fromstring(file_bytes), content)



def test_SRBitmapCostume_eq_equal(config, bitmap_example):
    a = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=bitmap_example,
        has_double_resolution=False,
    )
    b = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=copy(bitmap_example),
        has_double_resolution=False,
    )
    assert a.content != b.content
    assert a == b

def test_SRBitmapCostume_eq_super(config, bitmap_example):
    a = SRBitmapCostume(
        name="my first costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=bitmap_example,
        has_double_resolution=False,
    )
    b = SRBitmapCostume(
        name="my second costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=bitmap_example,
        has_double_resolution=False,
    )
    assert a != b

def test_SRBitmapCostume_eq_different_has_double_resolution(config, bitmap_example):
    a = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=bitmap_example,
        has_double_resolution=False,
    )
    b = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=bitmap_example,
        has_double_resolution=True,
    )
    assert a != b

def test_SRBitmapCostume_eq_different_content(config):
    a = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=Image.new("RGB", (16, 16), color="red"),
        has_double_resolution=False,
    )
    b = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(0, 0),
        content=Image.new("RGB", (16, 16), color="blue"),
        has_double_resolution=False,
    )
    assert a != b

def test_SRBitmapCostume_validate(config, bitmap_example):
    srcostume = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(-20, 15.6),
        content=bitmap_example,
        has_double_resolution=False,
    )
    srcostume.validate([], config)
    
    execute_attr_validation_tests(
        obj=srcostume,
        attr_tests=[
            ("name", 5, TypeValidationError),
            ("file_extension", {}, TypeValidationError),
            ("rotation_center", [], TypeValidationError),
            ("content", b"\x89PNG", TypeValidationError),
            ("has_double_resolution", "hi", TypeValidationError),
        ],
        validate_func=SRBitmapCostume.validate,
        func_args=[[], config],
    )


def test_SRBitmapCostume_to_first(bitmap_example):
    srcostume = SRBitmapCostume(
        name="my costume",
        file_extension="png",
        rotation_center=(-20, 15.6),
        content=bitmap_example,
        has_double_resolution=False,
    )
    frcostume, file_bytes = srcostume.to_first()
    md5 = generate_md5(file_bytes)
    assert isinstance(frcostume, FRCostume)
    assert frcostume.name == frcostume.name
    assert frcostume.asset_id == md5
    assert frcostume.data_format == srcostume.file_extension
    assert frcostume.md5ext == f"{md5}.png"
    assert frcostume.rotation_center_x == srcostume.rotation_center[0]
    assert frcostume.rotation_center_y == srcostume.rotation_center[1]
    assert frcostume.bitmap_resolution == 1
    result = Image.open(BytesIO(file_bytes))
    result.load()
    assert image_equal(result, bitmap_example)




def test_SRSound_validate(config, sound_example):
    srsound = SRSound(
        name="Hello there!",
        file_extension="wav",
        content=sound_example,
    )
    srsound.validate(path=[], config=config)
    
    execute_attr_validation_tests(
        obj=srsound,
        attr_tests=[
            ("name", 5, TypeValidationError),
            ("file_extension", {}, TypeValidationError),
            ("content", b"123456", TypeValidationError),
        ],
        validate_func=SRSound.validate,
        func_args=[[], config],
    )


def test_SRSound_to_first():
    content = AudioSegment.from_file(BytesIO(SIMPLE_SOUND_EXAMPLE))
    srsound = SRSound(
        name="pop",
        file_extension="wav",
        content=content,
    )
    frsound, file_bytes = srsound.to_first()
    md5 = generate_md5(file_bytes)
    assert isinstance(frsound, FRSound)
    assert frsound.name == srsound.name
    assert frsound.asset_id == md5
    assert frsound.data_format == srsound.file_extension
    assert frsound.md5ext == f"{md5}.wav"
    assert frsound.rate == 48000
    assert frsound.sample_count == 1508 # does not match; Scratch shows 1123
    # rate and sample_count possibly not matching the original is fine here. This is Scratch's fault.
    assert AudioSegment.from_file(BytesIO(file_bytes)) == content

