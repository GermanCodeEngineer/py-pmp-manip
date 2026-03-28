"""Generate a small Flappy Bird-style PenguinMod project and write `flappy.pmp`.

This script programmatically builds an `SRProject` with two sprites:
- `Bird` — a sprite with simple gravity and a flap on space key
- `Pipe` — a sprite that creates clones which move left and detect collisions

Run by importing and calling `create_and_write_flappy()` or executing the module.
"""
from __future__ import annotations
from pathlib import Path

from pmp_manip import (
    get_default_config,
    init_config,
    info_api,
    SRProject,
    SRSprite,
    SRVectorCostume,
    SRVariable,
)
from lxml import etree
from pmp_manip.utility import AbstractTreePath

from pmp_manip.core.block import (
    SRBlock,
    SRScript,
    SRBlockAndTextInputValue,
    SRBlockAndDropdownInputValue,
    SRBlockAndBoolInputValue,
    SRScriptInputValue,
)
from pmp_manip.core.dropdown import SRDropdownValue
from pmp_manip.opcode_info.api.dropdown import DropdownValueKind


def create_flappy_project() -> SRProject:
    """Construct a minimal Flappy Bird-like SRProject.

    The project contains two sprites and simple scripts for gameplay.
    """
    cfg = get_default_config()
    init_config(cfg)

    sr = SRProject.create_empty()

    # --- Bird sprite -------------------------------------------------
    bird = SRSprite.create_empty(name="Bird")
    # simple bird SVG
    bird_svg = '''
    <svg xmlns="http://www.w3.org/2000/svg" width="120" height="80" viewBox="0 0 120 80">
        <g>
            <ellipse cx="40" cy="40" rx="22" ry="16" fill="#6ab04c" />
            <circle cx="50" cy="32" r="3" fill="#111" />
            <polygon points="62,40 78,36 62,44" fill="#f39c12" />
        </g>
    </svg>
    '''
    bird_elem = etree.fromstring(bird_svg.encode())
    bird.costumes = [SRVectorCostume(name="bird-costume", file_extension="svg", rotation_center=(40,40), content=bird_elem)]
    bird.local_variables.append(SRVariable(name="velocity", current_value=0))

    # when green flag clicked: initialize and enter main loop
    hat = SRBlock(opcode="&events::when green flag clicked")
    set_y = SRBlock(
        opcode="&motion::set y to (Y)",
        inputs={"Y": SRBlockAndTextInputValue(block=None, immediate="0")},
    )
    set_vel = SRBlock(
        opcode="&variables::set [VARIABLE] to (VALUE)",
        dropdowns={"VARIABLE": SRDropdownValue(DropdownValueKind.VARIABLE, "velocity")},
        inputs={"VALUE": SRBlockAndTextInputValue(block=None, immediate="0")},
    )

    # forever body
    # change y by velocity
    vel_reporter = SRBlock(
        opcode="&variables::value of [VARIABLE]",
        dropdowns={"VARIABLE": SRDropdownValue(DropdownValueKind.VARIABLE, "velocity")},
    )
    change_y = SRBlock(
        opcode="&motion::change y by (DY)",
        inputs={"DY": SRBlockAndTextInputValue(block=vel_reporter, immediate="0")},
    )

    # gravity: change velocity by -0.6
    change_vel = SRBlock(
        opcode="&variables::change [VARIABLE] by (VALUE)",
        dropdowns={"VARIABLE": SRDropdownValue(DropdownValueKind.VARIABLE, "velocity")},
        inputs={"VALUE": SRBlockAndTextInputValue(block=None, immediate="-0.6")},
    )

    # if key space pressed then set velocity to 8
    key_check = SRBlock(
        opcode="&sensing::key ([KEY]) pressed?",
        inputs={"KEY": SRBlockAndDropdownInputValue(block=None, dropdown=SRDropdownValue(DropdownValueKind.STANDARD, "space"))},
    )
    set_vel_8 = SRBlock(
        opcode="&variables::set [VARIABLE] to (VALUE)",
        dropdowns={"VARIABLE": SRDropdownValue(DropdownValueKind.VARIABLE, "velocity")},
        inputs={"VALUE": SRBlockAndTextInputValue(block=None, immediate="8")},
    )
    if_space = SRBlock(
        opcode="&control::if <CONDITION> then {THEN}",
        inputs={
            "CONDITION": SRBlockAndBoolInputValue(block=key_check, immediate=False),
            "THEN": SRScriptInputValue(blocks=[set_vel_8]),
        },
    )

    # if touching Pipe then broadcast game over
    touching_pipe = SRBlock(
        opcode="&sensing::touching ([OBJECT]) ?",
        inputs={"OBJECT": SRBlockAndDropdownInputValue(block=None, dropdown=SRDropdownValue(DropdownValueKind.SPRITE, "Pipe"))},
    )
    broadcast_game_over = SRBlock(
        opcode="&events::broadcast ([MESSAGE])",
        inputs={"MESSAGE": SRBlockAndDropdownInputValue(block=None, dropdown=SRDropdownValue(DropdownValueKind.BROADCAST_MSG, "game over"))},
    )
    if_touch = SRBlock(
        opcode="&control::if <CONDITION> then {THEN}",
        inputs={
            "CONDITION": SRBlockAndBoolInputValue(block=touching_pipe, immediate=False),
            "THEN": SRScriptInputValue(blocks=[broadcast_game_over]),
        },
    )

    forever_body = SRBlock(
        opcode="&control::forever {BODY}",
        inputs={"BODY": SRScriptInputValue(blocks=[change_y, change_vel, if_space, if_touch])},
    )

    bird_script = SRScript(position=(0, 0), blocks=[hat, set_y, set_vel, forever_body])
    bird.scripts.append(bird_script)

    # --- Pipe sprite -------------------------------------------------
    pipe = SRSprite.create_empty(name="Pipe")
    # simple pipe SVG (top and bottom with gap)
    pipe_svg = '''
    <svg xmlns="http://www.w3.org/2000/svg" width="80" height="200" viewBox="0 0 80 200">
        <g>
            <rect x="0" y="0" width="80" height="60" fill="#27ae60" />
            <rect x="0" y="140" width="80" height="60" fill="#27ae60" />
        </g>
    </svg>
    '''
    pipe_elem = etree.fromstring(pipe_svg.encode())
    pipe.costumes = [SRVectorCostume(name="pipe-costume", file_extension="svg", rotation_center=(40,100), content=pipe_elem)]

    # when green flag clicked -> spawn clones repeatedly
    hat_pipe = SRBlock(opcode="&events::when green flag clicked")
    create_clone = SRBlock(
        opcode="&control::create clone of ([TARGET])",
        inputs={"TARGET": SRBlockAndDropdownInputValue(block=None, dropdown=SRDropdownValue(DropdownValueKind.MYSELF, "myself"))},
    )
    wait_block = SRBlock(opcode="&control::wait (SECONDS) seconds", inputs={"SECONDS": SRBlockAndTextInputValue(block=None, immediate="1.5")})
    forever_spawn = SRBlock(opcode="&control::forever {BODY}", inputs={"BODY": SRScriptInputValue(blocks=[create_clone, wait_block])})
    pipe.scripts.append(SRScript(position=(0, 0), blocks=[hat_pipe, forever_spawn]))

    # when I start as a clone: position and move left then delete
    hat_clone = SRBlock(opcode="&control::when I start as a clone")
    # spawn off-screen to the right and pick a Y within a safe central range
    set_x = SRBlock(opcode="&motion::set x to (X)", inputs={"X": SRBlockAndTextInputValue(block=None, immediate="300")})
    random_y = SRBlock(opcode="&operators::pick random (OPERAND1) to (OPERAND2)", inputs={
        "OPERAND1": SRBlockAndTextInputValue(block=None, immediate="-60"),
        "OPERAND2": SRBlockAndTextInputValue(block=None, immediate="60"),
    })
    set_y_clone = SRBlock(opcode="&motion::set y to (Y)", inputs={"Y": SRBlockAndTextInputValue(block=random_y, immediate="0")})
    show_block = SRBlock(opcode="&looks::show")
    change_x = SRBlock(opcode="&motion::change x by (DX)", inputs={"DX": SRBlockAndTextInputValue(block=None, immediate="-4")})
    # if touching Bird then broadcast game over
    touching_bird = SRBlock(opcode="&sensing::touching ([OBJECT]) ?", inputs={"OBJECT": SRBlockAndDropdownInputValue(block=None, dropdown=SRDropdownValue(DropdownValueKind.SPRITE, "Bird"))})
    if_touch_bird = SRBlock(opcode="&control::if <CONDITION> then {THEN}", inputs={
        "CONDITION": SRBlockAndBoolInputValue(block=touching_bird, immediate=False),
        "THEN": SRScriptInputValue(blocks=[broadcast_game_over]),
    })
    # delete when offscreen: check x position each step
    delete_clone = SRBlock(opcode="&control::delete this clone")
    x_pos = SRBlock(opcode="&motion::x position")
    less_than = SRBlock(
        opcode="&operators::(OPERAND1) < (OPERAND2)",
        inputs={
            "OPERAND1": SRBlockAndTextInputValue(block=x_pos, immediate="0"),
            "OPERAND2": SRBlockAndTextInputValue(block=None, immediate="-260"),
        },
    )
    if_offscreen = SRBlock(
        opcode="&control::if <CONDITION> then {THEN}",
        inputs={
            "CONDITION": SRBlockAndBoolInputValue(block=less_than, immediate=False),
            "THEN": SRScriptInputValue(blocks=[delete_clone]),
        },
    )
    forever_move = SRBlock(opcode="&control::forever {BODY}", inputs={"BODY": SRScriptInputValue(blocks=[change_x, if_offscreen])})

    pipe_clone_script = SRScript(position=(0, 0), blocks=[hat_clone, set_x, set_y_clone, show_block, forever_move])
    pipe.scripts.append(pipe_clone_script)

    # Add sprites to project
    sr.sprites.extend([bird, pipe])
    sr.sprite_layer_stack = [bird.uuid, pipe.uuid]

    return sr


def create_and_write_flappy(output: str | Path = "flappy.pmp") -> Path:
    out = Path(output)
    project = create_flappy_project()
    # Validate project to catch structural/opcode errors early
    try:
        project.validate(AbstractTreePath(), info_api)
    except Exception as e:
        print("Project validation failed:", e)
        raise
    fr = project.to_first(info_api)
    fr.to_file(str(out))
    return out


if __name__ == "__main__":
    out = create_and_write_flappy("flappy.pmp")
    print(f"Wrote project: {out.resolve()}")
