# Shapes of Blocks in `pmp_manip`

### STATEMENT
Example: `"&variables::change [VARIABLE] by (VALUE)"`<br>
![](images/block_shape/STATEMENT.jpg)
### ENDING_STATEMENT
Example: `"&control::delete this clone"`<br>
![](images/block_shape/ENDING_STATEMENT.jpg)
### HAT
Example: `"&events::when green flag clicked"`<br>
![](images/block_shape/HAT.jpg)

### STRING_REPORTER
Example: `"&operators::join (STRING1) (STRING2)"`<br>
![](images/block_shape/STRING_REPORTER.jpg)
### NUMBER_REPORTER
Example: `"&sensing::distance from (X1) (Y1) to (X2) (Y2)"`<br>
![](images/block_shape/NUMBER_REPORTER.jpg)
### BOOLEAN_REPORTER
Example: `"&sensing::key ([KEY]) pressed?"`<br>
![](images/block_shape/BOOLEAN_REPORTER.jpg)

### DYNAMIC
Used for blocks, which can change shape depending on e.g. dropdown values or other blocks.
Can only become one of the above.<br>
Example: `"&customblocks::call custom block"` and `"&control::stop script [TARGET]"`<br>
![](images/block_shape/DYNAMIC.jpg)

### EMBEDDED
Used only for blocks, which can not exist on their own. The only current use case is the deprecated polygon menu in the pen extension.
### MENU
Used in first representation in some block dropdowns to store a single value. Blocks of this shape never exist in second representation.
### NOT_RELEVANT
Used in first representation in boolean inputs and custom block definitions. Blocks of this shape never exist in second representation.

---

### References
* For a **documentation overview** and a **broader usage tutorial**, see [docs/index.md](index.md)

