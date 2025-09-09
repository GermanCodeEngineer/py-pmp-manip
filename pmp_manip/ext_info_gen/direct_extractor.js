const fs = require("fs");
const path = require("path");
const vm = require("vm");
const { interpolate } = require("../../../Penguinmod-VM/src/engine/tw-interpolate");


// ---------- Step 1: whitelist-only register (only keep getInfo) ----------

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

let defaultStubValue;
let isStrict;

// This design was chosen because all these three will work with the above value as X
// const y = new X()
// X()
// const {a, b} = X
// X.a.b ...
function makeConfiguredStub({
    valueProps = {},            // { propName: someValue }
    funcProps = [],             // ["someMethod", "otherMethod"]
    allowStaticGet = false,
} = {}) {
    const handler = {
        get(target, prop, receiver) {
        // Special cases to keep function identity intact
        if (prop === Symbol.toStringTag) return "Function";
        if (prop === "prototype") return target.prototype;
        if (prop === "constructor") return target.constructor;

        // Value properties
        if (Object.prototype.hasOwnProperty.call(valueProps, prop)) {
            return valueProps[prop];
        }

        // Function properties
        if (funcProps.includes(prop)) {
            return (...args) => defaultStubValue;
        }

        // If property is ALL_CAPS (with underscores), return its name as string
        if (allowStaticGet && typeof prop === "string" && /^[A-Z0-9_]+$/.test(prop)) {
            return prop;
        }

        // Unknown property
        if (isStrict) {
            const error = new Error(`Unknown property accessed: ${String(prop)}: =${(new Error()).stack}=`);
            console.error(error.stack); // Print stack trace immediately
            throw error;

        } else {
            return defaultStubValue;
        }
        },

        apply(target, thisArg, args) {
            return defaultStubValue;
        },

        construct(target, args, newTarget) {
            return defaultStubValue;
        }
    };

    function baseTarget(...args) {
        return defaultStubValue;
    }

    return new Proxy(baseTarget, handler);
}

// Create the ultimate stub globally
defaultStubValue = makeConfiguredStub({
  valueProps: {},
  funcProps: [],
  allowStaticGet: false,
});

