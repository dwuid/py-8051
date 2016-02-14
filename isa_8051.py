
from isa51_assembler import Instruction, Immediate, Destination, Register,\
    SpecialAccumulator, SpecialDptr, SpecialAB, CarryFlag, Bit, BitNot,\
    Indirection, IndirectionRegister, IndirectionDptr, IndirectionAccPc,\
    IndirectionAccDptr, TagDirect11, TagDirect16, TagRelativeOffset


class ajmp(Instruction, TagDirect11):
    _encoding_ = [
        (0x01, 2, (Destination,))
    ]

class acall(Instruction, TagDirect11):
    _encoding_ = [
        (0x11, 2, (Destination,))
    ]

class ljmp(Instruction, TagDirect16):
    _encoding_ = [
        (0x02, 3, (Destination,)),
    ]

class anl(Instruction):
    _encoding_ = [
        (0x52, 2, (Indirection, SpecialAccumulator,)),
        (0x53, 3, (Indirection, Immediate,)),
        (0x54, 2, (SpecialAccumulator, Immediate,)),
        (0x55, 2, (SpecialAccumulator, Indirection,)),
        (0x56, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0x58, 1, (SpecialAccumulator, Register,)),
        (0x82, 2, (CarryFlag, Bit,)),
        (0xb0, 2, (CarryFlag, BitNot,)),
    ]

class jnz(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x70, 2, (Destination,)),
    ]

class xch(Instruction):
    _encoding_ = [
        (0xc5, 2, (SpecialAccumulator, Indirection,)),
        (0xc6, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0xc8, 1, (SpecialAccumulator, Register,)),
    ]

class rrc(Instruction):
    _encoding_ = [
        (0x13, 1, (SpecialAccumulator,)),
    ]

class movc(Instruction):
    _encoding_ = [
        (0x83, 1, (SpecialAccumulator, IndirectionAccPc,)),
        (0x93, 1, (SpecialAccumulator, IndirectionAccDptr,)),
    ]

class pop(Instruction):
    _encoding_ = [
        (0xd0, 2, (Indirection,)),
    ]

class jnc(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x50, 2, (Destination,)),
    ]

class jnb(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x30, 3, (Bit, Destination,)),
    ]

class subb(Instruction):
    _encoding_ = [
        (0x94, 2, (SpecialAccumulator, Immediate,)),
        (0x95, 2, (SpecialAccumulator, Indirection,)),
        (0x96, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0x98, 1, (SpecialAccumulator, Register,)),
    ]

class movx(Instruction):
    _encoding_ = [
        (0xe0, 1, (SpecialAccumulator, IndirectionDptr,)),
        (0xe2, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0xf0, 1, (IndirectionDptr, SpecialAccumulator,)),
        (0xf2, 1, (IndirectionRegister, SpecialAccumulator,)),
    ]

class inc(Instruction):
    _encoding_ = [
        (0x04, 1, (SpecialAccumulator,)),
        (0x05, 2, (Indirection,)),
        (0x06, 1, (IndirectionRegister,)),
        (0x08, 1, (Register,)),
        (0xa3, 1, (SpecialDptr,)),
    ]

class xrl(Instruction):
    _encoding_ = [
        (0x62, 2, (Indirection, SpecialAccumulator,)),
        (0x63, 3, (Indirection, Immediate,)),
        (0x64, 2, (SpecialAccumulator, Immediate,)),
        (0x65, 2, (SpecialAccumulator, Indirection,)),
        (0x66, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0x68, 1, (SpecialAccumulator, Register,)),
    ]

class rr(Instruction):
    _encoding_ = [
        (0x03, 1, (SpecialAccumulator,)),
    ]

class sjmp(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x80, 2, (Destination,)),
    ]

class reti(Instruction):
    _encoding_ = [
        (0x32, 1, None),
    ]

class ret(Instruction):
    _encoding_ = [
        (0x22, 1, None),
    ]

class add(Instruction):
    _encoding_ = [
        (0x24, 2, (SpecialAccumulator, Immediate,)),
        (0x25, 2, (SpecialAccumulator, Indirection,)),
        (0x26, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0x28, 1, (SpecialAccumulator, Register,)),
    ]

class addc(Instruction):
    _encoding_ = [
        (0x34, 2, (SpecialAccumulator, Immediate,)),
        (0x35, 2, (SpecialAccumulator, Indirection,)),
        (0x36, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0x38, 1, (SpecialAccumulator, Register,)),
    ]

class swap(Instruction):
    _encoding_ = [
        (0xc4, 1, (SpecialAccumulator,)),
    ]

