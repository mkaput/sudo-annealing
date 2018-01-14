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
    def run_kernel(cls, sudoku_data: np.ndarray, program) -> np.ndarray:
        in_sudoku = cl.Buffer(ctx, MF.READ_ONLY | MF.COPY_HOST_PTR, hostbuf=sudoku_data)
        solution = cl.Buffer(ctx, MF.WRITE_ONLY, sudoku_data.nbytes)

        program.solve(queue, sudoku_data.shape, None, in_sudoku, solution)

        solution_np = np.empty_like(sudoku_data)
        cl.enqueue_copy(queue, solution_np, solution)

        return solution_np
