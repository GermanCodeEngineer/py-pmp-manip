"use strict";
var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};

// node_modules/format-message-parse/index.js
var require_format_message_parse = __commonJS({
  "node_modules/format-message-parse/index.js"(exports2, module2) {
    "use strict";
    var ARG_OPN = "{";
    var ARG_CLS = "}";
    var ARG_SEP = ",";
    var NUM_ARG = "#";
    var TAG_OPN = "<";
    var TAG_CLS = ">";
    var TAG_END = "</";
    var TAG_SELF_CLS = "/>";
    var ESC = "'";
    var OFFSET = "offset:";
    var simpleTypes = [
      "number",
      "date",
      "time",
      "ordinal",
      "duration",
      "spellout"
    ];
    var submTypes = [
      "plural",
      "select",
      "selectordinal"
    ];
    exports2 = module2.exports = function parse2(pattern, options) {
      return parseAST({
        pattern: String(pattern),
        index: 0,
        tagsType: options && options.tagsType || null,
        tokens: options && options.tokens || null
      }, "");
    };
    function parseAST(current, parentType) {
      var pattern = current.pattern;
      var length = pattern.length;
      var elements = [];
      var start = current.index;
      var text = parseText(current, parentType);
      if (text) elements.push(text);
      if (text && current.tokens) current.tokens.push(["text", pattern.slice(start, current.index)]);
      while (current.index < length) {
        if (pattern[current.index] === ARG_CLS) {
          if (!parentType) throw expected(current);
          break;
        }
        if (parentType && current.tagsType && pattern.slice(current.index, current.index + TAG_END.length) === TAG_END) break;
        elements.push(parsePlaceholder(current));
        start = current.index;
        text = parseText(current, parentType);
        if (text) elements.push(text);
        if (text && current.tokens) current.tokens.push(["text", pattern.slice(start, current.index)]);
      }
      return elements;
    }
    function parseText(current, parentType) {
      var pattern = current.pattern;
      var length = pattern.length;
      var isHashSpecial = parentType === "plural" || parentType === "selectordinal";
      var isAngleSpecial = !!current.tagsType;
      var isArgStyle = parentType === "{style}";
      var text = "";
      while (current.index < length) {
        var char = pattern[current.index];
        if (char === ARG_OPN || char === ARG_CLS || isHashSpecial && char === NUM_ARG || isAngleSpecial && char === TAG_OPN || isArgStyle && isWhitespace(char.charCodeAt(0))) {
          break;
        } else if (char === ESC) {
          char = pattern[++current.index];
          if (char === ESC) {
            text += char;
            ++current.index;
          } else if (
            // only when necessary
            char === ARG_OPN || char === ARG_CLS || isHashSpecial && char === NUM_ARG || isAngleSpecial && char === TAG_OPN || isArgStyle
          ) {
            text += char;
            while (++current.index < length) {
              char = pattern[current.index];
              if (char === ESC && pattern[current.index + 1] === ESC) {
                text += ESC;
                ++current.index;
              } else if (char === ESC) {
                ++current.index;
                break;
              } else {
                text += char;
              }
            }
          } else {
            text += ESC;
          }
        } else {
          text += char;
          ++current.index;
        }
      }
      return text;
    }
    function isWhitespace(code) {
      return code >= 9 && code <= 13 || code === 32 || code === 133 || code === 160 || code === 6158 || code >= 8192 && code <= 8205 || code === 8232 || code === 8233 || code === 8239 || code === 8287 || code === 8288 || code === 12288 || code === 65279;
    }
    function skipWhitespace(current) {
      var pattern = current.pattern;
      var length = pattern.length;
      var start = current.index;
      while (current.index < length && isWhitespace(pattern.charCodeAt(current.index))) {
        ++current.index;
      }
      if (start < current.index && current.tokens) {
        current.tokens.push(["space", current.pattern.slice(start, current.index)]);
      }
    }
    function parsePlaceholder(current) {
      var pattern = current.pattern;
      if (pattern[current.index] === NUM_ARG) {
        if (current.tokens) current.tokens.push(["syntax", NUM_ARG]);
        ++current.index;
        return [NUM_ARG];
      }
      var tag = parseTag(current);
      if (tag) return tag;
      if (pattern[current.index] !== ARG_OPN) throw expected(current, ARG_OPN);
      if (current.tokens) current.tokens.push(["syntax", ARG_OPN]);
      ++current.index;
      skipWhitespace(current);
      var id = parseId(current);
      if (!id) throw expected(current, "placeholder id");
      if (current.tokens) current.tokens.push(["id", id]);
      skipWhitespace(current);
      var char = pattern[current.index];
      if (char === ARG_CLS) {
        if (current.tokens) current.tokens.push(["syntax", ARG_CLS]);
        ++current.index;
        return [id];
      }
      if (char !== ARG_SEP) throw expected(current, ARG_SEP + " or " + ARG_CLS);
      if (current.tokens) current.tokens.push(["syntax", ARG_SEP]);
      ++current.index;
      skipWhitespace(current);
      var type = parseId(current);
      if (!type) throw expected(current, "placeholder type");
      if (current.tokens) current.tokens.push(["type", type]);
      skipWhitespace(current);
      char = pattern[current.index];
      if (char === ARG_CLS) {
        if (current.tokens) current.tokens.push(["syntax", ARG_CLS]);
        if (type === "plural" || type === "selectordinal" || type === "select") {
          throw expected(current, type + " sub-messages");
        }
        ++current.index;
        return [id, type];
      }
      if (char !== ARG_SEP) throw expected(current, ARG_SEP + " or " + ARG_CLS);
      if (current.tokens) current.tokens.push(["syntax", ARG_SEP]);
      ++current.index;
      skipWhitespace(current);
      var arg;
      if (type === "plural" || type === "selectordinal") {
        var offset = parsePluralOffset(current);
        skipWhitespace(current);
        arg = [id, type, offset, parseSubMessages(current, type)];
      } else if (type === "select") {
        arg = [id, type, parseSubMessages(current, type)];
      } else if (simpleTypes.indexOf(type) >= 0) {
        arg = [id, type, parseSimpleFormat(current)];
      } else {
        var index = current.index;
        var format = parseSimpleFormat(current);
        skipWhitespace(current);
        if (pattern[current.index] === ARG_OPN) {
          current.index = index;
          format = parseSubMessages(current, type);
        }
        arg = [id, type, format];
      }
      skipWhitespace(current);
      if (pattern[current.index] !== ARG_CLS) throw expected(current, ARG_CLS);
      if (current.tokens) current.tokens.push(["syntax", ARG_CLS]);
      ++current.index;
      return arg;
    }
    function parseTag(current) {
      var tagsType = current.tagsType;
      if (!tagsType || current.pattern[current.index] !== TAG_OPN) return;
      if (current.pattern.slice(current.index, current.index + TAG_END.length) === TAG_END) {
        throw expected(current, null, "closing tag without matching opening tag");
      }
      if (current.tokens) current.tokens.push(["syntax", TAG_OPN]);
      ++current.index;
      var id = parseId(current, true);
      if (!id) throw expected(current, "placeholder id");
      if (current.tokens) current.tokens.push(["id", id]);
      skipWhitespace(current);
      if (current.pattern.slice(current.index, current.index + TAG_SELF_CLS.length) === TAG_SELF_CLS) {
        if (current.tokens) current.tokens.push(["syntax", TAG_SELF_CLS]);
        current.index += TAG_SELF_CLS.length;
        return [id, tagsType];
      }
      if (current.pattern[current.index] !== TAG_CLS) throw expected(current, TAG_CLS);
      if (current.tokens) current.tokens.push(["syntax", TAG_CLS]);
      ++current.index;
      var children = parseAST(current, tagsType);
      var end = current.index;
      if (current.pattern.slice(current.index, current.index + TAG_END.length) !== TAG_END) throw expected(current, TAG_END + id + TAG_CLS);
      if (current.tokens) current.tokens.push(["syntax", TAG_END]);
      current.index += TAG_END.length;
      var closeId = parseId(current, true);
      if (closeId && current.tokens) current.tokens.push(["id", closeId]);
      if (id !== closeId) {
        current.index = end;
        throw expected(current, TAG_END + id + TAG_CLS, TAG_END + closeId + TAG_CLS);
      }
      skipWhitespace(current);
      if (current.pattern[current.index] !== TAG_CLS) throw expected(current, TAG_CLS);
      if (current.tokens) current.tokens.push(["syntax", TAG_CLS]);
      ++current.index;
      return [id, tagsType, { children }];
    }
    function parseId(current, isTag) {
      var pattern = current.pattern;
      var length = pattern.length;
      var id = "";
      while (current.index < length) {
        var char = pattern[current.index];
        if (char === ARG_OPN || char === ARG_CLS || char === ARG_SEP || char === NUM_ARG || char === ESC || isWhitespace(char.charCodeAt(0)) || isTag && (char === TAG_OPN || char === TAG_CLS || char === "/")) break;
        id += char;
        ++current.index;
      }
      return id;
    }
    function parseSimpleFormat(current) {
      var start = current.index;
      var style = parseText(current, "{style}");
      if (!style) throw expected(current, "placeholder style name");
      if (current.tokens) current.tokens.push(["style", current.pattern.slice(start, current.index)]);
      return style;
    }
    function parsePluralOffset(current) {
      var pattern = current.pattern;
      var length = pattern.length;
      var offset = 0;
      if (pattern.slice(current.index, current.index + OFFSET.length) === OFFSET) {
        if (current.tokens) current.tokens.push(["offset", "offset"], ["syntax", ":"]);
        current.index += OFFSET.length;
        skipWhitespace(current);
        var start = current.index;
        while (current.index < length && isDigit(pattern.charCodeAt(current.index))) {
          ++current.index;
        }
        if (start === current.index) throw expected(current, "offset number");
        if (current.tokens) current.tokens.push(["number", pattern.slice(start, current.index)]);
        offset = +pattern.slice(start, current.index);
      }
      return offset;
    }
    function isDigit(code) {
      return code >= 48 && code <= 57;
    }
    function parseSubMessages(current, parentType) {
      var pattern = current.pattern;
      var length = pattern.length;
      var options = {};
      while (current.index < length && pattern[current.index] !== ARG_CLS) {
        var selector = parseId(current);
        if (!selector) throw expected(current, "sub-message selector");
        if (current.tokens) current.tokens.push(["selector", selector]);
        skipWhitespace(current);
        options[selector] = parseSubMessage(current, parentType);
        skipWhitespace(current);
      }
      if (!options.other && submTypes.indexOf(parentType) >= 0) {
        throw expected(current, null, null, '"other" sub-message must be specified in ' + parentType);
      }
      return options;
    }
    function parseSubMessage(current, parentType) {
      if (current.pattern[current.index] !== ARG_OPN) throw expected(current, ARG_OPN + " to start sub-message");
      if (current.tokens) current.tokens.push(["syntax", ARG_OPN]);
      ++current.index;
      var message = parseAST(current, parentType);
      if (current.pattern[current.index] !== ARG_CLS) throw expected(current, ARG_CLS + " to end sub-message");
      if (current.tokens) current.tokens.push(["syntax", ARG_CLS]);
      ++current.index;
      return message;
    }
    function expected(current, expected2, found, message) {
      var pattern = current.pattern;
      var lines = pattern.slice(0, current.index).split(/\r?\n/);
      var offset = current.index;
      var line = lines.length;
      var column = lines.slice(-1)[0].length;
      found = found || (current.index >= pattern.length ? "end of message pattern" : parseId(current) || pattern[current.index]);
      if (!message) message = errorMessage(expected2, found);
      message += " in " + pattern.replace(/\r?\n/g, "\n");
      return new SyntaxError(message, expected2, found, offset, line, column);
    }
    function errorMessage(expected2, found) {
      if (!expected2) return "Unexpected " + found + " found";
      return "Expected " + expected2 + " but found " + found;
    }
    function SyntaxError(message, expected2, found, offset, line, column) {
      Error.call(this, message);
      this.name = "SyntaxError";
      this.message = message;
      this.expected = expected2;
      this.found = found;
      this.offset = offset;
      this.line = line;
      this.column = column;
    }
    SyntaxError.prototype = Object.create(Error.prototype);
    exports2.SyntaxError = SyntaxError;
  }
});

