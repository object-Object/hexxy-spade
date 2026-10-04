# top = double_dabble_3_testbench

import cocotb
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import FallingEdge
from spade import SpadeExt


async def test(dut, values):
    (value, expected) = values

    s = SpadeExt(dut)

    clk = dut.clk_i
    await cocotb.start(Clock(clk, 1, units="ns").start())
    await FallingEdge(clk)
    s.i.rst = True
    s.i.value = value
    await FallingEdge(clk)
    s.i.rst = False

    for _ in range(10):
        await FallingEdge(clk)

    s.i.value = value
    await FallingEdge(clk)
    s.o.assert_eq(expected)


tf = TestFactory(test)
tf.add_option(
    "values",
    [
        (0, 0),
        (1, 1),
        (9, 9),
        (10, (1 << 4)),
        (11, (1 << 4) | 1),
        (12, (1 << 4) | 2),
        (19, (1 << 4) | 9),
        (25, (2 << 4) | 5),
        (123, (1 << 8) | (2 << 4) | 3),
    ],
)
tf.generate_tests()
