camel_names = ["name", "assetId", "dataFormat", "md5ext", "rotationCenterX", "rotationCenterY", "bitmapResolution"]

var = "data"

snake_names = []
for name in camel_names:
    for letter in "abcdefghijklmnopqrstuvwxyz":
        name = name.replace(letter.upper(), "_" + letter)
    snake_names.append(name)




print(repr(snake_names).replace("'", '"'))
max_camel_length = max([len(item) for item in camel_names])
max_snake_length = max([len(item) for item in snake_names])

new_camel_names = ['"' + item + '"' + (" " * (max_camel_length-len(item))) for item in camel_names.copy()]
new_snake_names = [      item       + (" " * (max_snake_length-len(item))) for item in snake_names.copy()]

string = ""
for camel_name, snake_name in zip(new_camel_names, new_snake_names):
    string += f"\tself.{snake_name} = {var}[{camel_name}] \n"
print(string)