// Derived from https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/engine/runtime.js
const vmStub = makeConfiguredStub({
    valueProps: {
        targets: [],
        executableTargets: [],
        threads: [],
        threadMap: new Map(),
        sequencer: defaultStubValue,
        flyoutBlocks: defaultStubValue,
        monitorBlocks: defaultStubValue,
        _editingTarget: null,
        _primitives: {},
        _blockInfo: [],
        _hats: {},
        _scriptGlowsPreviousFrame: [],
        _nonMonitorThreadCount: 0,
        _lastStepDoneThreads: null,
        tabManager: defaultStubValue,
        modalManager: defaultStubValue,
        _cloneCounter: 0,
        _refreshTargets: false,
        monitorBlockInfo: {},
        _monitorState: defaultStubValue,
        _prevMonitorState: defaultStubValue,
        turboMode: false,
        frameLoop: defaultStubValue,
        currentStepTime: 1000 / 30,
        redrawRequested: false,
        ioDevices: defaultStubValue,
        peripheralExtensions: {},
        profiler: null,
        cloudOptions: { limit: 10 },
        extensionRuntimeOptions: {javascriptUnsandboxed: false},

        hasCloudData: () => false,
        canAddCloudVariable: () => true,
        getNumberOfCloudVariables: () => 0,
        addCloudVariable: () => {},
        removeCloudVariable: () => {},
        
        origin: null,
        _stageTarget: null,
        addonBlocks: {},
        stageWidth: 480,
        stageHeight: 360,
        runtimeOptions: {
            maxClones: 300,
            miscLimits: true,
            fencing: true,
            dangerousOptimizations: false,
            disableOffscreenRendering: false,
            disableDirectionClamping: false,
        },
        compilerOptions: {
            enabled: true,
            warpTimer: false,
        },
        optimizationUtil: { sin: [], cos: [] },
        debug: false,
        _lastStepTime: Date.now(),
        interpolationEnabled: false,
        interpolate: () => {},
        _defaultStoredSettings: {},
        isPackaged: false,
        isProjectPermissionManagerDisabled: true,
        isPackagedProject: false,
        externalCommunicationMethods: {},
        enforcePrivacy: true,
        extensionButtons: new Map(),
        _extensionAudioObjects: new Map(),
        fontManager: defaultStubValue,
        cameraStates: {
            pos: [0, 0],
            dir: 0,
            scale: 1
        },
        _extensionVariables: {},
        serializers: {},
        variables: {},
        extensionStorage: defaultStubValue,

        STAGE_WIDTH: 480,
        STAGE_HEIGHT: 360,
        THREAD_STEP_INTERVAL: 1000 / 60,
        THREAD_STEP_INTERVAL_COMPATIBILITY: 1000 / 30,
        MAX_CLONES: 300,

        
        "getMonitorState",
        "getBlocksXML",
        "getBlocksJSON",
        "getScratchLinkSocket",
        "getPeripheralIsConnected",
        "getOpcodeFunction",
        "getIsHat",
        "getIsEdgeActivatedHat",
        "getAddonBlock",
        "getTargetById",
        "getSpriteTargetByName",
        "getTargetByDrawableId",
        "getBranchAndTarget",
        "getCamera",
        "getTargetForStage",
        "getEditingTarget",
        "getAllVarNamesOfType",
        "getLabelForOpcode",
    },
    funcProps: [
        "_initializeAddCloudVariable",
        "_initializeRemoveCloudVariable",
        "_registerBlockPackages",
        "compilerRegisterExtension",
        "registerCompiledExtensionBlocks",
        "registerExtensionAudioContext",
        "_makeExtensionMenuId",
        "makeMessageContextForTarget",
        "_registerExtensionPrimitives",
        "_refreshExtensionPrimitives",
        "_removeExtensionPrimitive",
        "_fillExtensionCategory",
        "_convertMenuItems",
        "_buildMenuForScratchBlocks",
        "_buildCustomFieldInfo",
        "_buildCustomFieldTypeForScratchBlocks",
        "_convertForScratchBlocks",
        "_convertBlockForScratchBlocks",
        "_convertSeparatorForScratchBlocks",
        "_convertLabelForScratchBlocks",
        "_convertButtonForScratchBlocks",
        "_convertXmlForScratchBlocks",
        "_constructInlineImageJson",
        "_constructVariableDropdown",
        "_convertPlaceholders",
        "configureScratchLinkSocketFactory",
        "_defaultScratchLinkSocketFactory",
        "registerPeripheralExtension",
        "scanForPeripheral",
        "connectPeripheral",
        "disconnectPeripheral",
        "emitMicListening",
        "attachAudioEngine",
        "attachRenderer",
        "registerSerializer",
        "registerVariable",
        "unregisterVariable",
        "newVariableInstance",
        "attachV2BitmapAdapter",
        "attachStorage",
        "_pushThread",
        "_stopThread",
        "_restartThread",
        "emitCompileError",
        "isActiveThread",
        "isWaitingThread",
        "toggleScript",
        "addMonitorScript",
        "allScriptsDo",
        "allScriptsByOpcodeDo",
        "startHats",
        "dispose",
        "addTarget",
        "moveExecutable",
        "setExecutablePosition",
        "removeExecutable",
        "disposeTarget",
        "stopForTarget",
        "greenFlag",
        "pause",
        "play",
        "stopAll",
        "_renderInterpolatedPositions",
        "updateThreadMap",
        "_step",
        "_getMonitorThreadCount",
        "_pushMonitors",
        "setEditingTarget",
        "setCompatibilityMode",
        "setFramerate",
        "setInterpolation",
        "setRuntimeOptions",
        "setCompilerOptions",
        "setStageSize",
        "setInEditor",
        "convertToPackagedRuntime",
        "resetAllCaches",
        "addAddonBlock",
        "findProjectOptionsComment",
        "parseProjectOptions",
        "_generateAllProjectOptions",
        "generateDifferingProjectOptions",
        "storeProjectOptions",
        "precompile",
        "enableDebug",
        "_updateGlows",
        "_emitProjectRunStatus",
        "quietGlow",
        "glowBlock",
        "glowScript",
        "emitBlockDragUpdate",
        "emitBlockEndDrag",
        "visualReport",
        "requestAddMonitor",
        "requestUpdateMonitor",
        "requestRemoveMonitor",
        "requestHideMonitor",
        "requestShowMonitor",
        "requestRemoveMonitorByTargetId",
        "changeCloneCounter",
        "clonesAvailable",
        "emitProjectLoaded",
        "emitProjectChanged",
        "fireTargetWasCreated",
        "fireTargetWasRemoved",
        "updateCamera",
        "emitCameraChanged",
        "createNewGlobalVariable",
        "requestRedraw",
        "requestTargetsUpdate",
        "requestBlocksUpdate",
        "requestToolboxExtensionsUpdate",
        "start",
        "stop",
        "enableProfiling",
        "disableProfiling",
        "updateCurrentMSecs",
        "updatePrivacy",
        "setEnforcePrivacy",
        "setExternalCommunicationMethod",
    ],
    allowStaticGet: true, // allow e.g. PROJECT_START
});

