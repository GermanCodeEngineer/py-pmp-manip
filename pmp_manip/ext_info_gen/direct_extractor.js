const fs = require("fs");
const path = require("path");
const vm = require("vm");
const Module = require("module");

// ---------- Step 1: Blacklist register ----------

const BLACKLIST = new Set(["init", "initialize", "updateVideoDisplay", "_loop"]);

let scratch_ext = null;
let fullExtensionPath;

function register(ext) {
    // Patch the prototype directly
    const proto = typeof ext === "function" ? ext.prototype : Object.getPrototypeOf(ext);
    for (const method of BLACKLIST) {
        if (typeof proto[method] === "function") {
            console.warn(`Patching prototype method '${method}'`);
            proto[method] = function () {};
        }
    }
    scratch_ext = ext;
};

// ---------- Step 2: Setup Stubs and Proxy ----------

let defaultStubValue;

// This design was chosen because all these three will work with the above value as X
// const y = new X()
// X()
// const {a, b} = X
// X.a.b ...
// ... (keep your other imports and code)    

function makeConfiguredStub({
    basis = null,
    valueProps = {},
    funcProps = [],
    allowStaticGet = false,
} = {}) {
    // The stub function/object to return for everything else
    if (basis === null) {
        basis = Object.create(null);
    }

    basis.toString = basis.valueOf = basis[Symbol.toPrimitive] = () => "[STUB; PROPERTY OF py-pmp-manip]"

    // Assign known props
    for (const [key, value] of Object.entries(valueProps)) {
        basis[key] = value;
    }
    for (const funcName of funcProps) {
        basis[funcName] = function () {
            return defaultStubValue;
        };
    }

    // Proxy only property accesses, not apply/construct
    return new Proxy(basis, {
        get(target, prop, receiver) {
            if (Object.prototype.hasOwnProperty.call(target, prop)) {
                return target[prop];
            }
            if (allowStaticGet && typeof prop === "string" && /^[A-Z0-9_]+$/.test(prop)) {
                return prop;
            }
            if (prop === Symbol.toStringTag) return "Function";
            if (prop === "prototype") return target.prototype;
            if (prop === "constructor") return target.constructor;
            return defaultStubValue;
        },
    });
}

// Create the ultimate stub globally
defaultStubValue = makeConfiguredStub({
  basis: function () {return defaultStubValue},
  valueProps: {},
  funcProps: [],
  allowStaticGet: false,
});



// Derived from https://github.com/PenguinMod/PenguinMod-Vm/blob/develop/src/engine/runtime.js
const runtimeStub = makeConfiguredStub({
    basis: Object.create(null),
    valueProps: {
        // Instance properties
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
        
        
        // Methods which are expected to return sth
        getMonitorState: () => new Map(), // OrderedMap in reality, but does not really matter
        getBlocksXML: () => [],
        getBlocksJSON: () => [],
        getScratchLinkSocket: () => defaultStubValue,
        getPeripheralIsConnected: () => false,
        getOpcodeFunction: () => defaultStubValue,
        getIsHat: () => false,
        getIsEdgeActivatedHat: false,
        
        getAddonBlock: () => null,
        getTargetById: () => null,
        getSpriteTargetByName: () => null,
        getTargetByDrawableId: () => null,
        getBranchAndTarget: () => null,
        getCamera: () => defaultStubValue,
        getTargetForStage: () => defaultStubValue,
        getEditingTarget: defaultStubValue,
        getAllVarNamesOfType: () => [],
        getLabelForOpcode: () => defaultStubValue,
        
        _makeExtensionMenuId: () => "myExt_menu_myMenu", 
        _convertMenuItems: () => [],
        _buildMenuForScratchBlocks: () => defaultStubValue,
        _buildCustomFieldInfo: () => defaultStubValue,
        _buildCustomFieldTypeForScratchBlocks: () => defaultStubValue,
        _convertForScratchBlocks: () => defaultStubValue,
        _convertBlockForScratchBlocks: () => defaultStubValue,
        _convertSeparatorForScratchBlocks: () => defaultStubValue,
        _convertLabelForScratchBlocks: () => defaultStubValue,
        _convertButtonForScratchBlocks: () => defaultStubValue,
        _convertXmlForScratchBlocks: () => defaultStubValue,
        _constructInlineImageJson: () => defaultStubValue,
        _constructVariableDropdown: () => defaultStubValue,
        _convertPlaceholders: () => "%1",
        _defaultScratchLinkSocketFactory: () => defaultStubValue,
        _pushThread: () => defaultStubValue,
        _restartThread: () => defaultStubValue,
        isActiveThread: () => false,
        isWaitingThread: () => false,
        startHats: () => [],
        moveExecutable: () => 0,
        setExecutablePosition: () => 0,
        _getMonitorThreadCount: () => 0,
        findProjectOptionsComment: () => null,
        _generateAllProjectOptions: () => defaultStubValue,
        generateDifferingProjectOptions: () => defaultStubValue,
        requestUpdateMonitor: () => false,
        requestHideMonitor: () => false,
        requestShowMonitor: () => false,
        clonesAvailable: () => true,
        createNewGlobalVariable: () => defaultStubValue,

        // Inherited from EventEmitter
        addListener: () => this,
        on: () => this,
        once: () => this,
        removeListener: () => this,
        off: () => this,
        removeAllListeners: () => this,
        setMaxListeners: () => this,
        getMaxListeners: () => 10,
        listeners: () => [],
        rawListeners: () => [],
        emit: () => false,
        listenerCount: () => 0,
        prependListener: () => this,
        prependOnceListener: () => this,
        eventNames: () => [],
        
        // Set only in methods
        renderer: makeConfiguredStub({
            basis: Object.create(null),
            valueProps: {
                _nativeSize: [480, 360], // Idk
            },
            funcProps: [],
            allowStaticGet: false,
        }),
    },
    funcProps: [
        // Methods which are not expected to return sth
        "_initializeAddCloudVariable",
        "_initializeRemoveCloudVariable",
        "_registerBlockPackages",
        "compilerRegisterExtension",
        "registerCompiledExtensionBlocks",
        "registerExtensionAudioContext",
        "makeMessageContextForTarget",
        "_registerExtensionPrimitives",
        "_refreshExtensionPrimitives",
        "_removeExtensionPrimitive",
        "_fillExtensionCategory",
        "configureScratchLinkSocketFactory",
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
        "_stopThread",
        "emitCompileError",
        "toggleScript",
        "addMonitorScript",
        "allScriptsDo",
        "allScriptsByOpcodeDo",
        "dispose",
        "addTarget",
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
        "parseProjectOptions",
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
        "requestRemoveMonitor",
        "requestRemoveMonitorByTargetId",
        "changeCloneCounter",
        "emitProjectLoaded",
        "emitProjectChanged",
        "fireTargetWasCreated",
        "fireTargetWasRemoved",
        "updateCamera",
        "emitCameraChanged",
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
    basis: Object.create(null),
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
            basis: Object.create(null),
            valueProps: {
                unsandboxed: true,
                register: register,
                isPenguinMod: true
            },
        }),
        translate: makeConfiguredStub({
            basis: (m) => (typeof m === "string" ? m : m.default || ""),
            valueProps: {
                setup: makeConfiguredStub({
                    basis: (newTranslations) => makeConfiguredStub({
                        basis: Object.create(null),
                        valueProps: {
                            locale: "en",
                        },
                    }),
                }),
            },
        }),

        vm: makeConfiguredStub({
            basis: Object.create(null),
            valueProps: {
                runtime: runtimeStub,
            },
        }),
        // I only included the properties which a resonable getInfo should use

        // To allow builtin PM extension to import them (they are not used in getInfo)
        Cast: defaultStubValue,
        Clone: defaultStubValue,
        Color: defaultStubValue,
    },
})

