#!/usr/bin/env python2


from arch.lib8051 import Arch8051
from arch.lib8051.decutils import *
from arch.lib8051.opcode_8051 import decode

from intelhex import IntelHex
from collections import defaultdict

from isa51_assembler import *
from isa_8051 import *

import os


TARGET = 'sample/main.ihx'
RESULT = 'sample/output.ihx'
TEST   = 'sample/test.ihx'
MAX_INSTRUCTION = Arch8051.maxInsnLength

FUNC_START = 0x0fb


class DecodedInstruction(object):
    def __init__(self, mnemonic, operands, length, ip):
        self._mnemonic, self._operands = mnemonic, operands
        self._length, self._ip = length, ip

    def __str__(self):
        result = '%04x %s' % (self._ip, self._mnemonic)
        for o in self._operands:
            result += ' ' + str(o)
        return result

    @property
    def ip(self):
        return self._ip

    @property
    def operands(self):
        return self._operands

    @property
    def mnemonic(self):
        return self._mnemonic


class Disassembler(object):
    def __init__(self):
        self._instructions = {}
        self._code_xrefs_from = defaultdict(set)
        self._code_xrefs_to = defaultdict(set)

    def _disassemble(self, data, offset, ip):
        stream = {}
        work = set([ip + offset])
        visited = set()

        while work:
            current = work.pop()
            visited.add(current)

            relative = current - offset
            if current in self._instructions:
                stream[relative] = self._instructions[relative]
                continue

            relative_offset = current - offset - ip
            current_data = data[relative_offset:
                                relative_offset + MAX_INSTRUCTION]
            if not len(current_data):
                continue

            instruction = decode(relative, current_data)
            if not instruction:
                break

            length = instruction['length']
            disasm = instruction['disasm']
            dests = instruction['dests']

            if dests:
                work.update(dests)
                work = work.difference(visited)

            instruction = DecodedInstruction(disasm.opcode, disasm.operands,
                                             length, relative)
            self._instructions[relative] = instruction
            stream[relative] = instruction

            non_trivial_dests = set(dests) - set([relative + length])
            # One destination might point to the (physically) next instruction
            # without being a non-trivial one. Check PCJmpDestination class.
            for o in disasm.operands:
                if isinstance(o, PCJmpDestination):
                    if o.addr == relative + length:
                        non_trivial_dests.add(o.addr)
                        break

            self._update_references(instruction, non_trivial_dests)

        return stream

    def _update_references(self, instruction, dests):
        ip = instruction.ip
        for d in dests:
            self._code_xrefs_from[ip].add(d)
            self._code_xrefs_to[d].add(ip)

    def _parse_operand(self, operand):
        # TODO: Bit/BitNot may need to be fixed -- test it.
        mapping = {
            AccumulatorOperand: lambda _: A,
            DptrOperand: lambda _: DPTR,
            PCOperand: lambda _: PC,
            ABOperand: lambda _: AB,
            CarryFlagOperand: lambda _: C,
            DptrIndirectAddressingOperand: lambda _: [DPTR],
            RegisterOperand: lambda o: globals()[str(o)],
            RegisterIndirectAddressingOperand: lambda o: [globals()[str(o.Rn)]],
            DirectAddressingOperand: lambda o: Indirection(o.direct),
            ImmediateOperand8: lambda o: Immediate(o.constant, 8),
            ImmediateOperand16: lambda o: Immediate(o.constant, 16),
            BitOperand: lambda o: BitNot(o.bit) if o.invflag else Bit(o.bit),
            PCJmpDestination: lambda o: Block.build_label(o.addr),
        }

        handler = mapping.get(type(operand))
        assert handler, 'Don\'t know how to parse operand from disassembler.'
        return handler(operand)

    def parse(self, data, offset, ip):
        stream = self._disassemble(data, offset, ip)
        blocks, current = [], Block()

        for k, v in sorted(stream.iteritems()):
            instruction_class = globals()[v.mnemonic]
            parsed = instruction_class(*[self._parse_operand(o) for o\
                                         in v.operands])

            if v.ip in self.xrefs_from:
                if v.ip in self.xrefs_to:
                    current.append(Block.build_label(v.ip))

                current.append(parsed)
                blocks.append(current)
                current = Block()
                continue

            elif v.ip in self.xrefs_to:
                blocks.append(current)
                current = Block()
                current.append(Block.build_label(v.ip))

            current.append(parsed)

        if current:
            blocks.append(current)

        blocks = filter(lambda x: x, blocks)
        return blocks

    @property
    def xrefs_from(self):
        return self._code_xrefs_from

    @property
    def xrefs_to(self):
        return self._code_xrefs_to


def main():
    try:
        os.remove(RESULT)
    except OSError:
        pass

    ihx = IntelHex()
    ihx.fromfile(TARGET, format='hex')
    addr_min, addr_max = ihx.minaddr(), ihx.maxaddr()
    print hex(addr_min), hex(addr_max)

    ihx.tofile(TEST, format='hex')

    d = Disassembler()
    function = ihx.tobinarray()[FUNC_START:]
    blocks = d.parse(function, 0, FUNC_START)

    for b in blocks:
        print '-' * 40
        print repr(b)

    print '-' * 40
    blocks = sum(blocks)

    data = blocks.assemble(FUNC_START, externalize_labels=True)
    print 'Stream:', ' '.join('%02x' % b for b in bytearray(data))

    data_length = len(data)
    print 'Writing %d bytes.' % data_length

    ihx.puts(FUNC_START, data)

    appendix = Block()
    label_nops = Label('look_mah_no_ops')
    appendix += Block(label_nops, nop, nop, nop, nop)

    appendix += Block(Data('\xef\xbe'))
    appendix += Block(Data(0xbeef))
    appendix += Block(Data(label_nops))

    end = ihx.maxaddr() + 1
    data = appendix.assemble(end, externalize_labels=True)

    data_length = len(data)
    print 'Writing %d bytes.' % data_length

    ihx.puts(end, data)

    ihx.tofile(RESULT, format='hex')

    patched = IntelHex()
    patched.fromfile(RESULT, format='hex')

    check = ihx.tobinarray()[FUNC_START:FUNC_START + data_length]
    print 'Stream:', ' '.join('%02x' % b for b in bytearray(data))

    print hex(patched.minaddr()), hex(patched.maxaddr())


if __name__ == '__main__':
    main()