class rl(Instruction):
    _encoding_ = [
        (0x23, 1, (SpecialAccumulator,)),
    ]

class mul(Instruction):
    _encoding_ = [
        (0xa4, 1, (SpecialAB,)),
    ]

class xchd(Instruction):
    _encoding_ = [
        (0xd6, 1, (SpecialAccumulator, IndirectionRegister,)),
    ]

class djnz(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0xd5, 3, (Indirection, Destination,)),
        (0xd8, 2, (Register, Destination,)),
    ]

class clr(Instruction):
    _encoding_ = [
        (0xc2, 2, (Bit,)),
        (0xc3, 1, (CarryFlag,)),
        (0xe4, 1, (SpecialAccumulator,)),
    ]

class jz(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x60, 2, (Destination,)),
    ]

class jmp(Instruction):
    _encoding_ = [
        (0x73, 1, (IndirectionAccDptr,)),
    ]

class mov(Instruction):
    _encoding_ = [
        (0x74, 2, (SpecialAccumulator, Immediate,)),
        (0x75, 3, (Indirection, Immediate,)),
        (0x76, 2, (IndirectionRegister, Immediate,)),
        (0x78, 2, (Register, Immediate,)),
        (0x85, 3, (Indirection, Indirection,)),
        (0x86, 2, (Indirection, IndirectionRegister,)),
        (0x88, 2, (Indirection, Register,)),
        (0x90, 3, (SpecialDptr, Immediate,)),
        (0x92, 2, (Bit, CarryFlag,)),
        (0xa2, 2, (CarryFlag, Bit,)),
        (0xa6, 2, (IndirectionRegister, Indirection,)),
        (0xa8, 2, (Register, Indirection,)),
        (0xe5, 2, (SpecialAccumulator, Indirection,)),
        (0xe6, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0xe8, 1, (SpecialAccumulator, Register,)),
        (0xf5, 2, (Indirection, SpecialAccumulator,)),
        (0xf6, 1, (IndirectionRegister, SpecialAccumulator,)),
        (0xf8, 1, (Register, SpecialAccumulator,)),
    ]

class rlc(Instruction):
    _encoding_ = [
        (0x33, 1, (SpecialAccumulator,)),
    ]

class da(Instruction):
    _encoding_ = [
        (0xd4, 1, (SpecialAccumulator,)),
    ]

class orl(Instruction):
    _encoding_ = [
        (0x42, 2, (Indirection, SpecialAccumulator,)),
        (0x43, 3, (Indirection, Immediate,)),
        (0x44, 2, (SpecialAccumulator, Immediate,)),
        (0x45, 2, (SpecialAccumulator, Indirection,)),
        (0x46, 1, (SpecialAccumulator, IndirectionRegister,)),
        (0x48, 1, (SpecialAccumulator, Register,)),
        (0x72, 2, (CarryFlag, Bit,)),
        (0xa0, 2, (CarryFlag, BitNot,)),
    ]

class cjne(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0xb4, 3, (SpecialAccumulator, Immediate, Destination,)),
        (0xb5, 3, (SpecialAccumulator, Indirection, Destination,)),
        (0xb6, 3, (IndirectionRegister, Immediate, Destination,)),
        (0xb8, 3, (Register, Immediate, Destination,)),
    ]

class lcall(Instruction, TagDirect16):
    _encoding_ = [
        (0x12, 3, (Destination,)),
    ]

class nop(Instruction):
    _encoding_ = [
        (0x00, 1, None),
    ]

class jb(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x20, 3, (Bit, Destination,)),
    ]

class jc(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x40, 2, (Destination,)),
    ]

class cpl(Instruction):
    _encoding_ = [
        (0xb2, 2, (Bit,)),
        (0xb3, 1, (CarryFlag,)),
        (0xf4, 1, (SpecialAccumulator,)),
    ]

class setb(Instruction):
    _encoding_ = [
        (0xd2, 2, (Bit,)),
        (0xd3, 1, (CarryFlag,)),
    ]

class jbc(Instruction, TagRelativeOffset):
    _encoding_ = [
        (0x10, 3, (Bit, Destination,)),
    ]

class push(Instruction):
    _encoding_ = [
        (0xc0, 2, (Indirection,)),
    ]

class div(Instruction):
    _encoding_ = [
        (0x84, 1, (SpecialAB,)),
    ]

class dec(Instruction):
    _encoding_ = [
        (0x14, 1, (SpecialAccumulator,)),
        (0x15, 2, (Indirection,)),
        (0x16, 1, (IndirectionRegister,)),
        (0x18, 1, (Register,)),
    ]
