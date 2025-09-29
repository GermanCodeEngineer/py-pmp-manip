# Getting Information on block opcodes in `pmp_manip`

You will likely want to get information on a kind of block when working with it.
This is what the **Opcode Documentation Generator** is for. 

---

## Using `get_opcode_doc(info_api: OpcodeInfoAPI, new_opcode: str)`

You can use `get_opcode_doc` to generated Markdown documentation for an opcode:
```python
from pmp_manip import init_config, get_default_config, info_api, generate_opcode_doc

init_config(get_default_config())

doc_string = generate_opcode_doc(info_api, new_opcode="&motion::glide (SECONDS) secs to ([TARGET])")
print(doc_string)
```
Output:
```
## Documentation for opcode `glide (SECONDS) secs to ([TARGET])`(motion)
### Block Shape
* [**STATEMENT**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#STATEMENT)
### Inputs
* `SECONDS`
    * type: **NUMBER**
    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)
* `TARGET`
    * type: **RANDOM_MOUSE_OR_OTHER_SPRITE**
    * SR-Class: [`SRBlockAndDropdownInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndDropdownInputValue)
    * possible values for `.dropdown`:
        * `SRDropdownValue(DropdownValueKind.OBJECT, 'random position')`
        * `SRDropdownValue(DropdownValueKind.OBJECT, 'mouse-pointer')`
### Dropdowns: /
### Mutation: /
### Monitor: /

```
You can write it to a file and use any tool(like VSCode) to display it:
```python
from pmp_manip import init_config, get_default_config, info_api, generate_opcode_doc

init_config(get_default_config())

doc_string = generate_opcode_doc(info_api, new_opcode="&motion::glide (SECONDS) secs to ([TARGET])")
with open("generated_doc.md", "w") as file:
    file.write(doc_string)
```
Displayed:

---

## Documentation for opcode `glide (SECONDS) secs to ([TARGET])`(motion)
### Block Shape
* [**STATEMENT**](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/block_shape.md#STATEMENT)
### Inputs
* `SECONDS`
    * type: **NUMBER**
    * SR-Class: [`SRBlockAndTextInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndTextInputValue)
* `TARGET`
    * type: **RANDOM_MOUSE_OR_OTHER_SPRITE**
    * SR-Class: [`SRBlockAndDropdownInputValue`](https://github.com/GermanCodeEngineer/py-pmp-manip/blob/main/docs/second_repr.md#SRBlockAndDropdownInputValue)
    * possible values for `.dropdown`:
        * `SRDropdownValue(DropdownValueKind.OBJECT, 'random position')`
        * `SRDropdownValue(DropdownValueKind.OBJECT, 'mouse-pointer')`
### Dropdowns: /
### Mutation: /
### Monitor: /

---

Note: It can also be used for block opcodes from extensions after adding them to `info_api`(read [docs/handling_extensions.md](handling_extensions.md))

## Searching for opcodes

Opcodes of almost all blocks are based on their name in the PenguinMod Editor. Just the inputs and dropdowns(ALLCAPS) were added.
Let us say you want to get information for this block or are trying to find out its opcode:
![](images/doc_api_searched_opcode.jpg)
If an opcode is not found, `generate_opcode_doc` will show the closest matches. We know it is from the `sensing` category and contains the words "touching clone of":
```python
from pmp_manip import init_config, get_default_config, info_api, generate_opcode_doc

init_config(get_default_config())

# Just input everything you know and you will likely find it:
doc_string = generate_opcode_doc(info_api, new_opcode="&sensing::touching clone of")
```
Output(without traceback):
```
pmp_manip.utility.errors.MANIP_UnknownOpcodeError: Unknown new opcode '&sensing::touching clone of'. Did you forget to add an extension? The closest matches are:
  - '&sensing::touching color (COLOR) ?'
  - '&sensing::([OBJECT]) touching clone of ([SPRITE]) ?'
  - '&sensing::touching ([OBJECT]) ?'
  - '&sensing::mouse x'
  - '&sensing::mouse y'
  - '&sensing::mobile?'
  - '&sensing::mouse clicked?'
  - '&sensing::mouse down?'
  - '&sensing::loudness'
  - '&sensing::timer'
```

Yes! The second entry is what we are looking for: `"&sensing::([OBJECT]) touching clone of ([SPRITE]) ?"`
Now we can call `generate_opcode_doc` again with the real opcode and get our desired documentation.

---

This is the end of the tutorial. Try using `pmp_manip`. Be courageous. Ask questions, create issues, contribute if you want. I look forward to that :)

### References
* For a **documentation overview** and **all pages** of the tutorial, see [docs/index.md](index.md)
* For **more information on blocks, scripts and Second Representation**, see [docs/second_repr.md](second_repr.md)
