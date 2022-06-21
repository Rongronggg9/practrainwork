from __future__ import annotations
from typing import Union

from random import randint, random

import wasmtime.loader  # noqa: F401  # wasmtime.loader empower the possibility to directly import a WAT file
import wasm_code  # type: ignore  # the WAT file

func_call_map = {
    int: {
        '+': wasm_code.add_int,
        '-': wasm_code.sub_int,
        '*': wasm_code.mul_int,
        '/': wasm_code.div_int,
    },
    float: {
        '+': wasm_code.add_float,
        '-': wasm_code.sub_float,
        '*': wasm_code.mul_float,
        '/': wasm_code.div_float,
    },
}

verify_map = {
    int: {
        '+': int.__add__,
        '-': int.__sub__,
        '*': int.__mul__,
        '/': int.__floordiv__,
    },
    float: {
        '+': float.__add__,
        '-': float.__sub__,
        '*': float.__mul__,
        '/': float.__truediv__,
    },
}


# noinspection PyArgumentList
def verify_wasm_code(
        num1: Union[int, float],
        operator: str,
        num2: Union[int, float]

) -> Union[int, float]:
    """
    Verifies the result of the given operation.
    """
    if isinstance(num1, int) and isinstance(num2, int):
        num_type = int
    else:
        num_type = float
    wasm_v = func_call_map[num_type][operator](num1, num2)
    py_v = verify_map[num_type][operator](num1, num2)
    if py_v < 0 and num_type is int and operator == '/':
        py_v += 1
    print(f'{num1} {operator} {num2} = {wasm_v} (Py: {py_v})')
    assert wasm_v == py_v
    # assert abs(wasm_v - py_v) < 0.01  # if the float number in wasm is f32, the error could be up to 0.01
    return wasm_v


def main():
    for num_type in [int, float]:
        for operator in func_call_map[num_type]:
            for _ in range(3):
                if num_type is int:
                    num1 = randint(-1000, 1000)
                    num2 = randint(-100, 100)
                    while num2 == 0 and operator == '/':
                        num2 = randint(-100, 100)
                else:
                    num1 = random() * 1000
                    num2 = random() * 100
                    while num2 == 0 and operator == '/':
                        num2 = random() * 100
                verify_wasm_code(num1, operator, num2)


if __name__ == '__main__':
    main()
