import abc
import uuid
import random


class BlockBase:
    """
        The abstract base class for all blocks
    """

    @staticmethod
    def label() -> str:
        return "label_" + uuid.uuid1(node=0x7F000001).hex

    @staticmethod
    def imm(*, low, high) -> str:
        return str(random.randint(low, high))

    @staticmethod
    def shamt() -> str:
        return BlockBase.imm(low=0, high=31)

    @staticmethod
    def imm16() -> str:
        return BlockBase.imm(low=0, high=65535)

    @staticmethod
    def imm26() -> str:
        return BlockBase.imm(low=0, high=67108863)

    @staticmethod
    def reg(field="vats0") -> str:
        if field == '*':
            return random.choice([f"${i}" for i in range(32)])
        allowed = []
        if 'v' in field:
            allowed.extend([f"$v{i}" for i in range(2)])
        if 'a' in field:
            allowed.extend([f"$a{i}" for i in range(4)])
        if 't' in field:
            allowed.extend([f"$t{i}" for i in range(10)])
        if 's' in field:
            allowed.extend([f"$s{i}" for i in range(8)])
        if '0' in field:
            allowed.extend(["$zero"])
        return random.choice(allowed) if allowed else ""

    @abc.abstractmethod
    def spawn(self, *args, **kwargs):
        pass
