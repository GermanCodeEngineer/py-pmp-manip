const fs = require("fs");
const path = require("path");
const https = require("https");
const { URL } = require("url");

// ---- Scratch stub ----

function createTranslate(vm) {
    const translateFn = function (message, args) {
        if (message && typeof message === 'object') {
            // already in expected format
        } else if (typeof message === 'string') {
            message = { default: message };
        } else {
            throw new Error("unsupported data type in translate()");
        }
        return message.default || "";
    };

    const generateId = defaultMessage => `_${defaultMessage}`;

    const getLocale = () => {
        if (vm && vm.getLocale) return vm.getLocale();
        if (typeof navigator !== 'undefined') return navigator.language;
        return 'en';
    };

    let storedTranslations = {};
    translateFn.setup = newTranslations => {
        if (newTranslations) {
            storedTranslations = newTranslations;
        }
        // simulate the behavior of format-message.namespace().setup()
    };

    Object.defineProperty(translateFn, 'language', {
        configurable: true,
        enumerable: true,
        get: () => getLocale()
    });

    translateFn.setup({});

    if (vm && vm.on) {
        vm.on("LOCALE_CHANGED", () => {
            translateFn.setup(null);
        });
    }

    return translateFn;
}

globalThis.Scratch = {
    ArgumentAlignment: {
        "DEFAULT": null,
        "LEFT": "LEFT",
        "CENTER": "CENTRE",
        "RIGHT": "RIGHT"
    },
    ArgumentType: {
        "ANGLE": "angle",
        "BOOLEAN": "Boolean",
        "COLOR": "color",
        "NUMBER": "number",
        "STRING": "string",
        "MATRIX": "matrix",
        "NOTE": "note",
        "IMAGE": "image",
        "POLYGON": "polygon",
        "COSTUME": "costume",
        "SOUND": "sound",
        "VARIABLE": "variable",
        "LIST": "list",
        "BROADCAST": "broadcast",
        "SEPERATOR": "seperator"
    },
    BlockShape: {
        "HEXAGONAL": 1,
        "ROUND": 2,
        "SQUARE": 3,
        "LEAF": 4,
        "PLUS": 5
    },
    BlockType: {
        "BOOLEAN": "Boolean",
        "BUTTON": "button",
        "LABEL": "label",
        "COMMAND": "command",
        "CONDITIONAL": "conditional",
        "EVENT": "event",
        "HAT": "hat",
        "LOOP": "loop",
        "REPORTER": "reporter",
        "XML": "xml"
    },
    TargetType: {
        "SPRITE": "sprite",
        "STAGE": "stage"
    },
    extensions: {
        "unsandboxed": true,
        "register": (ext) => {
            globalThis._scratchExtension = ext;
        },
        "isPenguinMod": true
    },
    translate: createTranslate(null),

    vm: {
        runtime: {
            registerCompiledExtensionBlocks: (extensionId, compileInfo) => {
                // do nothing since we don't care about compilation stuff
            } 
        }
    }
    // I only included the properties which a resonable getInfo should use
}

// ---- Main loader ----

const inputArg = process.argv[2];
if (!inputArg) {
    console.error("Usage: node extract-info.js <file.js | https://... | data:...>");
    process.exit(1);
}

function runScript(code) {
    try {
        const module = { exports: {} };
        const requireFunc = require;
        eval(code); // evaluated in current global context
        if (!globalThis._scratchExtension) {
            console.error("Extension was not registered.");
            process.exit(1);
        }
        const info = globalThis._scratchExtension.getInfo();
        console.log(JSON.stringify(info));
    } catch (e) {
        console.error("Error executing script:", e);
        process.exit(1);
    }
}

function loadFromURL(urlStr) {
    const parsed = new URL(urlStr);
    if (parsed.protocol === 'data:') {
        const [, base64] = urlStr.split(',');
        const buf = Buffer.from(base64, 'base64');
        runScript(buf.toString());
    } else if (parsed.protocol === 'https:') {
        https.get(urlStr, res => {
            if (res.statusCode !== 200) {
                console.error("Failed to load URL:", res.statusCode);
                res.resume();
                return;
            }
            let data = "";
            res.on("data", chunk => data += chunk);
            res.on("end", () => runScript(data));
        }).on("error", e => {
            console.error("HTTPS error:", e);
        });
    } else {
        console.error("Unsupported URL scheme:", parsed.protocol);
        process.exit(1);
    }
}

function loadFromFile(filePath) {
    const fullPath = path.resolve(filePath);
    const code = fs.readFileSync(fullPath, "utf-8");
    runScript(code);
}

// Detect and dispatch
if (inputArg.startsWith("http") || inputArg.startsWith("data:")) {
    loadFromURL(inputArg);
} else {
    loadFromFile(inputArg);
}