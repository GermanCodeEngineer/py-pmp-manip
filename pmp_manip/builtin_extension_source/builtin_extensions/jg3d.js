const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');

const Icons = {
    // Icons do not matter for my purpose
    Cube: null,
    Sphere: null,
    Plane: null,
    Light: null,
    OBJ: null,
    Camera: null,
    Touching: null,
    Wireframe: null,
    Raycast: null,
}

const blockIconURI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAT6SURBVHhe7ZtdqBVVFMfXnHuvXG9i9/ZhWYGVYWoggqGVFSV9ywUpohch+lARFXwRAu1BEB97kNAKheiphyAKEqKXICIyKuhFS0Qh+yKvZqLXj+sZ//+99syZU/ecMx975pzDzA/WzFpzzszstWatvfeZmSMV3WXArkvHOMSPyFJIKRiChI6PL2kKAsWDFEqRJ6SDhgGcdeoAFG4ZRCNeNpujFNauIk40AblBVZH6fpx0mrPW6wjMOmson0OeUTU/anadB9sgvMbG+fdfhYGrPp3zpIaW8PMDr9kNIk9DuP+LxsqJPDLgRsgpVUXunyfy3ZtQkpwJbt/9hsjx8CiG6yAXVHWH6wCEdT42InJ6D5QsZ8DRZm8SOXfJ2orTNrs62J+QW1QVmXxHZJj9vSPOToqMbraG8gfkNlWzkbUPWA/hVTfO/7gTBurYpfPk+pl63P2v2A0icyE87xPGykDGBFWW3ynyLeu8CHDWFbtEDp2wtpLaj6Q78vsYsJQhTGQvvwvFVSElZAjD5lTYGkPiliTZ4STkdlVxIT7A4orqXQUeeBhiIxyGLFa1M3H6gNUQprtxft9aGJzF9YLzBC1je7Zx1qAsgrC9DxurA+0yYAxyWlWRNfi58jF74i6leyzg9sLtIj//ZW1lFHJW1f/Tyh1uN9U1MkPk/F67pV9AIGZsQJJetXab1rf6gAk+OPUZ5ucc4fuUr4+hDnYb9RBkhdH+Q9s+YGA+FisRUFZUH1FnezFTWLlK7XbEmgh57E4ozUNO70HHMT+sJZgjxp8J8uCPQB4wVu/Bn2B0PGG2Jp8K8y4ey4J9aw9QH8aCE2N01mlIHgCLdx8WCIQ0etpCMf0SHK9xsM5A6gCEPGolYeqlJXDcc/Jb0EUACLMAnaT/kJp54c9x53iAmwBYzO0u9g/skBxSH8SCVz2HpwhOAxDgLcSCgch4dJ+ZxTq/We08yCUAAd6DWLCjTDp/YJ0j1b071MyTXAMQgvmDv8zqHTDlk2I8T0sxAQAex2uWRYtOrM5xnHWecjxPS2EBCPDuwoKBsPMHn+XBOnfcccal8AAEeJw74MeWF95j6g5dC0CvUAXArktLFQC7Li1VAOy6tFQBsOvSUgXArktLFQC7Li3tA8B7cf3MrM5PdFt9YzYkfKTs/4JFHo/F+ODV+YtvYACONd4XIC0j0SoD/oWE92a8BSL3PAmloNtUWVjwenznSbsS4CNy7mxuYh37FcYikYkLndOqG5ycQPueEzn6u92AAoB0bGwSbw5CnlUVycD0/Uf11LgoAVxCr/mN4rchW1TtTJrLeRli3gQcRpFM/kQtJRkDUFuNC9Fclon9STMMsm8wL0BfRCj4EOSlrbQKAg4v3YzzIt0jzs+EpKrNVDtF4NsC36gq8ulekfEYb2WEJM2A4Zp4q5qGo3shHKNSkzUAAXwva46quDK/YXFO9bbEDcAIGvqY1RUG3cmjWFcBCAiT8qYxkb/D3GhBjADMel7k/EVrKE7bnKYPaAcbN4/KqTMw0D+89yGt5GzZh/1R5xHn50JcXzD3B4zwAuQjVTGt/B7TS/7lIco0GfDFDyJP7bCGwkcoX6nqnjwDENA0UPnHsQj+ABENAPpx73GrK8ihxn+N+h2WGgNhZPF8jGBHIF9CDop/62jjMyuuS7NnQH/ecPSTPUNRpyml4S1I1PGNkIqKiqIRuQYHeAEU9sBGCQAAAABJRU5ErkJggg==";

