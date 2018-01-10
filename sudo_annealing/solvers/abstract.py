from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from sudo_annealing.puzzle_pack import SudokuPack
from sudo_annealing.sudoku import Sudoku


class SudokuSolution(SudokuPack, List[Tuple[int, Sudoku]]):
    def __init__(self, initlist=None):
        super().__init__(initlist)

    @classmethod
    def _extract(cls, entry: Tuple[int, Sudoku]) -> Sudoku:
        return entry[1]

    def solution(self) -> Sudoku:
        return self._extract(self.data[-1])

    def _repr_html_(self):
        return self.solution()._repr_html_()


class AbstractSolver(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def full_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def solve(cls, sudoku: Sudoku) -> SudokuSolution:
        pass

    @classmethod
    def display_name(cls) -> str:
        return cls.full_name()

    @classmethod
    def log(cls, msg: str):
        print(f'[{cls.__name__}]:', msg)


class NonSteppingSolver(AbstractSolver):
    @classmethod
    @abstractmethod
    def do_solve(cls, sudoku: Sudoku) -> Sudoku:
        pass

    @classmethod
    def display_name(cls) -> str:
        return f'{cls.full_name()}, non-stepping'

    @classmethod
    def solve(cls, sudoku: Sudoku) -> SudokuSolution:
        s = SudokuSolution()
        s.append((0, sudoku.clone()))
        solution = cls.do_solve(sudoku)
        s.append((1, solution))
        return s
