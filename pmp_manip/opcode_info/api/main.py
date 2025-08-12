from dataclasses import field
from importlib   import util as importutil
from os          import path
from sys         import modules as sys_modules
from typing      import TYPE_CHECKING, Type, Iterable

from pmp_manip.utility import (
    grepr_dataclass, enforce_argument_types, file_exists, GEnum, DualKeyDict, 
    MANIP_UnknownOpcodeError, MANIP_SameOpcodeTwiceError,
    MANIP_ExtensionModuleNotFoundError, MANIP_UnexpectedExtensionModuleImportError, MANIP_UnknownBuiltinExtensionError,
)

from pmp_manip.opcode_info.api.input        import InputInfo
from pmp_manip.opcode_info.api.dropdown     import DropdownInfo
from pmp_manip.opcode_info.api.special_case import SpecialCase, SpecialCaseType

if TYPE_CHECKING:
    from pmp_manip.core.block_interface import FirstToInterIF, ValidationIF
    from pmp_manip.core.block_mutation  import FRMutation, SRMutation
    from pmp_manip.core.block           import FRBlock, IRBlock, SRBlock


@grepr_dataclass(grepr_fields=["id", "module_dir"])
class ExtensionRef:
    """
    A reference to an extension and its opcode info file
    """
    id: str
    module_dir: str

BUILTIN_MODULE_DIR = "pmp_manip/opcode_info/data/"
class BuiltinExtensionRef:
    makeymakey   = ExtensionRef("scratch_makey_makey"   , BUILTIN_MODULE_DIR)
    music        = ExtensionRef("scratch_music"         , BUILTIN_MODULE_DIR)
    pen          = ExtensionRef("scratch_pen"           , BUILTIN_MODULE_DIR)
    text2speech  = ExtensionRef("scratch_text_to_speech", BUILTIN_MODULE_DIR)
    text         = ExtensionRef("scratch_text"          , BUILTIN_MODULE_DIR)
    translate    = ExtensionRef("scratch_translate"     , BUILTIN_MODULE_DIR)
    videoSensing = ExtensionRef("scratch_video_sensing" , BUILTIN_MODULE_DIR)

    tw_files     = ExtensionRef("tw_files"              , BUILTIN_MODULE_DIR)
    lmsTempVars2 = ExtensionRef("tw_temporary_variables", BUILTIN_MODULE_DIR)

    jgJSON       = ExtensionRef("pm_json"               , BUILTIN_MODULE_DIR)

class OpcodeType(GEnum):
    """
    Represents the shape of all blocks with a certain opcode
    """
    
    @property
    def is_reporter(self) -> bool:
        """
        Return wether a OpcodeType is a reporter shape
        
        Returns:
            wether a OpcodeType is a reporter shape
        """
        return self.value[0]

    STATEMENT         = (False, 0)
    ENDING_STATEMENT  = (False, 1)
    HAT               = (False, 2)
    
    STRING_REPORTER   = (True , 3)
    NUMBER_REPORTER   = (True , 4)
    BOOLEAN_REPORTER  = (True , 5)
    
    # Pseudo Blocktypes
    MENU              = (False, 6)
    POLYGON_MENU      = (False, 7) # Exclusively for the "polygon" block 
    NOT_RELEVANT      = (False, 8)
    DYNAMIC           = (False, 9)
# TODO: find solution for draw polygon block

class MonitorIdBehaviour(GEnum):
    """
    The orientation basis for monitor id generation
    """

    SPRITE_OPCMAIN        = 0
    SPRITE_OPCMAIN_PARAMS = 1
    OPCMAIN_PARAMS        = 2
    OPCMAIN_LOWERPARAM    = 3
    OPCMAIN               = 4
    OPCFULL_PARAMS        = 5
    OPCFULL               = 6
    VARIABLE              = 7
    LIST                  = 8
    

