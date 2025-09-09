const fs = require("fs");
const path = require("path");
const vm = require("vm");


// ---------- Step 1: whitelist-only register (only keep getInfo) ----------

function makeStubWithArity(arity) {
    const params = Array.from({ length: arity }, (_, i) => `a${i}`);
    // eslint-disable-next-line no-new-func
    return Function(...params, 'return {};');
}

const BLACKLIST = new Set(["init", "initialize", "updateVideoDisplay", "_loop"]);

let scratch_ext = null;

function register(ext) {
    // Patch the prototype directly
    const proto = Object.getPrototypeOf(ext);
    throw new Error(`HEY '${typeof(ext)}' '${proto}' '${proto._loop}'`)
    for (const method of BLACKLIST) {
        if (typeof proto[method] === "function") {
            console.warn(`Patching prototype method '${method}'`);
            proto[method] = function () {};
            throw new Error(`Patching prototype method '${method}'`)
        }
    }
    scratch_ext = ext;
};

// ---------- Step 2: Setup Stubs and Proxy ----------

const ultimateStubValue = (() => {
    function target(...args) {
        return ultimateStubValue;
    }
    return new Proxy(target, {
        get(target, prop, receiver) {
        // Special cases to keep function identity intact
        if (prop === Symbol.toStringTag) return "Function";
        if (prop === "prototype") return target.prototype;
        if (prop === "constructor") return target.constructor;
        
        // For any normal property, return self again
        return receiver;
      }
    });
})();
// Chosen because all these three will work with the above value as X
// const y = new X()
// X()
// const {a, b} = X
// X.a.b ...

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

    vm: ultimateStubValue,
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

    path.resolve(__dirname, '../../extension-support/tw-l10n'),
];
const stubValue = [
    Scratch.ArgumentType,
    Scratch.ArgumentAlignment,
    Scratch.BlockType,
    Scratch.BlockShape,
    Scratch.NotchShape,
    Scratch.TargetType,
    Scratch.Cast,
    Scratch.Clone,
    Scratch.Color,

    () => Scratch.translate,
];


function myRequire(moduleName) {
    const fullPath = path.resolve(__dirname, moduleName);

    // Modules you want to return a specific stub value
    if (stubModules.includes(fullPath)) {
        return stubValue[stubModules.indexOf(fullPath)];
    }
    
    // Only stub relative imports under ../../ or from external organizations
    if (moduleName.startsWith('./') || moduleName.startsWith('../')    || moduleName.startsWith("@")) {
        return ultimateStubValue;
    }

    return require(moduleName); // fallback to real require
    /*
    Currently known packages which are required even for getInfo:
        - format-message // TODO: possibly replace with translate func
        - scratch-translate-extension-languages
    */
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
            vm: Scratch.vm,
            
            // Required by some extensions, just not available in node
            Audio: ultimateStubValue,
            addEventListener: ultimateStubValue,
            
        };
        vm.createContext(sandbox);
        vm.runInContext(code, sandbox, { filename });

        if (!scratch_ext) {
            const exported = sandbox.module.exports;
            // if a class is exported use it's getInfo
            if (typeof exported === "function" && /^class\s/.test(Function.prototype.toString.call(exported))) {
                register(exported);
                scratch_ext = new scratch_ext(Scratch.vm.runtime)
            } else {
                process.exit(1); // Errno. 1 (nothing or invalid value registered)
            }
            is_class = true;
        }        

        if (!(typeof scratch_ext.getInfo === "function")) {
            process.exit(1); // Errno. 1 (nothing or invalid value registered)
        }

        const extensionInfo = scratch_ext.getInfo();
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
