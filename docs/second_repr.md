# Working with Second Representation in `pmp_manip`

## Project Structure:
This is the UML structure of a `SRProject`:
![Structure of an `SRProject`](images/second_repr_uml.svg)

Let us compare an `SRProject` with it's view in the [PenguinMod Editor](https://studio.penguinmod.com/editor.html)

## Editor View vs. Project Object

### Editor View
![Project Editor View](images/editor_project_view.jpg)

### Project Object

```python
from pmp_manip import get_default_config, init_config, FRProject, info_api

cfg = get_default_config()
init_config(cfg)

frproject = FRProject.from_file(file_path="path/to/my_project.pmp")

srproject = frproject.to_second(info_api)
print("The contents of the project are:")
print(srproject)
```
Output(shortend):
```
The contents of the project are:
SRProject(
    stage=SRStage(
        scripts=[],
        comments=[
            SRComment(
                position=(244.16309497974535, 279.18415210865163),
                size=(200, 200),
                is_minimized=False,
                text="hi from a comment in the stage",
            ),
        ],
        ...
    ),
    sprites=[
        SRSprite(
            name="Sprite1",
            local_variables=[
                SRVariable(name="a var for this sprite only!", current_value="welcome"),
            ],
            local_lists=[
                SRList(name="a list for this sprite only!", current_value=["some item", 0, 45, True]),
            ],
            ...
    ],
    sprite_layer_stack=[
        UUID('da51ce38-832c-457b-84e6-372273438737'),
    ],
    global_variables=[
        SRVariable(name="my variable", current_value="hi"),
    ],
    global_lists=[
        SRList(name="a list for all spritess", current_value=[-694, "thing"]),
    ],
    tempo=60,
    video_transparency=50,
    video_state=SRVideoState.ON,
    text_to_speech_language=None,
    global_monitors=[
        SRVariableMonitor(
            readout_mode=SRVariableMonitorReadoutMode.NORMAL,
            slider_min=0,
            slider_max=100,
            allow_only_integers=True,
            opcode="value of [VARIABLE]",
            ...
        ),
        ...
    ],
    extensions=[],
)
```

Notes:
* I highly recommend to use a good code editor (especially VSCode), because you might want to look at the definition of e.g. a function/method or class(`Alt` + `Left Mouse Click`)
* All listed properties and can be read, set and modified if not specified otherwise.
* Most classes are dataclasses, which implement these features:
    - Initialization (call class with all its properties set (listed below)) (e.g. `SRVariable(name="my variable", current_value=5)`)
    - Comparison (`==`)
    - Mutability (most, a few specified ones are immutable and hashable)
    - Validation (`validate` method, it is recommended to just validate the `SRProject` as a whole => easiest, you will not need to pass in anything but `info_api`)
    - Conversion (most, with `SRProject.to_first` and `FRProject.to_second` methods, it is recommended to just convert the projects as wholes)