@grepr_dataclass(grepr_fields=["opcode_type", "inputs", "dropdowns", "can_have_monitor", "monitor_id_behaviour", "has_shadow", "has_variable_id", "special_cases", "old_mutation_cls", "new_mutation_cls"])
class OpcodeInfo:
    """
    The information about all the blocks with a certain opcode
    """
    
    opcode_type: OpcodeType
    inputs: DualKeyDict[str, str, InputInfo] = field(default_factory=DualKeyDict)
    dropdowns: DualKeyDict[str, str, DropdownInfo] = field(default_factory=DualKeyDict)
    can_have_monitor: bool = False
    monitor_id_behaviour: MonitorIdBehaviour | None = None
    has_shadow: bool = None
    has_variable_id: bool = False
    special_cases: dict[SpecialCaseType, SpecialCase] = field(default_factory=dict)
    old_mutation_cls: Type["FRMutation"] | None = None
    new_mutation_cls: Type["SRMutation"] | None = None
    
    def __post_init__(self) -> None:
        """
        Initialize has_shadow correctly and ensure correct monitor information
        
        Returns:
            None
        """
        if self.has_shadow is None:
            self.has_shadow = (self.opcode_type is OpcodeType.MENU)
        if self.can_have_monitor:
            assert self.monitor_id_behaviour is not None, repr(self)

        else:
            assert self.monitor_id_behaviour is None, repr(self)

    
    # Special Cases
    def add_special_case(self, special_case: SpecialCase) -> None:
        """
        Add special behaviour to a block opcode
        
        Args:
            special_case: The special behaviour to add
        
        Returns:
            None
        """
        self.special_cases[special_case.type] = special_case
    def get_special_case(self, case_type: SpecialCaseType) -> SpecialCase | None:
        """
        Get special behaviour by its SpecialCaseType
        
        Args:
            case_type: The kind of special case to look for
        
        Returns:
            the special case if exists
        """
        return self.special_cases.get(case_type, None)


    # Mutation Class
    def set_mutation_class(self, old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        """
        Blocks with some opcodes store additional information. For that purpose a mutation class can be added
        
        Args:
            old_cls: the mutation class to use in first representation
            new_cls: the mutation class to use in second representation
        
        Returns:
            None
        """
        self.old_mutation_cls = old_cls
        self.new_mutation_cls = new_cls


    # Info by Old Id
    def get_input_info_by_old(self, old: str) -> InputInfo:
        """
        Get information about an input by its old id
        
        Args:
            old: the old input id
        
        Returns:
            the input information
        """
        raise DeprecationWarning()
        return self.inputs.get_by_key1(old)
    def get_dropdown_info_by_old(self, old: str) -> DropdownInfo:
        """
        Get information about an dropdown by its old id
        
        Args:
            old: the old dropdown id
        
        Returns:
            the dropdown information
        """
        return self.dropdowns.get_by_key1(old)
    
    
    # Info by New Id
    def get_input_info_by_new(self, new: str, block: "SRBlock") -> InputInfo:
        """
        # TODO: ensure works
        # TODO: make parallell methods work; possibly allow for FRBlock and IRBlock as well
        Get information about an input by its new id
        
        Args:
            new: the new input id
        
        Returns:
            the input information
        """
        raise DeprecationWarning()
        return self.inputs.get_by_key2(new)
    def get_dropdown_info_by_new(self, new: str) -> DropdownInfo:
        """
        Get information about an dropdown by its new id
        
        Args:
            new: the new dropdown id
        
        Returns:
            the dropdown information
        """
        return self.dropdowns.get_by_key2(new)


    # Old Id -> New Id
    def get_new_input_id(self, old: str) -> str:
        """
        Get the new input id by its old id
        
        Args:
            old: the old input id
        
        Returns:
            the new input id
        """
        return self.inputs.get_key2_for_key1(old)
    def get_new_dropdown_id(self, old: str) -> str:
        """
        Get the new dropdown id by its old id
        
        Args:
            old: the old dropdown id
        
        Returns:
            the new dropdown id
        """
        return self.dropdowns.get_key2_for_key1(old)
    
    
    # New Id -> Old Id
    def get_old_input_id(self, new: str) -> str:
        """
        Get the old input id by its new id
        
        Args:
            new: the new input id
        
        Returns:
            the old input id
        """
        return self.inputs.get_key1_for_key2(new)
    def get_old_dropdown_id(self, new: str) -> str:
        """
        Get the old dropdown id by its new id
        
        Args:
            new: the new input id
        
        Returns:
            the old dropdown id
        """
        return self.dropdowns.get_key1_for_key2(new)
    
    
    # Fetching all ids
    def get_all_new_input_ids(self) -> list[str]:
        """
        Get all new input ids
        
        Returns:
            all new input ids
        """
        return list(self.inputs.keys_key2())
    def get_all_new_dropdown_ids(self) -> list[str]:
        """
        Get all new dropdown ids
        
        Returns:
            all new dropdown ids
        """
        return list(self.dropdowns.keys_key2())



    ##############################################################
    #               Methods based on Special Cases               #
    ##############################################################
    
    # Get the opcode type. Avoid OpcodeType.DYNAMIC
    def get_opcode_type(self, block: "IRBlock|SRBlock", validation_if: "ValidationIF") -> OpcodeType: # TODO: docs
        instead_case = self.get_special_case(SpecialCaseType.GET_OPCODE_TYPE)
        if self.opcode_type == OpcodeType.DYNAMIC:
            assert instead_case is not None, "If opcode_type is DYNAMIC, a special case with type GET_OPCODE_TYPE must be defined"
            return instead_case.call(block=block, validation_if=validation_if)
        else:
            assert instead_case is None, "If opcode_type is not DYNAMIC, no special case with type GET_OPCODE_TYPE should be defined"
            return self.opcode_type
    
    # Get input ids, info, types, modes
    def get_input_ids_infos(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> DualKeyDict[str, str, InputInfo]:
        """
        Get all the old and new inputs ids and their input information
        
        Args:
            block: needed as context to determine the ids and information e.g. for Custom Blocks
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            DualKeyDict mapping old input id and new input id to input information
        """
        instead_case = self.get_special_case(SpecialCaseType.GET_ALL_INPUT_IDS_INFO)
        if instead_case is None:
            return self.inputs
        else:
            return instead_case.call(block=block, fti_if=fti_if)

    def get_old_input_ids_infos(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, InputInfo]: # currently unused
        """
        Get all the old inputs ids and their input information
        
        Args:
            block: needed as context to determine the ids and information e.g. for Custom Blocks
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping old input id to input information
        """
        return dict(self.get_input_ids_infos(block, fti_if).items_key1())

    def get_new_input_ids_infos(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, InputInfo]:
        """
        Get all the new inputs ids and their input information
        
        Args:
            block: needed as context to determine the ids and information e.g. for Custom Blocks
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping new input id to input information
        """
        return dict(self.get_input_ids_infos(block, fti_if).items_key2())
    
    def get_old_new_input_ids(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, str]:
        """
        Get all the old and new input ids
        
        Args:
            block: needed as context to determine the ids and information e.g. for Custom Blocks
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping old input id to new input id
        """
        return dict(self.get_input_ids_infos(block, fti_if).keys_key1_key2())
    
    def get_new_old_input_ids(self, 
        block: "FRBlock|IRBlock|SRBlock", fti_if: "FirstToInterIF|None",
    ) -> dict[str, str]:
        """
        Get all the new and old input ids
        
        Args:
            block: needed as context to determine the ids and information e.g. for Custom Blocks
            fti_if: only necessary if block is a FRBlock
        
        Returns:
            dict mapping new input id to old input id
        """
        return dict(self.get_input_ids_infos(block, fti_if).keys_key2_key1())
    

@grepr_dataclass(grepr_fields=["name", "opcode_info"])
class OpcodeInfoGroup:
    """
    Represents a group of block opcode information. 
    Therefore it's used to represent opcode information about categories and extensions
    """

    name: str
    opcode_info: DualKeyDict[str, str, OpcodeInfo]

    def add_opcode(self, old_opcode: str, new_opcode: str, opcode_info: OpcodeInfo) -> None:
        """
        Add an opcode to a OpcodeInfoGroup with information about it
        
        Args:
            old_opcode: the old opcode referencing opcode_info
            new_opcode: the new opcode referencing opcode_info
            opcode_info: the information about that opcode, which will be fetchable by old_opcode or new_opcode
        
        Returns:
            None
        """
        self.opcode_info.set(
            key1  = old_opcode, 
            key2  = new_opcode, 
            value = opcode_info,
        )

@grepr_dataclass(grepr_fields=["opcode_info"])
class OpcodeInfoAPI:
    """
    API which provides a way to fetch information about block opcodes
    """

    opcode_info: DualKeyDict[str, str, OpcodeInfo] = field(default_factory=DualKeyDict)

    # Add Special Cases
    def add_opcode_case(self, old_opcode: str, special_case: SpecialCase) -> None:
        """
        Add a special case to the information about an opcode
        
        Args:
            old_opcode: the old opcode referencing the target opcode information
            special_case: the special behaviour to add
        
        Returns:
            None
        """
        assert isinstance(old_opcode, str)
        opcode_info = self.get_info_by_old(old_opcode)
        opcode_info.add_special_case(special_case)
    
    def add_opcodes_case(self, old_opcodes: Iterable[str], special_case: SpecialCase) -> None:
        """
        Add a special case to the information about multiple opcodes
        
        Args:
            old_opcodes: the old opcodes referencing the target opcode information
            special_case: the special behaviour to add
        
        Returns:
            None
        """
        assert isinstance(old_opcodes, set)
        for old_opcode in old_opcodes:
            self.add_opcode_case(old_opcode, special_case)

    # Set Mutation Classes
    def set_opcode_mutation_class(self, old_opcode: str, old_cls: Type["FRMutation"], new_cls: Type["SRMutation"]) -> None:
        """
        Blocks with some opcodes store additional information. 
        For that purpose a mutation class can be added to a given opcode
        
        Args:
            old_opcodes: the old opcodes referencing the target opcode information
            old_cls: the mutation class to use in first representation
            new_cls: the mutation class to use in second representation            
        
        Returns:
            None
        """
        assert isinstance(old_opcode, str)
        opcode_info = self.get_info_by_old(old_opcode)
        opcode_info.set_mutation_class(old_cls=old_cls, new_cls=new_cls)
    
    def set_opcodes_mutation_class(self, 
        old_opcodes: Iterable[str], 
        old_cls: Type["FRMutation"], 
        new_cls: Type["SRMutation"],
    ) -> None:
        """
        Blocks with some opcodes store additional information. 
        For that purpose a mutation class can be added to the given opcodes
        
        Args:
            old_opcodes: the old opcodes referencing the target opcode information
            old_cls: the mutation class to use in first representation
            new_cls: the mutation class to use in second representation            
        
        Returns:
            None
        """
        assert isinstance(old_opcodes, set)
        for old_opcode in old_opcodes:
            self.set_opcode_mutation_class(old_opcode, old_cls=old_cls, new_cls=new_cls)

    # Add Categories/Extensions
    def add_group(self, group: OpcodeInfoGroup) -> None:
        """
        Add a category or extension to the API
        
        Args:
            group: the category or extension
        """
        for old_opcode, new_opcode, opcode_info in group.opcode_info.items_key1_key2():
            if self.opcode_info.has_key1(old_opcode) or self.opcode_info.has_key2(new_opcode):
                raise MANIP_SameOpcodeTwiceError(f"Must not add opcode {(old_opcode, new_opcode)!r} twice")
            self.opcode_info.set(
                key1  = old_opcode,
                key2  = new_opcode,
                value = opcode_info,
            )
    
    @enforce_argument_types
    def add_extension(self, extension_ref: ExtensionRef) -> None:
        """
        Add an extension to the API
        
        Args:
            extension_ref: the reference to the extension

        Raises:
            MANIP_ExtensionModuleNotFoundError: If the extension's python module does not exist
            MANIP_UnexpectedExtensionModuleImportError: If the extension's python module can not be loaded e.g. because it is malformed
        """
        module_path = path.join(extension_ref.module_dir, f"{extension_ref.id}.py")
        # Validate file existence
        if not file_exists(module_path):
            raise MANIP_ExtensionModuleNotFoundError(f"Python module of extension {extension_ref!r} was not found. Did you forget to generate it?")
    
        # Generate a unique module name to avoid clashes in sys.modules
        module_name = f"_dynamic_module_{extension_ref.id}"
    
        try:
            spec = importutil.spec_from_file_location(module_name, module_path)
            if spec is None or spec.loader is None:
                raise MANIP_UnexpectedExtensionModuleImportError(
                    f"Can not create spec for python module of extension {extension_ref!r}"
                )
    
            module = importutil.module_from_spec(spec)
            sys_modules[module_name] = module  # Required so relative imports work
    
            spec.loader.exec_module(module)
        except (SyntaxError, ImportError, OSError, Exception) as error:
            raise MANIP_UnexpectedExtensionModuleImportError(
                f"Unexpected error importing python module of extension {extension_ref!r}: {error}. "
                 "Please try deleting cache and regenerating it or create a GitHub issue"
            ) from error
    
        try:
            group = getattr(module, f"ext_{extension_ref.id}")
        except AttributeError as error:
            raise MANIP_UnexpectedExtensionModuleImportError(
                f"Python module of extension {extension_ref!r} is malformed. "
                 "Please try deleting cache and regenerating it or create a GitHub issue"
            ) from error
        
        self.add_group(group)    
   
    def _add_all_extensions_of_project(self, custom_ext_id_to_source: dict[str, str], builtin_ext_ids: list[str]) -> None:
        """
        For every extension of a project generate and import the required opcode info py file.
        If cached versions exist and they are up to date, they will be kept and not replaced
        
        Args:
            custom_ext_id_to_source: maps custom extension id to extension source(probably a URL) of the project
            builtin_ext_ids: the builtin extensions of the project
        
        Raises:
            MANIP_UnknownBuiltinExtensionError: if one tries to add an unknown or not yet implemented builtin extension
            MANIP_ExtensionModuleNotFoundError: If the extension's python module does not exist
            MANIP_UnexpectedExtensionModuleImportError: If the extension's python module can not be loaded e.g. because it is malformed
            MANIP_NoNodeJSInstalledError: if Node.js is not installed or not found in PATH
            MANIP_ExtensionFetchError: if the extension code could not be fetched for some reason
            MANIP_DirectExtensionInfoExtractionError: if the extension info could not be extracted through direct execution
            MANIP_SafeExtensionInfoExtractionError: if the extension info could not be extracted through safe analysis
            MANIP_ExtensionInfoConvertionError: if the extracted extension info could not be converted into the format of this project
            MANIP_ThanksError(unlikely): if a block argument uses the mysterious Scratch.ArgumentType.SEPERATOR
            MANIP_FailedFileWriteError(unlikely): if the generated extension info file or cache file or their directory could not be written/created
    
        Warnings:
            MANIP_UnexpectedPropertyAccessWarning: if a property of 'this' is accessed in the getInfo method of the extension code in safe analysis
            MANIP_UnexpectedNotPossibleFeatureWarning: if an impossible to implement feature is used (eg. ternary expr) in the getInfo method of the extension code in safe analysis
        """
        from pmp_manip.ext_info_gen import generate_extension_info_py_file
                
        for builtin_ext_id in builtin_ext_ids:
            if not hasattr(BuiltinExtensionRef, builtin_ext_id):
                raise MANIP_UnknownBuiltinExtensionError(f"Unknown or not (yet) implemented builtin extension: {builtin_ext_id}")
            extension_ref = getattr(BuiltinExtensionRef, builtin_ext_id)
            self.add_extension(extension_ref)
        
        for custom_ext_id, extension_source in custom_ext_id_to_source.items():
            module_path = generate_extension_info_py_file(
                source=extension_source,  extension_id=custom_ext_id,
                tolerate_file_path=False, bundle_errors=True,
            )
            extension_ref = ExtensionRef(
                id         = custom_ext_id,
                module_dir = path.dirname(module_path),
            )
            self.add_extension(extension_ref)        
    
    # Get all opcodes
    @property
    def all_new(self) -> list[str]:
        """
        Get a list of all new opcodes
        
        Returns:
            a list of all new opcodes
        """
        return list(self.opcode_info.keys_key2())
    @property
    def all_old(self) -> list[str]:
        """
        Get a list of all old opcodes
        
        Returns:
            a list of all old opcodes
        """
        return list(self.opcode_info.keys_key1())
    
    
    # Get new opcode for old opcode
    def get_new_by_old_safe(self, old: str) -> str | None:
        """
        Safely get the new opcode for an old opcode, return None if the old opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the new opcode or None if the old opcode is unknown
        """
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_key2_for_key1(old)
        return None
    def get_new_by_old(self, old: str) -> str:
        """
        Get the new opcode for an old opcode, raise MANIP_UnknownOpcodeError if the old opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the new opcode
        """
        new = self.get_new_by_old_safe(old)
        if new is not None:
            return new
        raise MANIP_UnknownOpcodeError(f"Could not find new opcode for old opcode {old!r}")
    
    
    # Get old opcode for new opcode
    def get_old_by_new_safe(self, new: str) -> str:
        """
        Safely get the old opcode for an new opcode, return None if the new opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            new: the new opcode
        
        Returns:
            the old opcode or None if the new opcode is unknown
        """
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_key1_for_key2(new)
        return None
    def get_old_by_new(self, new: str) -> str:
        """
        Get the old opcode for an new opcode, raise MANIP_UnknownOpcodeError if the new opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            new: the new opcode
        
        Returns:
            the old opcode
        """
        old = self.get_old_by_new_safe(new)
        if old is not None:
            return old
        raise MANIP_UnknownOpcodeError(f"Could not find old opcode for new opcode {new!r}")
    
    
    # Fetching info by old opcode
    def get_info_by_old_safe(self, old: str) -> OpcodeInfo | None:
        """
        Safely get the opcode information by old opcode, return None if the old opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the opcode information or None if the old opcode is unknown
        """
        if self.opcode_info.has_key1(old):
            return self.opcode_info.get_by_key1(old)
        return None
    def get_info_by_old(self, old: str) -> OpcodeInfo:
        """
        Get the opcode infotamtion by old opcode, raise MANIP_UnknownOpcodeError if the old opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            old: the old opcode
        
        Returns:
            the opcode information
        """
        info = self.get_info_by_old_safe(old)
        if info is not None:
            return info
        raise MANIP_UnknownOpcodeError(f"Could not find OpcodeInfo by old opcode {old!r}. Have you possibly forgotten to add an extension?")
    
    
    # Fetching info by new opcode
    def get_info_by_new_safe(self, new: str) -> OpcodeInfo | None:
        """
        Safely get the opcode information by new opcode, return None if the new opcode is unknown.
        Use this one, if you want to handle the unknown case yourself
        
        Args:
            new the new opcode
        
        Returns:
            the opcode information or None if the new opcode is unknown
        """
        if self.opcode_info.has_key2(new):
            return self.opcode_info.get_by_key2(new)
        return None 
    def get_info_by_new(self, new: str) -> OpcodeInfo:
        """
        Get the opcode infotamtion by new opcode, raise MANIP_UnknownOpcodeError if the new opcode is unknown.
        Use this one, if you do NOT want to handle the unknown case yourself
        
        Args:
            new: the new opcode
        
        Returns:
            the opcode information
        """
        info = self.get_info_by_new_safe(new)
        if info is not None:
            return info
        raise MANIP_UnknownOpcodeError(f"Could not find OpcodeInfo by new opcode {new!r}")


__all__ = [
    "ExtensionRef", "BuiltinExtensionRef", 
    "OpcodeType", "MonitorIdBehaviour", "OpcodeInfo", "OpcodeInfoGroup", "OpcodeInfoAPI",
]

