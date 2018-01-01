from sudo_annealing.solvers.abstract import AbstractSolver, SudokuSolution
from sudo_annealing.sudoku import Sudoku


class PyDFS(AbstractSolver):
    @classmethod
    def full_name(cls) -> str:
        return "Backtracing, Python"

    @classmethod
    def solve(cls, sudoku: Sudoku) -> SudokuSolution:
        s = SudokuSolution()
        s.append((0, sudoku.clone()))
        result = cls.do_solve(0, 0, sudoku, s)
        if not result:
            raise Exception("sudoku not solvable!")
        return s

    @classmethod
    def do_solve(cls, it: int, c: int, sudoku: Sudoku, sol: SudokuSolution) -> bool:
        while c < 81 and not sudoku.masked(c):
            c += 1

        if c >= 81:
            return True

        for num in range(1, 10):
            if sudoku.is_safe_to_put(num, c):
                it += 1
                sudoku.data[c] = num
                sol.append((it, sudoku.clone()))

                if cls.do_solve(it, c + 1, sudoku, sol):
                    return True

                sudoku.data[c] = 0

        return False
