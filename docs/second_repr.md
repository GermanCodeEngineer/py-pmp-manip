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

frproject = FRProject.from_file(file_path="assets/small_example.pmp")
print("Project was loaded from a file successfully :)")

srproject = frproject.to_second(info_api)
print("Project was converted into Second Representation successfully :)")
print("The contents of the project are:")
print(srproject)
```
Output:
```
Project was loaded from a file successfully :)
Project was converted into Second Representation successfully :)
The full contents of the project are:
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
        costume_index=0,
        costumes=[
            SRVectorCostume(
                content=<Element {http://www.w3.org/2000/svg}svg at 0x773bd86c80>,
                name="backdrop1",
                file_extension="svg",
                rotation_center=(240, 180),
            ),
        ],
        sounds=[],
        volume=100,
    ),
    sprites=[
        SRSprite(
            name="Sprite1",
            sprite_only_variables=[
                SRVariable(name="a var for this sprite only!", current_value="welcome"),
            ],
            sprite_only_lists=[
                SRList(name="a list for this sprite only!", current_value=["some item", 0, 45, True]),
            ],
            local_monitors=[
                SRVariableMonitor(
                    readout_mode=SRVariableMonitorReadoutMode.NORMAL,
                    slider_min=0,
                    slider_max=100,
                    allow_only_integers=True,
                    opcode="value of [VARIABLE]",
                    dropdowns={
                        "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="a var for this sprite only!"),
                    },
                    position=(-235, -148),
                    is_visible=True,
                ),
                SRListMonitor(
                    size=(100, 120),
                    opcode="value of [LIST]",
                    dropdowns={
                        "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="a list for this sprite only!"),
                    },
                    position=(-235, -121),
                    is_visible=True,
                ),
                SRMonitor(
                    opcode="size",
                    dropdowns={},
                    position=(-235, 86),
                    is_visible=True,
                ),
            ],
            is_visible=True,
            position=(0, 0),
            size=89,
            direction=90,
            is_draggable=False,
            uuid=UUID('441065cf-e82f-4651-b117-6da716d7701f'),
            scripts=[
                SRScript(
                    position=(243, 257),
                    blocks=[
                        SRBlock(
                            opcode="when green flag clicked",
                            inputs={},
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                        SRBlock(
                            opcode="say (MESSAGE) for (SECONDS) seconds",
                            inputs={
                                "MESSAGE": SRBlockAndTextInputValue(block=None, text="Hello!"),
                                "SECONDS": SRBlockAndTextInputValue(block=None, text="2"),
                            },
                            dropdowns={},
                            comment=None,
                            mutation=None,
                        ),
                    ],
                ),
            ],
            comments=[],
            costume_index=0,
            costumes=[
                SRVectorCostume(
                    content=<Element {http://www.w3.org/2000/svg}svg at 0x773bd86b00>,
                    name="costume1",
                    file_extension="svg",
                    rotation_center=(26, 46),
                ),
            ],
            sounds=[
                SRSound(name="Squawk", file_extension="wav", content=<pydub.audio_segment.AudioSegment object at 0x773bd82630>),
            ],
            volume=100,
        ),
    ],
    sprite_layer_stack=[
        UUID('441065cf-e82f-4651-b117-6da716d7701f'),
    ],
    all_sprite_variables=[
        SRVariable(name="my variable", current_value="hi"),
    ],
    all_sprite_lists=[
        SRList(name="a list for all sprites", current_value=[-694, "thing"]),
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
            dropdowns={
                "VARIABLE": SRDropdownValue(kind=DropdownValueKind.VARIABLE, value="my variable"),
            },
            position=(-235, -175),
            is_visible=True,
        ),
        SRListMonitor(
            size=(100, 120),
            opcode="value of [LIST]",
            dropdowns={
                "LIST": SRDropdownValue(kind=DropdownValueKind.LIST, value="a list for all sprites"),
            },
            position=(140, -127.76918029785156),
            is_visible=True,
        ),
    ],
    extensions=[],
)
```




