from blocks import Blocks

if __name__ == "__main__":
    print(Blocks["Init"].spawn())
    print(Blocks["Calc"].spawn(pick="add"))
    print(Blocks["Calc"].spawn(reg="vt", repeat="20"))
    print(Blocks["Beq"].spawn(Blocks["Calc"].spawn(reg="v")))
    print(Blocks["Procedure"].spawn(Blocks["Calc"].spawn(reg="v")))
    print(Blocks["Endless"].spawn())
    print(Blocks["SwLw"].spawn(repeat="2"))
