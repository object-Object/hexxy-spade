# top = alu::operate_4

from cocotb.regression import TestFactory
from cocotb.triggers import Timer
from spade import SpadeExt

async def test(dut, values):
    s = SpadeExt(dut)
    (stack, op, expected) = values
    s.i.stack = stack
    s.i.op = op
    await Timer(1, units="ps")
    s.o.assert_eq(expected)

tf = TestFactory(test)
tf.add_option('values', [
    (
        [1, 2, 3, 4],
        "Op::Add",
        [0, 1, 2, 7],
    ),
])
tf.generate_tests()