// node_modules/format-message-formats/index.js
var require_format_message_formats = __commonJS({
  "node_modules/format-message-formats/index.js"(exports2, module2) {
    var LONG = "long";
    var SHORT = "short";
    var NARROW = "narrow";
    var NUMERIC = "numeric";
    var TWODIGIT = "2-digit";
    module2.exports = {
      number: {
        decimal: {
          style: "decimal"
        },
        integer: {
          style: "decimal",
          maximumFractionDigits: 0
        },
        currency: {
          style: "currency",
          currency: "USD"
        },
        percent: {
          style: "percent"
        },
        default: {
          style: "decimal"
        }
      },
      date: {
        short: {
          month: NUMERIC,
          day: NUMERIC,
          year: TWODIGIT
        },
        medium: {
          month: SHORT,
          day: NUMERIC,
          year: NUMERIC
        },
        long: {
          month: LONG,
          day: NUMERIC,
          year: NUMERIC
        },
        full: {
          month: LONG,
          day: NUMERIC,
          year: NUMERIC,
          weekday: LONG
        },
        default: {
          month: SHORT,
          day: NUMERIC,
          year: NUMERIC
        }
      },
      time: {
        short: {
          hour: NUMERIC,
          minute: NUMERIC
        },
        medium: {
          hour: NUMERIC,
          minute: NUMERIC,
          second: NUMERIC
        },
        long: {
          hour: NUMERIC,
          minute: NUMERIC,
          second: NUMERIC,
          timeZoneName: SHORT
        },
        full: {
          hour: NUMERIC,
          minute: NUMERIC,
          second: NUMERIC,
          timeZoneName: SHORT
        },
        default: {
          hour: NUMERIC,
          minute: NUMERIC,
          second: NUMERIC
        }
      },
      duration: {
        default: {
          hours: {
            minimumIntegerDigits: 1,
            maximumFractionDigits: 0
          },
          minutes: {
            minimumIntegerDigits: 2,
            maximumFractionDigits: 0
          },
          seconds: {
            minimumIntegerDigits: 2,
            maximumFractionDigits: 3
          }
        }
      },
      parseNumberPattern: function(pattern) {
        if (!pattern) return;
        var options = {};
        var currency = pattern.match(/\b[A-Z]{3}\b/i);
        var syms = pattern.replace(/[^¤]/g, "").length;
        if (!syms && currency) syms = 1;
        if (syms) {
          options.style = "currency";
          options.currencyDisplay = syms === 1 ? "symbol" : syms === 2 ? "code" : "name";
          options.currency = currency ? currency[0].toUpperCase() : "USD";
        } else if (pattern.indexOf("%") >= 0) {
          options.style = "percent";
        }
        if (!/[@#0]/.test(pattern)) return options.style ? options : void 0;
        options.useGrouping = pattern.indexOf(",") >= 0;
        if (/E\+?[@#0]+/i.test(pattern) || pattern.indexOf("@") >= 0) {
          var size = pattern.replace(/E\+?[@#0]+|[^@#0]/gi, "");
          options.minimumSignificantDigits = Math.min(Math.max(size.replace(/[^@0]/g, "").length, 1), 21);
          options.maximumSignificantDigits = Math.min(Math.max(size.length, 1), 21);
        } else {
          var parts = pattern.replace(/[^#0.]/g, "").split(".");
          var integer = parts[0];
          var n = integer.length - 1;
          while (integer[n] === "0") --n;
          options.minimumIntegerDigits = Math.min(Math.max(integer.length - 1 - n, 1), 21);
          var fraction = parts[1] || "";
          n = 0;
          while (fraction[n] === "0") ++n;
          options.minimumFractionDigits = Math.min(Math.max(n, 0), 20);
          while (fraction[n] === "#") ++n;
          options.maximumFractionDigits = Math.min(Math.max(n, 0), 20);
        }
        return options;
      },
      parseDatePattern: function(pattern) {
        if (!pattern) return;
        var options = {};
        for (var i = 0; i < pattern.length; ) {
          var current = pattern[i];
          var n = 1;
          while (pattern[++i] === current) ++n;
          switch (current) {
            case "G":
              options.era = n === 5 ? NARROW : n === 4 ? LONG : SHORT;
              break;
            case "y":
            case "Y":
              options.year = n === 2 ? TWODIGIT : NUMERIC;
              break;
            case "M":
            case "L":
              n = Math.min(Math.max(n - 1, 0), 4);
              options.month = [NUMERIC, TWODIGIT, SHORT, LONG, NARROW][n];
              break;
            case "E":
            case "e":
            case "c":
              options.weekday = n === 5 ? NARROW : n === 4 ? LONG : SHORT;
              break;
            case "d":
            case "D":
              options.day = n === 2 ? TWODIGIT : NUMERIC;
              break;
            case "h":
            case "K":
              options.hour12 = true;
              options.hour = n === 2 ? TWODIGIT : NUMERIC;
              break;
            case "H":
            case "k":
              options.hour12 = false;
              options.hour = n === 2 ? TWODIGIT : NUMERIC;
              break;
            case "m":
              options.minute = n === 2 ? TWODIGIT : NUMERIC;
              break;
            case "s":
            case "S":
              options.second = n === 2 ? TWODIGIT : NUMERIC;
              break;
            case "z":
            case "Z":
            case "v":
            case "V":
              options.timeZoneName = n === 1 ? SHORT : LONG;
              break;
          }
        }
        return Object.keys(options).length ? options : void 0;
      }
    };
  }
});

// node_modules/lookup-closest-locale/index.js
var require_lookup_closest_locale = __commonJS({
  "node_modules/lookup-closest-locale/index.js"(exports2, module2) {
    module2.exports = function lookupClosestLocale2(locale, available) {
      if (typeof locale === "string" && available[locale]) return locale;
      var locales = [].concat(locale || []);
      for (var l = 0, ll = locales.length; l < ll; ++l) {
        var current = locales[l].split("-");
        while (current.length) {
          var candidate = current.join("-");
          if (available[candidate]) return candidate;
          current.pop();
        }
      }
    };
  }
});

// node_modules/format-message-interpret/plurals.js
var require_plurals = __commonJS({
  "node_modules/format-message-interpret/plurals.js"(exports2, module2) {
    "use strict";
    var zero = "zero";
    var one = "one";
    var two = "two";
    var few = "few";
    var many = "many";
    var other = "other";
    var f = [
      function(s) {
        var n = +s;
        return n === 1 ? one : other;
      },
      function(s) {
        var n = +s;
        return 0 <= n && n <= 1 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var n = +s;
        return i === 0 || n === 1 ? one : other;
      },
      function(s) {
        var n = +s;
        return n === 0 ? zero : n === 1 ? one : n === 2 ? two : 3 <= n % 100 && n % 100 <= 10 ? few : 11 <= n % 100 && n % 100 <= 99 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        return i === 1 && v === 0 ? one : other;
      },
      function(s) {
        var n = +s;
        return n % 10 === 1 && n % 100 !== 11 ? one : 2 <= n % 10 && n % 10 <= 4 && (n % 100 < 12 || 14 < n % 100) ? few : n % 10 === 0 || 5 <= n % 10 && n % 10 <= 9 || 11 <= n % 100 && n % 100 <= 14 ? many : other;
      },
      function(s) {
        var n = +s;
        return n % 10 === 1 && (n % 100 !== 11 && n % 100 !== 71 && n % 100 !== 91) ? one : n % 10 === 2 && (n % 100 !== 12 && n % 100 !== 72 && n % 100 !== 92) ? two : (3 <= n % 10 && n % 10 <= 4 || n % 10 === 9) && ((n % 100 < 10 || 19 < n % 100) && (n % 100 < 70 || 79 < n % 100) && (n % 100 < 90 || 99 < n % 100)) ? few : n !== 0 && n % 1e6 === 0 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        var f2 = +(s + ".").split(".")[1];
        return v === 0 && i % 10 === 1 && i % 100 !== 11 || f2 % 10 === 1 && f2 % 100 !== 11 ? one : v === 0 && (2 <= i % 10 && i % 10 <= 4) && (i % 100 < 12 || 14 < i % 100) || 2 <= f2 % 10 && f2 % 10 <= 4 && (f2 % 100 < 12 || 14 < f2 % 100) ? few : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        return i === 1 && v === 0 ? one : 2 <= i && i <= 4 && v === 0 ? few : v !== 0 ? many : other;
      },
      function(s) {
        var n = +s;
        return n === 0 ? zero : n === 1 ? one : n === 2 ? two : n === 3 ? few : n === 6 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var t = +("" + s).replace(/^[^.]*.?|0+$/g, "");
        var n = +s;
        return n === 1 || t !== 0 && (i === 0 || i === 1) ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        var f2 = +(s + ".").split(".")[1];
        return v === 0 && i % 100 === 1 || f2 % 100 === 1 ? one : v === 0 && i % 100 === 2 || f2 % 100 === 2 ? two : v === 0 && (3 <= i % 100 && i % 100 <= 4) || 3 <= f2 % 100 && f2 % 100 <= 4 ? few : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        return i === 0 || i === 1 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        var f2 = +(s + ".").split(".")[1];
        return v === 0 && (i === 1 || i === 2 || i === 3) || v === 0 && (i % 10 !== 4 && i % 10 !== 6 && i % 10 !== 9) || v !== 0 && (f2 % 10 !== 4 && f2 % 10 !== 6 && f2 % 10 !== 9) ? one : other;
      },
      function(s) {
        var n = +s;
        return n === 1 ? one : n === 2 ? two : 3 <= n && n <= 6 ? few : 7 <= n && n <= 10 ? many : other;
      },
      function(s) {
        var n = +s;
        return n === 1 || n === 11 ? one : n === 2 || n === 12 ? two : 3 <= n && n <= 10 || 13 <= n && n <= 19 ? few : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        return v === 0 && i % 10 === 1 ? one : v === 0 && i % 10 === 2 ? two : v === 0 && (i % 100 === 0 || i % 100 === 20 || i % 100 === 40 || i % 100 === 60 || i % 100 === 80) ? few : v !== 0 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        var n = +s;
        return i === 1 && v === 0 ? one : i === 2 && v === 0 ? two : v === 0 && (n < 0 || 10 < n) && n % 10 === 0 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var t = +("" + s).replace(/^[^.]*.?|0+$/g, "");
        return t === 0 && i % 10 === 1 && i % 100 !== 11 || t !== 0 ? one : other;
      },
      function(s) {
        var n = +s;
        return n === 1 ? one : n === 2 ? two : other;
      },
      function(s) {
        var n = +s;
        return n === 0 ? zero : n === 1 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var n = +s;
        return n === 0 ? zero : (i === 0 || i === 1) && n !== 0 ? one : other;
      },
      function(s) {
        var f2 = +(s + ".").split(".")[1];
        var n = +s;
        return n % 10 === 1 && (n % 100 < 11 || 19 < n % 100) ? one : 2 <= n % 10 && n % 10 <= 9 && (n % 100 < 11 || 19 < n % 100) ? few : f2 !== 0 ? many : other;
      },
      function(s) {
        var v = (s + ".").split(".")[1].length;
        var f2 = +(s + ".").split(".")[1];
        var n = +s;
        return n % 10 === 0 || 11 <= n % 100 && n % 100 <= 19 || v === 2 && (11 <= f2 % 100 && f2 % 100 <= 19) ? zero : n % 10 === 1 && n % 100 !== 11 || v === 2 && f2 % 10 === 1 && f2 % 100 !== 11 || v !== 2 && f2 % 10 === 1 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        var f2 = +(s + ".").split(".")[1];
        return v === 0 && i % 10 === 1 && i % 100 !== 11 || f2 % 10 === 1 && f2 % 100 !== 11 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        var n = +s;
        return i === 1 && v === 0 ? one : v !== 0 || n === 0 || n !== 1 && (1 <= n % 100 && n % 100 <= 19) ? few : other;
      },
      function(s) {
        var n = +s;
        return n === 1 ? one : n === 0 || 2 <= n % 100 && n % 100 <= 10 ? few : 11 <= n % 100 && n % 100 <= 19 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        return i === 1 && v === 0 ? one : v === 0 && (2 <= i % 10 && i % 10 <= 4) && (i % 100 < 12 || 14 < i % 100) ? few : v === 0 && i !== 1 && (0 <= i % 10 && i % 10 <= 1) || v === 0 && (5 <= i % 10 && i % 10 <= 9) || v === 0 && (12 <= i % 100 && i % 100 <= 14) ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        return 0 <= i && i <= 1 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        return v === 0 && i % 10 === 1 && i % 100 !== 11 ? one : v === 0 && (2 <= i % 10 && i % 10 <= 4) && (i % 100 < 12 || 14 < i % 100) ? few : v === 0 && i % 10 === 0 || v === 0 && (5 <= i % 10 && i % 10 <= 9) || v === 0 && (11 <= i % 100 && i % 100 <= 14) ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var n = +s;
        return i === 0 || n === 1 ? one : 2 <= n && n <= 10 ? few : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var f2 = +(s + ".").split(".")[1];
        var n = +s;
        return n === 0 || n === 1 || i === 0 && f2 === 1 ? one : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        var v = (s + ".").split(".")[1].length;
        return v === 0 && i % 100 === 1 ? one : v === 0 && i % 100 === 2 ? two : v === 0 && (3 <= i % 100 && i % 100 <= 4) || v !== 0 ? few : other;
      },
      function(s) {
        var n = +s;
        return 0 <= n && n <= 1 || 11 <= n && n <= 99 ? one : other;
      },
      function(s) {
        var n = +s;
        return n === 1 || n === 5 || n === 7 || n === 8 || n === 9 || n === 10 ? one : n === 2 || n === 3 ? two : n === 4 ? few : n === 6 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        return i % 10 === 1 || i % 10 === 2 || i % 10 === 5 || i % 10 === 7 || i % 10 === 8 || (i % 100 === 20 || i % 100 === 50 || i % 100 === 70 || i % 100 === 80) ? one : i % 10 === 3 || i % 10 === 4 || (i % 1e3 === 100 || i % 1e3 === 200 || i % 1e3 === 300 || i % 1e3 === 400 || i % 1e3 === 500 || i % 1e3 === 600 || i % 1e3 === 700 || i % 1e3 === 800 || i % 1e3 === 900) ? few : i === 0 || i % 10 === 6 || (i % 100 === 40 || i % 100 === 60 || i % 100 === 90) ? many : other;
      },
      function(s) {
        var n = +s;
        return (n % 10 === 2 || n % 10 === 3) && (n % 100 !== 12 && n % 100 !== 13) ? few : other;
      },
      function(s) {
        var n = +s;
        return n === 1 || n === 3 ? one : n === 2 ? two : n === 4 ? few : other;
      },
      function(s) {
        var n = +s;
        return n === 0 || n === 7 || n === 8 || n === 9 ? zero : n === 1 ? one : n === 2 ? two : n === 3 || n === 4 ? few : n === 5 || n === 6 ? many : other;
      },
      function(s) {
        var n = +s;
        return n % 10 === 1 && n % 100 !== 11 ? one : n % 10 === 2 && n % 100 !== 12 ? two : n % 10 === 3 && n % 100 !== 13 ? few : other;
      },
      function(s) {
        var n = +s;
        return n === 1 || n === 11 ? one : n === 2 || n === 12 ? two : n === 3 || n === 13 ? few : other;
      },
      function(s) {
        var n = +s;
        return n === 1 ? one : n === 2 || n === 3 ? two : n === 4 ? few : n === 6 ? many : other;
      },
      function(s) {
        var n = +s;
        return n === 1 || n === 5 ? one : other;
      },
      function(s) {
        var n = +s;
        return n === 11 || n === 8 || n === 80 || n === 800 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        return i === 1 ? one : i === 0 || (2 <= i % 100 && i % 100 <= 20 || i % 100 === 40 || i % 100 === 60 || i % 100 === 80) ? many : other;
      },
      function(s) {
        var n = +s;
        return n % 10 === 6 || n % 10 === 9 || n % 10 === 0 && n !== 0 ? many : other;
      },
      function(s) {
        var i = Math.floor(Math.abs(+s));
        return i % 10 === 1 && i % 100 !== 11 ? one : i % 10 === 2 && i % 100 !== 12 ? two : (i % 10 === 7 || i % 10 === 8) && (i % 100 !== 17 && i % 100 !== 18) ? many : other;
      },
      function(s) {
        var n = +s;
        return n === 1 ? one : n === 2 || n === 3 ? two : n === 4 ? few : other;
      },
      function(s) {
        var n = +s;
        return 1 <= n && n <= 4 ? one : other;
      },
      function(s) {
        var n = +s;
        return n === 1 || n === 5 || 7 <= n && n <= 9 ? one : n === 2 || n === 3 ? two : n === 4 ? few : n === 6 ? many : other;
      },
      function(s) {
        var n = +s;
        return n === 1 ? one : n % 10 === 4 && n % 100 !== 14 ? many : other;
      },
      function(s) {
        var n = +s;
        return (n % 10 === 1 || n % 10 === 2) && (n % 100 !== 11 && n % 100 !== 12) ? one : other;
      },
      function(s) {
        var n = +s;
        return n % 10 === 6 || n % 10 === 9 || n === 10 ? few : other;
      },
      function(s) {
        var n = +s;
        return n % 10 === 3 && n % 100 !== 13 ? few : other;
      }
    ];
    module2.exports = {
      af: { cardinal: f[0] },
      ak: { cardinal: f[1] },
      am: { cardinal: f[2] },
      ar: { cardinal: f[3] },
      ars: { cardinal: f[3] },
      as: { cardinal: f[2], ordinal: f[34] },
      asa: { cardinal: f[0] },
      ast: { cardinal: f[4] },
      az: { cardinal: f[0], ordinal: f[35] },
      be: { cardinal: f[5], ordinal: f[36] },
      bem: { cardinal: f[0] },
      bez: { cardinal: f[0] },
      bg: { cardinal: f[0] },
      bh: { cardinal: f[1] },
      bn: { cardinal: f[2], ordinal: f[34] },
      br: { cardinal: f[6] },
      brx: { cardinal: f[0] },
      bs: { cardinal: f[7] },
      ca: { cardinal: f[4], ordinal: f[37] },
      ce: { cardinal: f[0] },
      cgg: { cardinal: f[0] },
      chr: { cardinal: f[0] },
      ckb: { cardinal: f[0] },
      cs: { cardinal: f[8] },
      cy: { cardinal: f[9], ordinal: f[38] },
      da: { cardinal: f[10] },
      de: { cardinal: f[4] },
      dsb: { cardinal: f[11] },
      dv: { cardinal: f[0] },
      ee: { cardinal: f[0] },
      el: { cardinal: f[0] },
      en: { cardinal: f[4], ordinal: f[39] },
      eo: { cardinal: f[0] },
      es: { cardinal: f[0] },
      et: { cardinal: f[4] },
      eu: { cardinal: f[0] },
      fa: { cardinal: f[2] },
      ff: { cardinal: f[12] },
      fi: { cardinal: f[4] },
      fil: { cardinal: f[13], ordinal: f[0] },
      fo: { cardinal: f[0] },
      fr: { cardinal: f[12], ordinal: f[0] },
      fur: { cardinal: f[0] },
      fy: { cardinal: f[4] },
      ga: { cardinal: f[14], ordinal: f[0] },
      gd: { cardinal: f[15], ordinal: f[40] },
      gl: { cardinal: f[4] },
      gsw: { cardinal: f[0] },
      gu: { cardinal: f[2], ordinal: f[41] },
      guw: { cardinal: f[1] },
      gv: { cardinal: f[16] },
      ha: { cardinal: f[0] },
      haw: { cardinal: f[0] },
      he: { cardinal: f[17] },
      hi: { cardinal: f[2], ordinal: f[41] },
      hr: { cardinal: f[7] },
      hsb: { cardinal: f[11] },
      hu: { cardinal: f[0], ordinal: f[42] },
      hy: { cardinal: f[12], ordinal: f[0] },
      ia: { cardinal: f[4] },
      io: { cardinal: f[4] },
      is: { cardinal: f[18] },
      it: { cardinal: f[4], ordinal: f[43] },
      iu: { cardinal: f[19] },
      iw: { cardinal: f[17] },
      jgo: { cardinal: f[0] },
      ji: { cardinal: f[4] },
      jmc: { cardinal: f[0] },
      ka: { cardinal: f[0], ordinal: f[44] },
      kab: { cardinal: f[12] },
      kaj: { cardinal: f[0] },
      kcg: { cardinal: f[0] },
      kk: { cardinal: f[0], ordinal: f[45] },
      kkj: { cardinal: f[0] },
      kl: { cardinal: f[0] },
      kn: { cardinal: f[2] },
      ks: { cardinal: f[0] },
      ksb: { cardinal: f[0] },
      ksh: { cardinal: f[20] },
      ku: { cardinal: f[0] },
      kw: { cardinal: f[19] },
      ky: { cardinal: f[0] },
      lag: { cardinal: f[21] },
      lb: { cardinal: f[0] },
      lg: { cardinal: f[0] },
      ln: { cardinal: f[1] },
      lt: { cardinal: f[22] },
      lv: { cardinal: f[23] },
      mas: { cardinal: f[0] },
      mg: { cardinal: f[1] },
      mgo: { cardinal: f[0] },
      mk: { cardinal: f[24], ordinal: f[46] },
      ml: { cardinal: f[0] },
      mn: { cardinal: f[0] },
      mo: { cardinal: f[25], ordinal: f[0] },
      mr: { cardinal: f[2], ordinal: f[47] },
      mt: { cardinal: f[26] },
      nah: { cardinal: f[0] },
      naq: { cardinal: f[19] },
      nb: { cardinal: f[0] },
      nd: { cardinal: f[0] },
      ne: { cardinal: f[0], ordinal: f[48] },
      nl: { cardinal: f[4] },
      nn: { cardinal: f[0] },
      nnh: { cardinal: f[0] },
      no: { cardinal: f[0] },
      nr: { cardinal: f[0] },
      nso: { cardinal: f[1] },
      ny: { cardinal: f[0] },
      nyn: { cardinal: f[0] },
      om: { cardinal: f[0] },
      or: { cardinal: f[0], ordinal: f[49] },
      os: { cardinal: f[0] },
      pa: { cardinal: f[1] },
      pap: { cardinal: f[0] },
      pl: { cardinal: f[27] },
      prg: { cardinal: f[23] },
      ps: { cardinal: f[0] },
      pt: { cardinal: f[28] },
      "pt-PT": { cardinal: f[4] },
      rm: { cardinal: f[0] },
      ro: { cardinal: f[25], ordinal: f[0] },
      rof: { cardinal: f[0] },
      ru: { cardinal: f[29] },
      rwk: { cardinal: f[0] },
      saq: { cardinal: f[0] },
      sc: { cardinal: f[4], ordinal: f[43] },
      scn: { cardinal: f[4], ordinal: f[43] },
      sd: { cardinal: f[0] },
      sdh: { cardinal: f[0] },
      se: { cardinal: f[19] },
      seh: { cardinal: f[0] },
      sh: { cardinal: f[7] },
      shi: { cardinal: f[30] },
      si: { cardinal: f[31] },
      sk: { cardinal: f[8] },
      sl: { cardinal: f[32] },
      sma: { cardinal: f[19] },
      smi: { cardinal: f[19] },
      smj: { cardinal: f[19] },
      smn: { cardinal: f[19] },
      sms: { cardinal: f[19] },
      sn: { cardinal: f[0] },
      so: { cardinal: f[0] },
      sq: { cardinal: f[0], ordinal: f[50] },
      sr: { cardinal: f[7] },
      ss: { cardinal: f[0] },
      ssy: { cardinal: f[0] },
      st: { cardinal: f[0] },
      sv: { cardinal: f[4], ordinal: f[51] },
      sw: { cardinal: f[4] },
      syr: { cardinal: f[0] },
      ta: { cardinal: f[0] },
      te: { cardinal: f[0] },
      teo: { cardinal: f[0] },
      ti: { cardinal: f[1] },
      tig: { cardinal: f[0] },
      tk: { cardinal: f[0], ordinal: f[52] },
      tl: { cardinal: f[13], ordinal: f[0] },
      tn: { cardinal: f[0] },
      tr: { cardinal: f[0] },
      ts: { cardinal: f[0] },
      tzm: { cardinal: f[33] },
      ug: { cardinal: f[0] },
      uk: { cardinal: f[29], ordinal: f[53] },
      ur: { cardinal: f[4] },
      uz: { cardinal: f[0] },
      ve: { cardinal: f[0] },
      vo: { cardinal: f[0] },
      vun: { cardinal: f[0] },
      wa: { cardinal: f[1] },
      wae: { cardinal: f[0] },
      xh: { cardinal: f[0] },
      xog: { cardinal: f[0] },
      yi: { cardinal: f[4] },
      zu: { cardinal: f[2] },
      lo: { ordinal: f[0] },
      ms: { ordinal: f[0] },
      vi: { ordinal: f[0] }
    };
  }
});

// node_modules/format-message-interpret/index.js
var require_format_message_interpret = __commonJS({
  "node_modules/format-message-interpret/index.js"(exports2, module2) {
    "use strict";
    var formats = require_format_message_formats();
    var lookupClosestLocale2 = require_lookup_closest_locale();
    var plurals2 = require_plurals();
    exports2 = module2.exports = function interpret2(ast, locale, types) {
      return interpretAST(ast, null, locale || "en", types || {}, true);
    };
    exports2.toParts = function toParts(ast, locale, types) {
      return interpretAST(ast, null, locale || "en", types || {}, false);
    };
    function interpretAST(elements, parent, locale, types, join) {
      var parts = elements.map(function(element) {
        return interpretElement(element, parent, locale, types, join);
      });
      if (!join) {
        return function format(args) {
          return parts.reduce(function(parts2, part) {
            return parts2.concat(part(args));
          }, []);
        };
      }
      if (parts.length === 1) return parts[0];
      return function format(args) {
        var message = "";
        for (var e = 0; e < parts.length; ++e) {
          message += parts[e](args);
        }
        return message;
      };
    }
    function interpretElement(element, parent, locale, types, join) {
      if (typeof element === "string") {
        var value = element;
        return function format() {
          return value;
        };
      }
      var id = element[0];
      var type = element[1];
      if (parent && element[0] === "#") {
        id = parent[0];
        var offset = parent[2];
        var formatter = (types.number || defaults.number)([id, "number"], locale);
        return function format(args) {
          return formatter(getArg(id, args) - offset, args);
        };
      }
      var children;
      if (type === "plural" || type === "selectordinal") {
        children = {};
        Object.keys(element[3]).forEach(function(key) {
          children[key] = interpretAST(element[3][key], element, locale, types, join);
        });
        element = [element[0], element[1], element[2], children];
      } else if (element[2] && typeof element[2] === "object") {
        children = {};
        Object.keys(element[2]).forEach(function(key) {
          children[key] = interpretAST(element[2][key], element, locale, types, join);
        });
        element = [element[0], element[1], children];
      }
      var getFrmt = type && (types[type] || defaults[type]);
      if (getFrmt) {
        var frmt = getFrmt(element, locale);
        return function format(args) {
          return frmt(getArg(id, args), args);
        };
      }
      return join ? function format(args) {
        return String(getArg(id, args));
      } : function format(args) {
        return getArg(id, args);
      };
    }
    function getArg(id, args) {
      if (args && id in args) return args[id];
      var parts = id.split(".");
      var a = args;
      for (var i = 0, ii = parts.length; a && i < ii; ++i) {
        a = a[parts[i]];
      }
      return a;
    }
    function interpretNumber(element, locales) {
      var style = element[2];
      var options = formats.number[style] || formats.parseNumberPattern(style) || formats.number.default;
      return new Intl.NumberFormat(locales, options).format;
    }
    function interpretDuration(element, locales) {
      var style = element[2];
      var options = formats.duration[style] || formats.duration.default;
      var fs = new Intl.NumberFormat(locales, options.seconds).format;
      var fm = new Intl.NumberFormat(locales, options.minutes).format;
      var fh = new Intl.NumberFormat(locales, options.hours).format;
      var sep = /^fi$|^fi-|^da/.test(String(locales)) ? "." : ":";
      return function(s, args) {
        s = +s;
        if (!isFinite(s)) return fs(s);
        var h = ~~(s / 60 / 60);
        var m = ~~(s / 60 % 60);
        var dur = (h ? fh(Math.abs(h)) + sep : "") + fm(Math.abs(m)) + sep + fs(Math.abs(s % 60));
        return s < 0 ? fh(-1).replace(fh(1), dur) : dur;
      };
    }
    function interpretDateTime(element, locales) {
      var type = element[1];
      var style = element[2];
      var options = formats[type][style] || formats.parseDatePattern(style) || formats[type].default;
      return new Intl.DateTimeFormat(locales, options).format;
    }
    function interpretPlural(element, locales) {
      var type = element[1];
      var pluralType = type === "selectordinal" ? "ordinal" : "cardinal";
      var offset = element[2];
      var children = element[3];
      var pluralRules;
      if (Intl.PluralRules && Intl.PluralRules.supportedLocalesOf(locales).length > 0) {
        pluralRules = new Intl.PluralRules(locales, { type: pluralType });
      } else {
        var locale = lookupClosestLocale2(locales, plurals2);
        var select = locale && plurals2[locale][pluralType] || returnOther;
        pluralRules = { select };
      }
      return function(value, args) {
        var clause = children["=" + +value] || children[pluralRules.select(value - offset)] || children.other;
        return clause(args);
      };
    }
    function returnOther() {
      return "other";
    }
    function interpretSelect(element, locales) {
      var children = element[2];
      return function(value, args) {
        var clause = children[value] || children.other;
        return clause(args);
      };
    }
    var defaults = {
      number: interpretNumber,
      ordinal: interpretNumber,
      // TODO: support rbnf
      spellout: interpretNumber,
      // TODO: support rbnf
      duration: interpretDuration,
      date: interpretDateTime,
      time: interpretDateTime,
      plural: interpretPlural,
      selectordinal: interpretPlural,
      select: interpretSelect
    };
    exports2.types = defaults;
  }
});

// node_modules/format-message/index.js
var parse = require_format_message_parse();
var interpret = require_format_message_interpret();
var plurals = require_plurals();
var lookupClosestLocale = require_lookup_closest_locale();
var origFormats = require_format_message_formats();
function assign(target, source) {
  Object.keys(source).forEach(function(key) {
    target[key] = source[key];
  });
  return target;
}
function namespace() {
  var formats = assign({}, origFormats);
  var currentLocales = "en";
  var translations = {};
  var generateId = function(pattern) {
    return pattern;
  };
  var missingReplacement = null;
  var missingTranslation = "warning";
  var types = {};
  function formatMessage(msg, args, locales) {
    var pattern = typeof msg === "string" ? msg : msg.default;
    var id = typeof msg === "object" && msg.id || generateId(pattern);
    var translated = translate(pattern, id, locales || currentLocales);
    var format = translated.format || (translated.format = interpret(parse(translated.message), locales || currentLocales, types));
    return format(args);
  }
  formatMessage.rich = function rich(msg, args, locales) {
    var pattern = typeof msg === "string" ? msg : msg.default;
    var id = typeof msg === "object" && msg.id || generateId(pattern);
    var translated = translate(pattern, id, locales || currentLocales);
    var format = translated.toParts || (translated.toParts = interpret.toParts(parse(translated.message, { tagsType }), locales || currentLocales, types));
    return format(args);
  };
  var tagsType = "<>";
  function richType(node, locales) {
    var style = node[2];
    return function(fn, args) {
      var props = typeof style === "object" ? mapObject(style, args) : style;
      return typeof fn === "function" ? fn(props) : fn;
    };
  }
  types[tagsType] = richType;
  function mapObject(object, args) {
    return Object.keys(object).reduce(function(mapped, key) {
      mapped[key] = object[key](args);
      return mapped;
    }, {});
  }
  function translate(pattern, id, locales) {
    var locale = lookupClosestLocale(locales, translations) || "en";
    var messages = translations[locale] || (translations[locale] = {});
    var translated = messages[id];
    if (typeof translated === "string") {
      translated = messages[id] = { message: translated };
    }
    if (!translated) {
      var message = 'Translation for "' + id + '" in "' + locale + '" is missing';
      if (missingTranslation === "warning") {
        if (typeof console !== "undefined") console.warn(message);
      } else if (missingTranslation !== "ignore") {
        throw new Error(message);
      }
      var replacement = typeof missingReplacement === "function" ? missingReplacement(pattern, id, locale) || pattern : missingReplacement || pattern;
      translated = messages[id] = { message: replacement };
    }
    return translated;
  }
  formatMessage.setup = function setup(opt) {
    opt = opt || {};
    if (opt.locale) currentLocales = opt.locale;
    if ("translations" in opt) translations = opt.translations || {};
    if (opt.generateId) generateId = opt.generateId;
    if ("missingReplacement" in opt) missingReplacement = opt.missingReplacement;
    if (opt.missingTranslation) missingTranslation = opt.missingTranslation;
    if (opt.formats) {
      if (opt.formats.number) assign(formats.number, opt.formats.number);
      if (opt.formats.date) assign(formats.date, opt.formats.date);
      if (opt.formats.time) assign(formats.time, opt.formats.time);
    }
    if (opt.types) {
      types = opt.types;
      types[tagsType] = richType;
    }
    return {
      locale: currentLocales,
      translations,
      generateId,
      missingReplacement,
      missingTranslation,
      formats,
      types
    };
  };
  formatMessage.number = function(value, style, locales) {
    var options = style && formats.number[style] || formats.parseNumberPattern(style) || formats.number.default;
    return new Intl.NumberFormat(locales || currentLocales, options).format(value);
  };
  formatMessage.date = function(value, style, locales) {
    var options = style && formats.date[style] || formats.parseDatePattern(style) || formats.date.default;
    return new Intl.DateTimeFormat(locales || currentLocales, options).format(value);
  };
  formatMessage.time = function(value, style, locales) {
    var options = style && formats.time[style] || formats.parseDatePattern(style) || formats.time.default;
    return new Intl.DateTimeFormat(locales || currentLocales, options).format(value);
  };
  formatMessage.select = function(value, options) {
    return options[value] || options.other;
  };
  formatMessage.custom = function(placeholder, locales, value, args) {
    if (!(placeholder[1] in types)) return value;
    return types[placeholder[1]](placeholder, locales)(value, args);
  };
  formatMessage.plural = plural.bind(null, "cardinal");
  formatMessage.selectordinal = plural.bind(null, "ordinal");
  function plural(pluralType, value, offset, options, locale) {
    if (typeof offset === "object" && typeof options !== "object") {
      locale = options;
      options = offset;
      offset = 0;
    }
    var closest = lookupClosestLocale(locale || currentLocales, plurals);
    var plural2 = closest && plurals[closest][pluralType] || returnOther;
    return options["=" + +value] || options[plural2(value - offset)] || options.other;
  }
  function returnOther() {
    return "other";
  }
  formatMessage.namespace = namespace;
  return formatMessage;
}
module.exports = exports = namespace();