## `SRProject`
The "root node" of a project in second representation.
### `SRProject.stage`
- **type**: [`SRStage`(subclass of `SRTarget`)](#srstage)
- **content**: The stage of the project.
### `SRProject.sprites`
- **type**: `list` of [`SRSprite`(subclass of `SRTarget`)](#srsprite)
- **content**: The sprites of the project, excluding the stage.
### `SRProject.sprite_layer_stack`
- **type**: `list` of `UUID`(from package `uuid`)
- **content**: The order of sprites on the stage. Must contain all sprite UUIDs(`SRSprite.uuid`) in any order. Last UUID means sprite is on the highest layer and is rendered on top of all other sprites. First UUID means lowest layer.
### `SRProject.global_variables`
- **type**: `list` of [`SRVariable`](#srvariable)
- **content**: The names and values of the "for all sprites" variables of the project. Local Variables are stored in specific sprites, see [`SRSprite.local_variables`](#srspritelocal_variables).
### `SRProject.global_lists`
- **type**: `list` of [`SRList`](#srlist)
- **content**: The names and values of the "for all sprites" lists of the project. Local Lists are stored in specific sprites, see [`SRSprite.local_lists`](#srspritelocal_lists)
### `SRProject.global_monitors`
- **type**: `list` of [`SRMonitor`](#srmonitor), `SRVariableMonitor`(subclass) and `SRListMonitor`(subclass)
- **content**: The non-sprite-specific monitors of blocks shown or once shown on the stage. Local Monitors are stored in specific sprites, see [`SRSprite.local_monitors`](#srspritelocal_monitors).
### `SRProject.extensions`
- **type**: `list` of `SRBuiltinExtension` or `SRCustomExtension`, see [`SRExtension`(parent class)](#srextension)
- **content**: Stores the ids and possibly urls/sources of all added extensions.
### `*SRProject.tempo*`
- **type**: `int` (minimum: `20`, maximum: `500`)
- **content**: The music "tempo" of Scratch's Music extension in BPM (insignificant for most projects).
- **note**: Equal to value of "tempo" block.
- **default value**: `60`
### `*SRProject.video_transparency*`
- **type**: `int` or `float` (normally between `0` and `100`) (seems not to have limits by Scratch)
- **content**: The "video transparency" of Scratch's Video Sensing extension (insignificant for most projects).
- **note**: Equal to input of "set video transparency to" block.
- **default value**: `50`
### `*SRProject.video_state*`
- **type**: `SRVideoState` (enum class)
- **possible values**: `SRVideoState.ON`, `SRVideoState.ON_FLIPPED`, `SRVideoState.OFF`
- **content**: The "state" of Scratch's Video Sensing extension (insignificant for most projects).
- **note**: Equal to dropdown menu of "turn video ..." block.
- **default value**: `SRVideoState.ON`
### `*SRProject.text_to_speech_language*`
- **type**: [`SRTTSLanguage`](#srttslanguage) (enum class) or `None`
- **possible values**: `SRTTSLanguage.ENGLISH`, `SRTTSLanguage.FRENCH`, `SRTTSLanguage.GERMAN` ...
- **content**: The "text to speech language" of Scratch's TTS extension (insignificant for most projects).
- **note**: Equal to dropdown menu of "set language to" block.
- **default value**: `None`


## `SRTarget`
Common base for [`SRStage`](#srstage) and [`SRSprite`](#srsprite)
### `SRTarget.scripts`
- **type**: `list` of [`SRScript`](#srscript)
- **content**: Stores all the blocks and attached comments in a sprite or the stage.
### `SRTarget.comments`
- **type**: `list` of [`SRComment`](#srcomment)
- **content**: Stores all the comments, which are not attached to a block, in a sprite or the stage.
### `SRTarget.costumes`
- **type**: `list` of `SRVectorCostume` or `SRBitmapCostume`, see [`SRCostume`(parent class)](#srcostume)
- **content**: Stores all the costumes of a sprite or stage.
- **note**: Must have at least one costume(hint: use `SRVectorCostume.create_empty` for an empty default costume)
### `SRTarget.sounds`
- **type**: `list` of [`SRSound`](#srsound)
- **content**: Stores all the sounds of a sprite or stage.
### `SRTarget.costume_index`
- **type**: `int` (at least `0` and at most one less then the amount of costumes)
- **content**: References the current costume of the sprite or stage in `costumes` by index.
- **default value**: `0`
### `SRTarget.volume`
- **type**: `int` (minimum: `0`, maximum: `100`)
- **content**: The local volume for playing sounds from a sprite or stage.
- **default value**: `100`


## `SRStage`
Represents the project stage. Inherits from [`SRTarget`](#srtarget)
Has no additional properties compared to `SRTarget`, as all global information is stored on the project directly.


## `SRSprite`
Represents a sprite of the project. Inherits from [`SRTarget`](#srtarget)
### `SRSprite.name`
- **type**: `str` (Blacklist: `"_myself_"`, `"_stage_"`, `"_mouse_"`, `"_edge_"`)
- **content**: The name of the sprite.
### `SRSprite.local_variables`
- **type**: `list` of [`SRVariable`](#srvariable)
- **content**: The names and values of the "for this sprite only" variables of the sprite. Global Variables are stored in the project directly, see [`SRProject.global_variables`](#srprojectglobal_variables).
### `SRSprite.local_lists`
- **type**: `list` of [`SRList`](#srlist)
- **content**: The names and values of the "for this sprite only" lists of the sprite. Global Lists are stored in the project directly, see [`SRProject.global_lists`](#srprojectglobal_lists)
### `SRSprite.local_monitors`
- **type**: `list` of [`SRMonitor`](#srmonitor), `SRVariableMonitor`(subclass) and `SRListMonitor`(subclass)
- **content**: The sprite-specific monitors of blocks shown or once shown on the stage. Global Monitors are stored in the project directly, see [`SRProject.global_monitors`](#srprojectglobal_monitors).



