import os
from abc import abstractmethod

import numpy as np
import pyopencl as cl

from sudo_annealing.solvers.abstract import NonSteppingSolver
from sudo_annealing.sudoku import Sudoku


__ctx = None
__queue = None
MF = cl.mem_flags


def init():
    global __ctx, __queue
    __ctx = cl.create_some_context(interactive=True)
    __queue = cl.CommandQueue(__ctx)

    print('Used OpenCL devices:')
    for i, device in enumerate(__ctx.devices, start=1):
        print(f'[{i}]', device.name)
        print('   ', 'OpenCL version:', device.version)
        print('   ', 'Supported Extensions:')
        for ext in device.extensions.split(' '):
            print('   ', '-', ext)

def ctx():
    return __ctx

def queue():
    return __queue

def get_program_source(program_name: str) -> str:
    path = os.path.join(os.path.dirname(__file__), 'cl', f'{program_name}.cl')
    with open(path, 'r') as f:
        return f.read()


def get_program(program_name: str) -> cl.Program:
    source = get_program_source(program_name)
    prg = cl.Program(ctx(), source)
    return prg.build()


class CLSolver(NonSteppingSolver):
    @classmethod
    @abstractmethod
    def program_name(cls) -> str:
        pass

    @classmethod
    def do_solve(cls, sudoku: Sudoku) -> Sudoku:
        solution_np = cls.run_kernel(
            sudoku.data,
            sudoku.bitmask(),
            get_program(cls.program_name())
        )
        return Sudoku(solution_np, sudoku.mask)

    @classmethod
    @abstractmethod
    def run_kernel(cls, sudoku_data: np.ndarray, bitmask: np.ndarray, program) -> np.ndarray:
        pass