const ScratchVar = makeConfiguredStub({
    valueProps: {
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
        extensions: makeConfiguredStub({
            valueProps:{
                "unsandboxed": true,
                "register": register,
                "isPenguinMod": true
            },
        }),
        translate: (() => {
            const translateFn = (m) => (typeof m === "string" ? m : m.default || "");
            translateFn.setup = (newTranslations) => {};
            return translateFn;
        })(),

        vm: vmStub,
        // I only included the properties which a resonable getInfo should use

        // To allow builtin PM extension to import them (they are not used in getInfo)
        Cast: class Cast {},
        Clone: class Clone {},
        Color: class Color {},
    },
})

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
    ScratchVar.ArgumentType,
    ScratchVar.ArgumentAlignment,
    ScratchVar.BlockType,
    ScratchVar.BlockShape,
    ScratchVar.NotchShape,
    ScratchVar.TargetType,
    ScratchVar.Cast,
    ScratchVar.Clone,
    ScratchVar.Color,

    () => ScratchVar.translate,
];


function myRequire(moduleName) {
    const fullPath = path.resolve(__dirname, moduleName);

    // Modules you want to return a specific stub value
    if (stubModules.includes(fullPath)) {
        return stubValue[stubModules.indexOf(fullPath)];
    }
    
    // Only stub relative imports under ../../ or from external organizations
    if (moduleName.startsWith('./') || moduleName.startsWith('../')    || moduleName.startsWith("@")) {
        return defaultStubValue;
    }

    return require(moduleName); // fallback to real require
    /*
    Currently known packages which are required even for getInfo:
        - format-message // TODO: possibly replace with translate func
        - scratch-translate-extension-languages
    */
}

const vmEnvironment = makeConfiguredStub({
    valueProps: {
        ...global,
        // Important:
        module: { exports: {} },
        require: myRequire,
        Scratch: ScratchVar,
        vm: ScratchVar.vm,
        
        // Required by some extensions, just not available in node
        Audio: defaultStubValue,
        addEventListener: defaultStubValue,
    }
})

// ---------- Step 4: VM execution wrapper ----------

function runScript(code, filename) {
    try {
        vm.createContext(vmEnvironment);
        vm.runInContext(code, vmEnvironment, { filename });

        if (!scratch_ext) {
            const exported = vmEnvironment.module.exports;
            // if a class is exported use it's getInfo
            if (typeof exported === "function" && /^class\s/.test(Function.prototype.toString.call(exported))) {
                register(exported);
                scratch_ext = new scratch_ext(ScratchVar.vm.runtime)
            } else {
                process.exit(2); // Errno. 2 (nothing or invalid value registered)
            }
            is_class = true;
        }        

        if (!(typeof scratch_ext.getInfo === "function")) {
            process.exit(2); // Errno. 2 (nothing or invalid value registered)
        }

        const extensionInfo = scratch_ext.getInfo();
        console.log(JSON.stringify(extensionInfo)); // must be the last call to console.log() or similar
    } catch (error) {
        if (error && error.stack) {
            console.error(error.stack);
        } else {
            console.error(error);
        }
        process.exit(1);
    }
}

// ---------- Entry point ----------

if (require.main === module) { // like if __name__ == "__main__"
    const filePath = process.argv[2];
    isStrict = JSON.parse(process.argv[3]);
    const fullPath = path.resolve(filePath);
    const code = fs.readFileSync(fullPath, "utf-8");

    runScript(code, fullPath);
    process.exit(0);
}
