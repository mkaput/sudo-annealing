import numpy as np
import pyopencl as cl

from sudo_annealing.solvers.abstractcl import CLSolver, ctx, queue, MF


class CLDFS(CLSolver):
    @classmethod
    def full_name(cls) -> str:
        return "Backtracing, OpenCL"

    @classmethod
    def program_name(cls) -> str:
        return 'cldfs'

    @classmethod
    def run_kernel(cls, sudoku: np.ndarray, bitmask: np.ndarray, program) -> np.ndarray:
        sudoku_buff = cl.Buffer(ctx(), MF.READ_ONLY | MF.COPY_HOST_PTR, hostbuf=sudoku)
        bitmask_buff = cl.Buffer(ctx(), MF.READ_ONLY | MF.COPY_HOST_PTR, hostbuf=bitmask)
        solution_buff = cl.Buffer(ctx(), MF.WRITE_ONLY, sudoku.nbytes)

        program.solve(queue(), [1], None,
            sudoku_buff, bitmask_buff, solution_buff)

        solution = np.empty_like(sudoku)
        cl.enqueue_copy(queue(), solution, solution_buff)

        return solution
