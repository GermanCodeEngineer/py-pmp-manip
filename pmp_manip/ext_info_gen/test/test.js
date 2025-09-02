const vm = require('vm');
const fs = require('fs');
const path = require('path');
const StubOject = require("./stub");

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
        return StubOject[stubProperty[stubModules.indexOf(fullPath)]];
    }

    // Only stub relative imports under ../../
    if (moduleName.startsWith('./') || moduleName.startsWith('../')) {
        return {};
    }

    return require(moduleName); // fallback to real require
}

// Read the module code
const code = fs.readFileSync(path.resolve("pmp_manip/ext_info_gen/test/example.js"), 'utf-8');

// Create the sandbox with all globals + overrides
const sandbox = {
    ...global,           // inject all default globals
    module: { exports: {} },
    require: myRequire,
};

// Run the code
vm.createContext(sandbox);
vm.runInContext(code, sandbox);

// Extract the exported value
const exported = sandbox.module.exports;
console.log(exported);

const info = exported.prototype.getInfo();
console.log(JSON.stringify(info, null, 2));

