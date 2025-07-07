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
    // I only included the properties which a resonable getInfo should use
}
