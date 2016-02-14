
from arch.lib8051.decutils import ImmediateOperand8, ImmediateOperand16


class Label(object):
    def __init__(self, label=0):
        self._label = label
        self._base = 0

    def __repr__(self):
        return '__lbl_%s' % str(self.label)

    @property
    def label(self):
        if isinstance(self._label, str):
            label = self._label
        else:
            label = self._base + self._label
        return label


class Immediate(object):
    def __init__(self, immediate, size=0):
        if isinstance(immediate, (ImmediateOperand8, ImmediateOperand16)):
            immediate = immediate.constant

        self._value = immediate
        if size:
            self._size = size
            if immediate >= 2**size:
                raise ValueError('Immediate out of bounds (%d, size %d)' %
                    (immediate, size))
        else:
            if immediate < 2**8:
                self._size = 8
            elif immediate < 2**16:
                self._size = 16
            else:
                raise ValueError('No bounds given for immediate, but '\
                    ' immediate is larger than 2^16.')

    def __repr__(self):
        return '#%xh' % self._value

    @property
    def value(self):
        return self._value

    @property
    def size(self):
        return self._size


class Destination(Immediate):
    def __init__(self, destination):
        super(Destination, self).__init__(destination)

    def __repr__(self):
        return 'off_%x' % self._value


class Register(object):
    def __init__(self, index):
        assert 0 <= index <= 7
        self._index = index

    def __repr__(self):
        return 'R%d' % self._index

    @property
    def index(self):
        return self._index


class InternalAccPc(object):
    pass


class InternalAccDptr(object):
    pass


class SpecialAccumulator(object):
    def __repr__(self):
        return 'A'

    def __add__(self, other):
        if type(other) is SpecialPc:
            return InternalAccPc()
        if type(other) is SpecialDptr:
            return InternalAccDptr()
        return self

    def __radd__(self, other):
        return self + other


class SpecialDptr(object):
    def __repr__(self):
        return 'DPTR'

    def __add__(self, other):
        if type(other) is SpecialAccumulator:
            return InternalAccDptr()
        return self

    def __radd__(self, other):
        return self + other


class SpecialAB(object):
    def __repr__(self):
        return 'AB'


class SpecialPc(object):
    def __repr__(self):
        return 'PC'

    def __add__(self, other):
        if type(other) is SpecialAccumulator:
            return InternalAccPc()
        return self

    def __radd__(self, other):
        return self + other


class CarryFlag(object):
    def __repr__(self):
        return 'C'


class Bit(object):
    def __init__(self, bit):
        self._bit = bit

    @property
    def is_negated(self):
        return self._bit < 0

    @property
    def value(self):
        return abs(self._bit)

    def __repr__(self):
        return '%xh' % self._bit


class BitNot(Bit):
    def __init__(self, bit):
        super(BitNot, self).__init__(-bit)

    def __repr__(self):
        return '/' + super(BitNot, self).__repr__()


class Indirection(Immediate):
    def __init__(self, direct):
        super(Indirection, self).__init__(direct)

    def __repr__(self):
        return '%x' % self._value


class IndirectionRegister(Register):
    def __init__(self, register):
        super(IndirectionRegister, self).__init__(register)
        if self._index > 1:
            raise ValueError('Register index out of bounds for indirection.')

    def __repr__(self):
        return '@' + super(IndirectionRegister, self).__repr__()


class IndirectionDptr(object):
    def __repr__(self):
        return '@DPTR'


class IndirectionAccPc(object):
    def __repr__(self):
        return '@A + PC'


class IndirectionAccDptr(object):
    def __repr__(self):
        return '@A + DPTR'


A = SpecialAccumulator()
AB = SpecialAB()
DPTR = SpecialDptr()
C = CarryFlag()
PC = SpecialPc()

for i in range(7 + 1):
    globals()['R%d' % i] = Register(i)


class TagRelativeOffset:
    pass


class TagDirect11:
    pass


class TagDirect16:
    pass
