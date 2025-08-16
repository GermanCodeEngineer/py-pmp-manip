from pmp_manip.opcode_info.api import DropdownValueKind

from pmp_manip.core.context import PartialContext, CompleteContext


def test_CompleteContext_from_partial():
    my_variable = (DropdownValueKind.VARIABLE, "my variable")
    my_sprite_variable = (DropdownValueKind.VARIABLE, "my sprite variable")
    my_list = (DropdownValueKind.LIST, "my list")
    my_sprite_list = (DropdownValueKind.LIST, "my sprite list")
    partial_context = PartialContext(
        scope_variables=[my_variable, my_sprite_variable],
        scope_lists=[my_list, my_sprite_list],

        global_variables=[my_variable],

        local_variables=[my_sprite_variable],
        local_lists=[my_sprite_list],

        other_sprites=[(DropdownValueKind.SPRITE, "Sprite2"), (DropdownValueKind.SPRITE, "Player")],
        backdrops=[(DropdownValueKind.BACKDROP, "intro"), (DropdownValueKind.BACKDROP, "scene1")],
    )
    
    
    costumes = [(DropdownValueKind.COSTUME, "costume1"), (DropdownValueKind.COSTUME, "costume2")],
    sounds = [(DropdownValueKind.SOUND, "hi"), (DropdownValueKind.SOUND, "bye")],
    is_stage = False
    
    complete_context = CompleteContext.from_partial(
        pc=partial_context,
        costumes=costumes,
        sounds=sounds,
        is_stage=is_stage,
    )
    assert isinstance(complete_context, CompleteContext)
    assert complete_context.scope_variables == partial_context.scope_variables
    assert complete_context.scope_lists == partial_context.scope_lists
    assert complete_context.global_variables == partial_context.global_variables
    assert complete_context.local_variables == partial_context.local_variables
    assert complete_context.local_lists == partial_context.local_lists
    assert complete_context.other_sprites == partial_context.other_sprites
    assert complete_context.backdrops == partial_context.backdrops
    assert complete_context.costumes == costumes
    assert complete_context.sounds == sounds
    assert complete_context.is_stage == is_stage

