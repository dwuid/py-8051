
import struct
import inspect
import binascii

from isa51_types import *
from ctypes import c_uint8


_VALID_OPERANDS = frozenset([int, long, Immediate, Destination, Register,\
    SpecialAccumulator, SpecialDptr, SpecialAB, CarryFlag, Bit, BitNot,\
    Indirection, IndirectionRegister, IndirectionDptr, IndirectionAccPc,\
    IndirectionAccDptr, Label])

_EQUIVALENT_TYPES = dict(zip(_VALID_OPERANDS, _VALID_OPERANDS))
_EQUIVALENT_TYPES.update({
    Label: Destination,
    long: Immediate,
    int: Immediate
})


def _pack_arbitrary(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


class BaseInstruction(object):
    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def assemble(self, base=0):
        return str(self)

    def resolve_labels(self, labels=None):
        raise NotImplementedError()


class Data(BaseInstruction):
    _encoding_ = None

    def __init__(self, raw_data, base=0):
        if isinstance(raw_data, (int, long)):
            raw_data = _pack_arbitrary(raw_data)

        self._raw_data = raw_data
        self._base = base

    def __repr__(self):
        if isinstance(self._raw_data, Label):
            return 'db %s' % str(self._raw_data)
        return 'db ' + ', '.join(map(lambda x: '0x%02x' % ord(x),
                                     str(self._raw_data)))

    def __len__(self):
        if isinstance(self._raw_data, Label):
            # TODO: Cpu8051.LabelSize <- 2 [?]
            return 2
        return len(str(self))

    def __str__(self):
        return str(self._raw_data)

    def __add__(self, other):
        # TODO: Bail out on add to Label?
        return Data(self._raw_data + str(other))

    def __radd__(self, other):
        return Data(str(other) + self._raw_data)

    def resolve_labels(self, labels=None):
        if not labels:
            labels = {}

        if isinstance(self._raw_data, Label):
            if not self._raw_data.label in labels:
                raise ValueError('Cannot resolve unresolved label.')
            self._raw_data = _pack_arbitrary(labels[self._raw_data.label])


class Instruction(BaseInstruction):
    _encoding_ = None

    def __init__(self, operand0=None, operand1=None, operand2=None):
        def sanitize(operand):
            if inspect.isclass(operand):
                operand = operand()

            if isinstance(operand, list):
                if len(operand) != 1:
                    raise ValueError('Invalid number of elements in'\
                        ' indirection.')

                operand = sanitize(operand[0])
                if type(operand) is InternalAccPc:
                    operand = IndirectionAccPc()
                elif type(operand) is InternalAccDptr:
                    operand = IndirectionAccDptr()
                elif type(operand) is SpecialDptr:
                    operand = IndirectionDptr()
                elif type(operand) is Register:
                    operand = IndirectionRegister(operand.index)
                elif type(operand) is Immediate:
                    operand = Indirection(operand.value)
                return operand

            return operand if not isinstance(operand, (int, long,
                ImmediateOperand8, ImmediateOperand16)) else Immediate(operand)

        self._operands = map(sanitize, (operand0, operand1, operand2))
        self._operands = filter(lambda x: x, self._operands)

        if not all(type(o) in _VALID_OPERANDS for o in self._operands):
            raise ValueError('Not all operands are valid for given'\
                ' instruction.')

    def __repr__(self):
        operands = filter(lambda x: x, self._operands)
        return self.name + ' ' + ', '.join(repr(o) for o in operands) + ' '

    def _find_encoding(self):
        for opcode, size, operands in self._encoding_:
            if len(self._operands) == 0 and not operands:
                return (opcode, size, operands)

            if len(operands) != len(self._operands):
                continue

            encoding_types = list(operands)
            given_types = map(type, self._operands)

            def compare_types(types):
                lhs, rhs = types
                return _EQUIVALENT_TYPES[lhs] == _EQUIVALENT_TYPES[rhs]

            if all(map(compare_types, zip(encoding_types, given_types))):
                return (opcode, size, operands)
        return None

    def resolve_labels(self, labels=None):
        if not labels:
            labels = {}

        resolved_operands = []
        for i, operand in enumerate(self._operands):
            if isinstance(operand, Label):
                if isinstance(operand.label, str):
                    operand = Destination(labels[operand.label])
            resolved_operands.append(operand)

        self._operands = resolved_operands

    def __len__(self):
        encoding = self._find_encoding()
        assert encoding, 'Cannot find encoding for instruction.'

        _, size, _ = encoding
        return size

    def __str__(self):
        return self.assemble()

    def assemble(self, base=0):
        encoding = self._find_encoding()
        if not encoding:
            raise ValueError('No valid encoding has been found for current'\
                ' instruction.')

        def stringify(l):
            return ''.join([chr(c_uint8(x).value) for x in l])

        opcode, size, _ = encoding
        bytes = [0,] * size
        bytes[0] = opcode

        if isinstance(self, TagDirect16):
            o = self._operands[0]
            bytes[1] = (o.value >> 8) & 0xff
            bytes[2] = o.value & 0xff
            return stringify(bytes)

        if isinstance(self, TagDirect11):
            o = self._operands[0]
            upper = o.value & (0b111 << 5)

            bytes[0] |= upper
            bytes[1] = o.value & 0xff
            return stringify(bytes)

        i = 0
        for o in self._operands:
            if type(o) is IndirectionRegister:
                bytes[0] |= o.index
                i += 1

            elif type(o) is Immediate:
                bytes[i] = o.value & 0xff
                i += 1

            elif type(o) is Register:
                bytes[0] |= (bytes[0] & ~0b111) | o.index
                i += 1

            elif type(o) in (Indirection, Bit, BitNot, Destination):
                if not i: i += 1
                value = o.value

                if isinstance(self, TagRelativeOffset):
                    value = value - base - size

                bytes[i] = value
                i += 1

            elif type(o) in (SpecialAccumulator, SpecialDptr, SpecialAB,
                CarryFlag, IndirectionDptr, IndirectionAccPc,
                IndirectionAccDptr):
                i += 1

            else:
                raise ValueError('Encountered invalid operand when encoding.')
        return stringify(bytes)
