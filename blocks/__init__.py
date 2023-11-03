from importlib import import_module
from os import listdir


# Wildcard all the Block modules
# I cannot find a better method to do this except walking the folder
__block_list = [
    ".".join(s.split('.')[0:-1])
    for s in listdir("blocks") if s.endswith(".py") and s != "__init__.py" and s != "BlockBase.py"
]

# Dump dict to the caller
# Like: {"Beq": <Object>}
# So why there are `instance()` method in each module file?
# To simplify the `import` and `call` procedures
Blocks = dict(
    [(name, import_module(f"{__package__}.{name}").instance()) for name in __block_list]
)
