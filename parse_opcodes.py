#!/usr/bin/env python2.7

from collections import defaultdict


OPERANDS = {
    #'addr11': 'Destination',
    'addr16': 'Destination',
    'offset': 'Destination',
    'A': 'SpecialAccumulator',
    'C': 'CarryFlag',
    'AB': 'SpecialAB',
    'direct': 'Indirection',
    '@R0': 'IndirectionRegister',
    'bit': 'Bit',
    '/bit': 'BitNot',
    'DPTR': 'SpecialDptr',
    '@DPTR': 'IndirectionDptr',
    '#immed': 'Immediate',
    '@A+DPTR': 'IndirectionAccDptr',
    '@A+PC': 'IndirectionAccPc',
    'R0': 'Register'
}


def parse():
    instructions = defaultdict(list)
    with open('8051.txt') as f:
        for l in f.readlines():
            if l.startswith(';') or 'reserved' in l or\
                any(x in l for x in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6',
                    'R7')) or '@R1' in l or 'addr11' in l:
                continue

            values = l.split()
            opcode = int(values[0], 16)
            size = int(values[1])
            mnemonic = values[2]
            operands = values[3:]

            instructions[mnemonic.lower()].append((opcode, size,
                map(OPERANDS.get, operands)))

    for mnemonic, encoding in instructions.iteritems():
        template = 'class %s(Instruction):\n\t_encoding_ = [\n' % mnemonic
        for opcode, size, operands in encoding:
            ops = ', '.join(operands)
            if not ops:
                ops = 'None'
            else:
                ops = '(%s,)' % ops

            template += '\t\t(0x%02x, %d, %s),' % (opcode, size, ops)
            template += '\n'

        template += '\t]\n'
        print template


def main():
    parse()


if __name__ == '__main__':
    main()
