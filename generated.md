## Documentation for opcode `{{EXPANDABLE IF-THEN-ELSE CHAIN}}`(control)
### Block Shape
* **STATEMENT**
### Inputs
Depends on how many branches the block has. format of keys: `CONDITION1`...`CONDITIONn`, `THEN1`...`THENn`, `ELSE` if it has an else branch
* `CONDITION1`...`CONDITIONn`
    * type: **BOOLEAN**
    * SR-Class: [`SRBlockAndBoolInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndBoolInputValue)
* `THEN1`...`THENn`
    * type: **SCRIPT**
    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)
* (`ELSE`)
    * type: **SCRIPT**
    * SR-Class: [`SRScriptInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRScriptInputValue)
### Dropdowns: /
### Mutation
An instance of [`SRExpandableIfMutation`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRExpandableIfMutation).
### Monitor: /
