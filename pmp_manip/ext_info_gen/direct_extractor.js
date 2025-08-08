const fs = require("fs");
const path = require("path");

// ---- Scratch stub ----

function createTranslate() {
    const translateFn = function (message, args) {
        if (message && typeof message === "object") {
            // already in expected format
        } else if (typeof message === "string") {
            message = { default: message };
        } else {
            throw new Error("unsupported data type in translate()");
        }
        return message.default || "";
    };

    translateFn.setup = (newTranslations => {});

    Object.defineProperty(translateFn, "language", {
        configurable: true,
        enumerable: true,
        get: (() => "en")
    });

    translateFn.setup({});

    return translateFn;
}

register = (ext) => {
    const dangerousMethods = ["init"];

    // Patch the prototype directly
    const proto = Object.getPrototypeOf(ext);
    for (const method of dangerousMethods) {
        if (typeof proto[method] === "function") {
            console.warn(`Patching prototype method '${method}'`);
            proto[method] = () => {};
        }
    }

    globalThis._scratchExtension = ext;
};

globalThis.Scratch = { // Must be kept in sync with safe_extractor.py
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
        "register": register,
        "isPenguinMod": true
    },
    translate: createTranslate(null),

    vm: {
        runtime: {
            registerCompiledExtensionBlocks: (extensionId, compileInfo) => {
                // do nothing since we don't care about compilation stuff
            },
            on: (eventName, func) => { // TODO: research
                // do nothing since we don't care about what happens after loading the extension
            },
        }
    }
    // I only included the properties which a resonable getInfo should use
}

// ---- Main loader ----
function runScript(code) {
    try {
        const module = { exports: {} };
        const requireFunc = require;
        eval(code); // evaluated in current global context
        if (!globalThis._scratchExtension) {
            console.error("Extension was not registered.");
            process.exit(1); // Errno. 1
        }
        const extensionInfo = globalThis._scratchExtension.getInfo();
        console.log(JSON.stringify(extensionInfo)); // must be the last call to console.log() or similar
    } catch (e) {
        console.error("Error executing script:", e);
        process.exit(2); // Errno. 2
    }
}

const filePath = process.argv[2];
const fullPath = path.resolve(filePath);
const code = fs.readFileSync(fullPath, "utf-8");
runScript(code);
process.exit(0);
