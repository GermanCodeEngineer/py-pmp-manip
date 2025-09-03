const fs = require("fs");
const path = require("path");
const vm = require("vm");


// ---------- Step 1: whitelist-only register (only keep getInfo) ----------

function makeStubWithArity(arity) {
const params = Array.from({ length: arity }, (_, i) => `a${i}`);
// eslint-disable-next-line no-new-func
return Function(...params, 'return {};');
}

const BLACKLIST = new Set(["init", "initialize"]);

function register(ext) {
    // Patch the prototype directly
    const proto = Object.getPrototypeOf(ext);
    for (const method of BLACKLIST) {
        if (typeof proto[method] === "function") {
            console.warn(`Patching prototype method '${method}'`);
            proto[method] = () => {};
        }
    }

    globalThis._scratchExtension = ext;
};

// ---------- Step 2: setup Scratch stubs (from stub.js, minimal version) ----------

const Scratch = {
    // Must be kept in sync with safe_extractor.py
    // Derived from https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/extension-support/tw-extension-api-common.js
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
    ArgumentAlignment: {
        "DEFAULT": null,
        "LEFT": "LEFT",
        "CENTER": "CENTRE",
        "RIGHT": "RIGHT"
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
    BlockShape: {
        "HEXAGONAL": 1,
        "ROUND": 2,
        "SQUARE": 3,
        "LEAF": 4,
        "PLUS": 5
    },
    NotchShape: {
        "SWITCH": "switchCase",
        "HEXAGON": "hexagon",
        "ROUND": "round",
        "SQUARE": "square",
        "LEAF": "leaf",
        "PLUS": "plus",
        "OCTAGONAL": "octagonal",
        "BUMPED": "bumped",
        "INDENTED": "indented",
        "SCRAPPED": "scrapped",
        "ARROW": "arrow",
        "TICKET": "ticket",
        "JIGSAW": "jigsaw",
        "INVERTED": "inverted",
        "PINCER": "pincer",
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
    translate: (() => {
        const translateFn = (m) => (typeof m === "string" ? m : m.default || "");
        translateFn.setup = (newTranslations) => {};
        return translateFn;
    })(),

    vm: {
        runtime: {
            registerCompiledExtensionBlocks: (extensionId, compileInfo) => {
                // do nothing since we do not care about compilation stuff
            },
            on: (eventName, func) => {
                // do nothing since we do not care about what happens after loading the extension
            },
        }
    },
    // I only included the properties which a resonable getInfo should use

    // To allow builtin PM extension to import them (they are not used in getInfo)
    Cast: class Cast {},
    Clone: class Clone {},
    Color: class Color {},
}

// ---------- Step 3: Custom require replacement ----------
const stubModules = [
    path.resolve(__dirname, '../../extension-support/argument-type'),
    path.resolve(__dirname, '../../extension-support/argument-alignment'),
    path.resolve(__dirname, '../../extension-support/block-type'),
    path.resolve(__dirname, '../../extension-support/block-shape'),
    path.resolve(__dirname, '../../extension-support/notch-shape'),
    path.resolve(__dirname, '../../extension-support/target-type'),

    path.resolve(__dirname, '../../util/cast'),
    path.resolve(__dirname, '../../util/clone'),
    path.resolve(__dirname, '../../util/color'),
];
const stubProperty = [
    "ArgumentType",
    "ArgumentAlignment",
    "BlockType",
    "BlockShape",
    "NotchShape",
    "TargetType",
    "Cast",
    "Clone",
    "Color",
];

function myRequire(moduleName) {
    const fullPath = path.resolve(__dirname, moduleName);

    // Modules you want to return null/undefined
    if (stubModules.includes(fullPath)) {
        return Scratch[stubProperty[stubModules.indexOf(fullPath)]];
    }

    // Only stub relative imports under ../../
    if (moduleName.startsWith('./') || moduleName.startsWith('../')) {
        return {};
    }

    return require(moduleName); // fallback to real require
}

// ---------- Step 4: VM execution wrapper ----------

function runScript(code, filename) {
    try {
        const sandbox = {
            ...global,
            // Important:
            module: { exports: {} },
            require: myRequire,
            Scratch: Scratch,
        };
        vm.createContext(sandbox);
        vm.runInContext(code, sandbox, { filename });

        let getInfoProvider = globalThis._scratchExtension
        if (!getInfoProvider) {
            const exported = sandbox.module.exports;
            // if a class is exported use it's getInfo
            if (typeof exported === "function" && /^class\s/.test(Function.prototype.toString.call(exported))) {
                getInfoProvider = exported.prototype
            } else {
                process.exit(1); // Errno. 1 (nothing or invalid value registered)
            }
        }

        if (!(typeof getInfoProvider.getInfo === "function")) {
            process.exit(1); // Errno. 1 (nothing or invalid value registered)
        }

        const extensionInfo = getInfoProvider.getInfo();
        console.log(JSON.stringify(extensionInfo)); // must be the last call to console.log() or similar
    } catch (error) {
        console.error("Error executing script:", error);
        process.exit(2); // Errno. 2 (execution error)
    }
}

// ---------- Entry point ----------

if (require.main === module) { // like if __name__ == "__main__"
    const filePath = process.argv[2];
    const fullPath = path.resolve(filePath);
    const code = fs.readFileSync(fullPath, "utf-8");

    runScript(code, fullPath);
    process.exit(0);
}
