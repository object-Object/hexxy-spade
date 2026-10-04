# top = decoder::decode

from cocotb.regression import TestFactory
from cocotb.triggers import Timer
from spade import SpadeExt

async def test(dut, values: tuple[int, str]):
    s = SpadeExt(dut)
    (value, expected) = values
    s.i.value = value
    await Timer(1, units="ps")
    s.o.assert_eq(expected)

tf = TestFactory(test)
tf.add_option('values', [
    (0b010_000_000_010_111_0, "Action::Add"),
    (0b010_000_000_010_111_1, "Action::Invalid"),
    (0b000_000_000_000_000_0, "Action::Invalid"),
    (0b101_0_0000_0000_0000, "Action::Number(0)"),
    (0b101_0_0000_0000_0001, "Action::Number(1)"),
    (0b101_0_0000_0000_1111, "Action::Number(15)"),
    (0b101_0_1000_0000_0000, "Action::Number(2048)"),
    (0b101_1_1111_1111_1111, "Action::Number(-1)"),
])
tf.generate_tests()
