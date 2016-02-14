
import inspect
from isa51_types import *
from isa51_instruction import *


class Block:
    _identifier = 0
    LABEL_PREFIX= 'internal_label_'

    def __init__(self, *arguments):
        self._list = []
        Block._identifier += 1
        map(self.append, arguments)

    @staticmethod
    def build_label(address):
        return Label(Block.LABEL_PREFIX + '%04x' % address)

    @staticmethod
    def extract_address(label):
        # TODO: Maybe explicitly accept type 'InternalLabel'?

        l = label.label
        if l.startswith(Block.LABEL_PREFIX):
            return int(l[len(Block.LABEL_PREFIX):], 16)
        return None

    def resolve_labels(self, base=0):
        labels = {}
        offset = base

        for i, instruction in enumerate(self._list):
            if inspect.isclass(instruction):
                instruction = instruction()
                self._list[i] = instruction

            if isinstance(instruction, Label):
                # -- DEBUG
                #print 'Resolved %s to %04x.' % (instruction.label, offset)
                labels[instruction.label] = offset
                continue

            if isinstance(instruction, BaseInstruction):
                offset += len(instruction)
        return labels

    def _externalize_labels(self, known_labels, all_labels):
        for l in all_labels:
            if not isinstance(l, Label):
                continue

            internal = self.extract_address(l)
            if not internal:
                continue

            if not l.label in known_labels:
                known_labels[l.label] = internal
        return known_labels

    def assemble(self, base=0, labels=None, externalize_labels=False):
        if not labels:
            labels = self.resolve_labels(base=base)
            if externalize_labels:
                labels = self._externalize_labels(labels, labels)

        raw, offset = '', base
        for instruction in self._list:
            if isinstance(instruction, BaseInstruction):
                instruction.resolve_labels(labels)
                current = instruction.assemble(offset)

                raw += current
                offset += len(current)
        return raw

    def append(self, other):
        if isinstance(other, (list, tuple)):
            map(self.append, other)

        elif isinstance(other, Block):
            map(self.append, other._list)

        else:
            self._list.append(None)
            self[-1] = other
        return self

    def __repr__(self):
        return '\n'.join(repr(i) for i in self._list)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._list.__getitem__[key]
        return self._list[key]

    def __setitem__(self, key, other):
        if isinstance(key, slice):
            del self._list[key]

            insert = [None]
            if isinstance(other, Block):
                insert *= len(other)

            self._list[key.start:key.start] = insert
            self[key.start] = other
            return self

        _ = self._list[key]
        if inspect.isclass(other):
            other = other()

        if isinstance(other, Block):
            for i, instruction in enumerate(other):
                self[key + i] = instruction
        else:
            self._list[key] = other
        return self

    def __iadd__(self, other):
        self.append(other)
        return self

    def __add__(self, other):
        return Block(self, other)

    def __radd__(self, other):
        return Block(other, self)

    def __iter__(self):
        return iter(self._list)
