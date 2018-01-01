from sudo_annealing.solvers.abstract import AbstractSolver, SudokuSolution
from sudo_annealing.sudoku import Sudoku


class PyDFS(AbstractSolver):
    @classmethod
    def full_name(cls) -> str:
        return "Backtracing, Python"

    @classmethod
    def solve(cls, sudoku: Sudoku) -> SudokuSolution:
        s = SudokuSolution()
        s.append((0, sudoku))
        s.append((10, sudoku))
        s.append((20, sudoku))
        return s