const seperator = "---";

function infoMenu(array) {
    return {
        acceptReporters: true,
        items: array.map(item => ({ text: item, value: item }))
    }
}
function infoLabel(text) {
    return {
        blockType: BlockType.LABEL,
        text: text
    }
}
function infoArgument(value, extra, extra2) {
    switch (typeof value) {
        case "number":
            return { type: ArgumentType.NUMBER, defaultValue: value };
        case "boolean":
            return { type: ArgumentType.BOOLEAN, defaultValue: value };
        case "string":
            switch (value) {
                case "COLOR":
                    return { type: ArgumentType.COLOR };
                case "ANGLE":
                    return { type: ArgumentType.ANGLE };
                case "MATRIX":
                    return { type: ArgumentType.MATRIX };
                case "NOTE":
                    return { type: ArgumentType.NOTE, defaultValue: 60 };
                case "POLYGON":
                    return { type: ArgumentType.POLYGON, nodes: extra };
                case "IMAGE":
                    return { type: ArgumentType.IMAGE, dataURI: extra, alt: extra2 };
                default:
                    return { type: ArgumentType.STRING, defaultValue: value };
            }
    }
}
function infoArgumentMenu(type, menu) {
    return {
        type: type,
        menu: menu
    }
}

function createCommandBlock(opcode, text, args, icon, hidden) {
    const obj = {
        opcode: opcode,
        text: text ? text : opcode,
        blockType: BlockType.COMMAND
    }
    if (args) {
        obj.arguments = args;
    }
    if (icon) {
        obj.blockIconURI = icon;
    }
    if (hidden === true) {
        obj.hideFromPalette = true;
    }
    return obj;
}
function createReporterBlock(opcode, text, args, icon, disablemonitor) {
    const obj = {
        opcode: opcode,
        text: text ? text : opcode,
        blockType: BlockType.REPORTER
    }
    if (typeof disablemonitor === 'boolean') {
        obj.disableMonitor = disablemonitor;
    }
    if (args) {
        obj.arguments = args;
    }
    if (icon) {
        obj.blockIconURI = icon;
    }
    return obj;
}
function createBooleanBlock(opcode, text, args, icon) {
    const obj = {
        opcode: opcode,
        text: text ? text : opcode,
        blockType: BlockType.BOOLEAN,
        disableMonitor: true
    }
    if (args) {
        obj.arguments = args;
    }
    if (icon) {
        obj.blockIconURI = icon;
    }
    return obj;
}

/**
 * Class for 3D blocks
 * @constructor
 */