// ---------- Step 3: Custom require replacement ----------
const stubModules = [
    path.resolve(__dirname, "../../extension-support/argument-type"),
    path.resolve(__dirname, "../../extension-support/argument-alignment"),
    path.resolve(__dirname, "../../extension-support/block-type"),
    path.resolve(__dirname, "../../extension-support/block-shape"),
    path.resolve(__dirname, "../../extension-support/notch-shape"),
    path.resolve(__dirname, "../../extension-support/target-type"),

    path.resolve(__dirname, "../../util/cast"),
    path.resolve(__dirname, "../../util/clone"),
    path.resolve(__dirname, "../../util/color"),
    path.resolve(__dirname, "../../util/uid"),

    path.resolve(__dirname, "../../extension-support/tw-l10n"),
    path.resolve(__dirname, "../../extension-support/extension-addon-switchers"),
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
    () => "",

    () => ScratchVar.translate,
    makeConfiguredStub({
        basis: () => ({}),
        valueProps: {
            get_extension_switches: () => ({}),
            noopSwitch: {isNoop: true},
        },
    })
];

function myRequire(moduleName) {
    const fullPath = path.resolve(__dirname, moduleName);

    // Forbid access to non-JS files e.g. .png
    const extMatch = fullPath.match(/\.([a-zA-Z0-9]+)$/);
    if (extMatch && extMatch[1] !== "js") {
        return defaultStubValue;
    }

    // Modules you want to return a specific stub value
    if (stubModules.includes(fullPath)) {
        return stubValue[stubModules.indexOf(fullPath)];
    }
    
    // Only stub relative imports under ../../ or from external organizations
    if (moduleName.startsWith("../../") || moduleName.startsWith("@")) {
        return defaultStubValue;
    }
    
    // We do not care about translations and just want english anyway
    if (moduleName === "format-message") {
        return ScratchVar.translate;
    }

    if (moduleName.startsWith("three/")) {
        // can cause problems as the CJS modules of three do not work with require
        return defaultStubValue;
    }

    // fallback to real require
    return require(moduleName);
    /*
    Currently known packages which are required by builtin extensions:
        - scratch-translate-extension-languages
        - three
        - pathfinding
    */
}

const vmEnvironment = {
    ...global,
    // Important:
    module: { exports: {} },
    require: myRequire,
    Scratch: ScratchVar,
    vm: ScratchVar.vm,
    
    window: makeConfiguredStub({
        basis: Object.create(null),
        valueProps: {
            vm: ScratchVar.vm,
        },
    }),
    document: defaultStubValue,
    localStorage: defaultStubValue,
    MutationObserver: defaultStubValue,
}


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
    fullExtensionPath = path.resolve(filePath);
    const code = fs.readFileSync(fullExtensionPath, "utf-8");

    runScript(code, fullExtensionPath);
    process.exit(0);
}

module.exports = {vmEnvironment, defaultStubValue};
