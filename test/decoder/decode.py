# top = decoder::decode

from cocotb.regression import TestFactory
from cocotb.triggers import Timer
from spade import SpadeExt

async def test(dut, values: tuple[int, str, int]):
    s = SpadeExt(dut)
    (value, expected_op, expected_bytes) = values
    s.i.value = value
    await Timer(1, units="ps")
    s.o.op.assert_eq(expected_op)
    s.o.bytes.assert_eq(expected_bytes)

tf = TestFactory(test)
tf.add_option('values', [
    (0b010_000_000_010_111_0_000_000_000_000_000_0, "Op::Add", 2),
    (0b010_000_001_000_010_0_000_000_000_000_000_0, "Op::Multiply", 2),
    (0b011_000_001_001_100_1_011_011_111_111_111_0, "Op::LogicShiftRight", 4),
    (0b010_000_000_010_111_1_000_000_000_000_000_0, "Op::Invalid", 2),
    (0b000_000_000_000_000_0_000_000_000_000_000_0, "Op::Invalid", 2),
    (0b101_0_0000_0000_0000_0000_0000_0000_0000, "Op::Number(0)", 4),
    (0b101_0_0000_0000_0000_0000_0000_0000_0001, "Op::Number(1)", 4),
    (0b101_0_0000_0000_0000_0000_0000_0000_1111, "Op::Number(15)", 4),
    (0b101_0_0000_0000_0000_0000_1000_0000_0000, "Op::Number(2048)", 4),
    (0b101_0_0000_0000_0000_0001_0000_0000_0000, "Op::Number(4096)", 4),
    (0b101_0_1000_0000_0000_0000_0000_0000_0000, "Op::Number(134217728)", 4),
    (0b101_1_1111_1111_1111_1111_1111_1111_1111, "Op::Number(-1)", 4),
])
tf.generate_tests()
