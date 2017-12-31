from typing import List

from ipywidgets import interact

from sudo_annealing.puzzle_pack import SudokuPack
from sudo_annealing.solvers.abstract import AbstractSolver


def workbench(algorithms: List[AbstractSolver], puzzle_pack: SudokuPack):
    interact(
        workbench_f,
        algo={a.full_name(): a for a in algorithms},
        puzzle={i: p for i, p in enumerate(puzzle_pack.data)},
    )


def workbench_f(algo, puzzle):
    return puzzle