class Jg3DBlocks {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'jg3d',
            name: '3D',
            color1: '#B100FE',
            color2: '#8600C3',
            color3: '#5B0088',
            blockIconURI: blockIconURI,
            blocks: [
                infoLabel("Initializing your scene"),
        
                createCommandBlock('initialize', 'create 3D scene'),
                createCommandBlock('dispose', 'remove 3D scene'),
                seperator,
                createCommandBlock(
                    'setCameraPerspective0',
                    'set scene camera to perspective camera with fov: [FOV]',
                    {
                        FOV: infoArgument(70)
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'setCameraPerspective1',
                    'set scene camera to perspective camera with fov: [FOV] aspect ratio: [AR]',
                    {
                        FOV: infoArgument(70),
                        AR: infoArgument(480 / 360)
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'setCameraPerspective2',
                    'set scene camera to perspective camera with fov: [FOV] aspect ratio: [AR] and only render objects within [NEAR] and [FAR] units of the camera',
                    {
                        FOV: infoArgument(70),
                        AR: infoArgument(480 / 360),
                        NEAR: infoArgument(0.1),
                        FAR: infoArgument(1000)
                    },
                    Icons.Camera
                ),
                seperator,
                createCommandBlock('setCameraOrthographic0', 'set scene camera to orthographic camera', null, Icons.Camera),
                createCommandBlock(
                    'setCameraOrthographic1',
                    'set scene camera to orthographic camera with left plane: [LEFT] right plane: [RIGHT] top plane: [TOP] bottom plane: [BOTTOM]',
                    {
                        LEFT: infoArgument(-480 / 2),
                        RIGHT: infoArgument(480 / 2),
                        TOP: infoArgument(360 / 2),
                        BOTTOM: infoArgument(-360 / 2)
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'setCameraOrthographic2',
                    'set scene camera to orthographic camera with left plane: [LEFT] right plane: [RIGHT] top plane: [TOP] bottom plane: [BOTTOM] and only render objects within [NEAR] and [FAR] units of the camera',
                    {
                        LEFT: infoArgument(-480 / 2),
                        RIGHT: infoArgument(480 / 2),
                        TOP: infoArgument(360 / 2),
                        BOTTOM: infoArgument(-360 / 2),
                        NEAR: infoArgument(1),
                        FAR: infoArgument(1000)
                    },
                    Icons.Camera
                ),
                seperator,
                createCommandBlock('render'),
        
                infoLabel("Scene customization"),
        
                createCommandBlock('setSceneLayer', "move 3D scene layer to [SIDE]", {
                    SIDE: infoArgumentMenu(ArgumentType.STRING, "frontBack")
                }),
                createCommandBlock('setSceneBackgroundColor', "set background color to [COLOR]", {
                    COLOR: infoArgument("COLOR")
                }),
                createCommandBlock('setSceneBackgroundOpacity', "set background transparency to [OPACITY]%", {
                    OPACITY: infoArgument(100)
                }),
                createCommandBlock("show3d", "show 3D scene", {}),
                createCommandBlock("hide3d", "hide 3D scene", {}),
                createBooleanBlock("is3dVisible", "is 3D scene visible?", {}),
        
                infoLabel("Camera controls"),
        
                createCommandBlock(
                    'MoveCameraBy',
                    'move camera by [AMOUNT]',
                    {
                        AMOUNT: infoArgument(10)
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'setCameraPosition',
                    'set camera position to x: [X] y: [Y] z: [Z]',
                    {
                        X: infoArgument(0),
                        Y: infoArgument(0),
                        Z: infoArgument(0)
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'changeCameraPosition',
                    'change camera position by x: [X] y: [Y] z: [Z]',
                    {
                        X: infoArgument(0),
                        Y: infoArgument(0),
                        Z: infoArgument(0)
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'setCameraRotation',
                    'set camera rotation to x: [X] y: [Y] z: [Z]',
                    {
                        X: infoArgument('ANGLE'),
                        Y: infoArgument('ANGLE'),
                        Z: infoArgument('ANGLE')
                    },
                    Icons.Camera
                ),
                createCommandBlock(
                    'changeCameraRotation',
                    'change camera rotation by x: [X] y: [Y] z: [Z]',
                    {
                        X: infoArgument('ANGLE'),
                        Y: infoArgument('ANGLE'),
                        Z: infoArgument('ANGLE')
                    },
                    Icons.Camera
                ),
                createCommandBlock('setCameraZoom', 'set camera zoom to [ZOOM]%', {
                    ZOOM: infoArgument(100)
                }, Icons.Camera),
                createReporterBlock("getCameraClipPlane", "camera [CLIPPLANE]", {
                    CLIPPLANE: infoArgumentMenu(ArgumentType.STRING, "clippingPlanes")
                }, Icons.Camera),
                createReporterBlock("getCameraPosition", "camera [VECTOR3] position", {
                    VECTOR3: infoArgumentMenu(ArgumentType.STRING, "vector3")
                }, Icons.Camera),
                createReporterBlock("getCameraRotation", "camera [VECTOR3] rotation", {
                    VECTOR3: infoArgumentMenu(ArgumentType.STRING, "vector3")
                }, Icons.Camera),
                createReporterBlock("getCameraAspectRatio", "camera aspect ratio", null, Icons.Camera),
                createReporterBlock("getCameraZoom", "camera zoom", null, Icons.Camera),
                createReporterBlock("getCameraFov", "camera fov", null, Icons.Camera),
                seperator,
                createBooleanBlock("isCameraPerspective", "is scene camera a perspective camera?", null, Icons.Camera),
                createBooleanBlock("isCameraOrthographic", "is scene camera an orthographic camera?", null, Icons.Camera),
        
                infoLabel("Objects"),
        
                createBooleanBlock("doesObjectExist", "object named [NAME] exists?", {
                    NAME: infoArgument("Object1")
                }),
                createReporterBlock("existingObjectsArray", "existing [OBJECTLIST]", {
                    OBJECTLIST: infoArgumentMenu(ArgumentType.STRING, "objectTypeList")
                }),
                seperator,
                createCommandBlock('createCubeObject', 'create cube named [NAME] at x: [X] y: [Y] z: [Z]', {
                    NAME: infoArgument("Object1"),
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0)
                }, Icons.Cube),
                createCommandBlock('createSphereObject', 'create sphere named [NAME] at x: [X] y: [Y] z: [Z]', {
                    NAME: infoArgument("Object1"),
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0)
                }, Icons.Sphere),
                createCommandBlock('createPlaneObject', 'create plane named [NAME] at x: [X] y: [Y] z: [Z]', {
                    NAME: infoArgument("Object1"),
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0)
                }, Icons.Plane),
                createCommandBlock('createMeshObject', 'create mesh named [NAME] with .obj data: [URL] at x: [X] y: [Y] z: [Z]', {
                    NAME: infoArgument("Object1"),
                    URL: infoArgument("data:text/plain;base64,"),
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0)
                }, Icons.OBJ, true),
                createCommandBlock('createMeshObjectFileTyped', 'create mesh named [NAME] with [FILETYPE] data: [URL] at x: [X] y: [Y] z: [Z]', {
                    NAME: infoArgument("Object1"),
                    FILETYPE: infoArgumentMenu(ArgumentType.STRING, "meshFileTypes"),
                    URL: infoArgument("data:text/plain;base64,"),
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0)
                }, Icons.OBJ),
                createCommandBlock('createLightObject', 'create [LIGHTTYPE] light named [NAME] at x: [X] y: [Y] z: [Z]', {
                    LIGHTTYPE: infoArgumentMenu(ArgumentType.STRING, "lightType"),
                    NAME: infoArgument("Light1"),
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0)
                }, Icons.Light),
                seperator,
                createCommandBlock('moveObjectUnits', 'move object named [NAME] by [AMOUNT]', {
                    NAME: infoArgument("Object1"),
                    AMOUNT: infoArgument(10)
                }),
                createCommandBlock("setObjectPosition", "move object named [NAME] to x: [X] y: [Y] z: [Z]", {
                    NAME: infoArgument("Object1"),
                    X: infoArgument(1),
                    Y: infoArgument(1),
                    Z: infoArgument(1)
                }),
                createCommandBlock("setObjectRotation", "set rotation of object named [NAME] to x: [X] y: [Y] z: [Z]", {
                    NAME: infoArgument("Object1"),
                    X: infoArgument('ANGLE'),
                    Y: infoArgument('ANGLE'),
                    Z: infoArgument('ANGLE')
                }),
                createCommandBlock("setObjectSize", "set size of object named [NAME] to x: [X]% y: [Y]% z: [Z]%", {
                    NAME: infoArgument("Object1"),
                    X: infoArgument(100),
                    Y: infoArgument(100),
                    Z: infoArgument(100)
                }),
                createCommandBlock('pointTowardsObject', 'point object named [NAME1] towards object named [NAME2]', {
                    NAME1: infoArgument("Object1"),
                    NAME2: infoArgument("Object2"),
                }),
                createCommandBlock('pointTowardsXYZ', 'point object named [NAME] towards x: [X] y: [Y] z: [Z]', {
                    NAME: infoArgument("Object1"),
                    X: infoArgument(31),
                    Y: infoArgument(26),
                    Z: infoArgument(47),
                }),
                createReporterBlock("getObjectPosition", "[VECTOR3] position of object named [NAME]", {
                    VECTOR3: infoArgumentMenu(ArgumentType.STRING, "vector3"),
                    NAME: infoArgument("Object1"),
                }),
                createReporterBlock("getObjectRotation", "[VECTOR3] rotation of object named [NAME]", {
                    VECTOR3: infoArgumentMenu(ArgumentType.STRING, "vector3"),
                    NAME: infoArgument("Object1"),
                }),
                createReporterBlock("getObjectSize", "[VECTOR3] size of object named [NAME]", {
                    VECTOR3: infoArgumentMenu(ArgumentType.STRING, "vector3"),
                    NAME: infoArgument("Object1"),
                }),
                createReporterBlock("getObjectColor", "hex color of object named [NAME]", {
                    NAME: infoArgument("Object1"),
                }),
                createReporterBlock("getObjectParent", "parent of object named [NAME]", {
                    NAME: infoArgument("Object1"),
                }),
                seperator,
                createBooleanBlock("objectTouchingObject", "object [NAME1] touching object [NAME2]?", {
                    NAME1: infoArgument("Object1"),
                    NAME2: infoArgument("Object2"),
                }, Icons.Touching),
                seperator,
                createCommandBlock("deleteObject", "remove object named [NAME]", {
                    NAME: infoArgument("Object1")
                }),
                createCommandBlock("setObjectColor", "recolor object named [NAME] to [COLOR]", {
                    NAME: infoArgument("Object1"),
                    COLOR: infoArgument("COLOR"),
                }),
                createCommandBlock("setObjectShading", "turn [ONOFF] shading on object named [NAME]", {
                    ONOFF: infoArgumentMenu(ArgumentType.STRING, "onoff"),
                    NAME: infoArgument("Object1"),
                }),
                createCommandBlock("setObjectWireframe", "turn [ONOFF] wireframe view on object named [NAME]", {
                    ONOFF: infoArgumentMenu(ArgumentType.STRING, "onoff"),
                    NAME: infoArgument("Object1"),
                }, Icons.Wireframe),
                seperator,
                createReporterBlock("rayCollision", "first object in raycast from x: [X] y: [Y] z: [Z] with direction x: [DX] y: [DY] z: [DZ]", {
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0),
                    DX: infoArgument(0),
                    DY: infoArgument(0),
                    DZ: infoArgument(0),
                }, Icons.Raycast, true),
                createReporterBlock("rayCollisionArray", "raycast result from x: [X] y: [Y] z: [Z] with direction x: [DX] y: [DY] z: [DZ]", {
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0),
                    DX: infoArgument(0),
                    DY: infoArgument(0),
                    DZ: infoArgument(0),
                }, Icons.Raycast, true),
                createReporterBlock("rayCollisionDistance", "first object in raycast from x: [X] y: [Y] z: [Z] with direction x: [DX] y: [DY] z: [DZ] with a max distance of [DIS]", {
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0),
                    DX: infoArgument(0),
                    DY: infoArgument(0),
                    DZ: infoArgument(0),
                    DIS: infoArgument(10)
                }, Icons.Raycast, true),
                createReporterBlock("rayCollisionArrayDistance", "raycast result from x: [X] y: [Y] z: [Z] with direction x: [DX] y: [DY] z: [DZ] with a max distance of [DIS]", {
                    X: infoArgument(0),
                    Y: infoArgument(0),
                    Z: infoArgument(0),
                    DX: infoArgument(0),
                    DY: infoArgument(0),
                    DZ: infoArgument(0),
                    DIS: infoArgument(10)
                }, Icons.Raycast, true),
                createReporterBlock("rayCollisionCamera", "first object from raycast in camera center", {
                }, Icons.Raycast, true),
                createReporterBlock("rayCollisionCameraArray", "raycast result starting from the camera center", {
                }, Icons.Raycast, true)
            ],
            menus: {
                cameraType: infoMenu(["perspective", "orthographic"]),
                lightType: infoMenu(["point"]),
                clippingPlanes: infoMenu(["near", "far"]),
                frontBack: infoMenu(["front", "back"]),
                vector3: infoMenu(["x", "y", "z"]),
                vector2: infoMenu(["x", "y"]),
                onoff: infoMenu(["on", "off"]),
                objectTypeList: infoMenu(["objects", "physical objects", "lights"]),
                meshFileTypes: infoMenu([".obj", ".glb / .gltf", ".fbx"])
            }
        };
    }
}

module.exports = Jg3DBlocks;
