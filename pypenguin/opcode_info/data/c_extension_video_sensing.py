from pypenguin.utility import DualKeyDict

from pypenguin.opcode_info.api import OpcodeInfoGroup, OpcodeInfo, OpcodeType, InputInfo, InputType, DropdownInfo, DropdownType, MenuInfo


extension_video_sensing = OpcodeInfoGroup(name="extension_video_sensing", opcode_info=DualKeyDict({
    ("videoSensing_whenMotionGreaterThan", "when video motion > (THRESHOLD)"): OpcodeInfo(
        opcode_type=OpcodeType.HAT,
        inputs=DualKeyDict({
            ("REFERENCE", "THRESHOLD"): InputInfo(InputType.NUMBER),
        }),
    ),
    ("videoSensing_videoOn", "video ([PROPERTY]) on ([TARGET])"): OpcodeInfo(
        opcode_type=OpcodeType.STRING_REPORTER,
        inputs=DualKeyDict({
            ("ATTRIBUTE", "PROPERTY"): InputInfo(InputType.VIDEO_SENSING_PROPERTY, menu=MenuInfo("videoSensing_menu_ATTRIBUTE", inner="ATTRIBUTE")),
            ("SUBJECT", "TARGET"): InputInfo(InputType.VIDEO_SENSING_TARGET, menu=MenuInfo("videoSensing_menu_SUBJECT", inner="SUBJECT")),
        }),
    ),
    ("videoSensing_videoToggle", "turn video ([VIDEO_STATE])"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("VIDEO_STATE", "VIDEO_STATE"): InputInfo(InputType.VIDEO_STATE, menu=MenuInfo("videoSensing_menu_VIDEO_STATE", inner="VIDEO_STATE")),
        }),
    ),
    ("videoSensing_setVideoTransparency", "set video transparency to (TRANSPARENCY)"): OpcodeInfo(
        opcode_type=OpcodeType.STATEMENT,
        inputs=DualKeyDict({
            ("TRANSPARENCY", "TRANSPARENCY"): InputInfo(InputType.NUMBER),
        }),
    ),
}))