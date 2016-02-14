#!/usr/bin/env python2.7

from generation import *
from isa_8051 import *


def test():
    ops = {
        '@R0': [R0],
        '@R1': [R1],
        'R0': R0,
        'R1': R1,
        'R2': R2,
        'R3': R3,
        'R4': R4,
        'R5': R5,
        'R6': R6,
        'R7': R7,
        'A': A,
        'direct': [0xd],
        'bit': Bit(1),
        '/bit': BitNot(2),
        'offset': Destination(0xde),
        '#immed': 0xff,
        '@A+DPTR': [A + DPTR],
        '@A+PC': [A + PC],
        'DPTR': DPTR,
        'C': C,
        'AB': AB,
        '@DPTR': [DPTR],
    }

    with open('8051.txt') as f:
        for l in f.readlines():
            if l.startswith(';') or 'reserved' in l or\
                'addr11' in l or 'addr16' in l:
                continue

            values = l.split()
            opcode = int(values[0], 16)
            size = int(values[1])
            mnemonic = values[2]
            operands = values[3:]

            operands = map(ops.get, operands)
            cls = globals()[mnemonic.lower()]
            i = cls(*operands)

            raw = str(i)
            if ord(raw[0]) != opcode:
                print map(lambda x: hex(ord(x)), raw)
                print 'Mismatch at %02x.' % opcode
                return False

        print 'Done.'
        return True


def main():
    test()


if __name__ == '__main__':
    main()
