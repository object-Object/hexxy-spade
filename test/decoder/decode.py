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


PAD = "000"
A = "001"
Q = "010"
W = "011"
E = "100"
D = "101"
NUMBER = "110"
RESERVED = "111"

tf = TestFactory(test)
tf.add_option(
    "values",
    [
        (f"0b{W}{A}{A}{W}{PAD}_0_{PAD * 5}_0", "Op::Add", 2),
        (f"0b{W}{A}{Q}{A}{W}_0_{PAD * 5}_0", "Op::Multiply", 2),
        (f"0b{E}{A}{Q}{Q}{D}_1_{E}{E}{PAD * 3}_0", "Op::LogicShiftRight", 4),
        (f"0b{W}{A}{A}{W}{PAD}_1_{PAD * 5}_0", "Op::Invalid", 2),
        (f"0b{PAD * 5}_0_{PAD * 5}_0", "Op::Invalid", 2),
        (f"0b{RESERVED * 5}_0_{RESERVED * 5}_0", "Op::Invalid", 2),
        (f"0b{NUMBER}_0_0000_0000_0000_0000_0000_0000_0000", "Op::Number(0)", 4),
        (f"0b{NUMBER}_0_0000_0000_0000_0000_0000_0000_0001", "Op::Number(1)", 4),
        (f"0b{NUMBER}_0_0000_0000_0000_0000_0000_0000_1111", "Op::Number(15)", 4),
        (f"0b{NUMBER}_0_0000_0000_0000_0000_1000_0000_0000", "Op::Number(2048)", 4),
        (f"0b{NUMBER}_0_0000_0000_0000_0001_0000_0000_0000", "Op::Number(4096)", 4),
        (
            f"0b{NUMBER}_0_1000_0000_0000_0000_0000_0000_0000",
            "Op::Number(134217728)",
            4,
        ),
        (f"0b{NUMBER}_1_1111_1111_1111_1111_1111_1111_1111", "Op::Number(-1)", 4),
    ],
)
tf.generate_tests()
