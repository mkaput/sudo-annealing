import glob
import gzip
from collections import UserList
from typing import List, Callable, TypeVar, Generic

from ipywidgets import interact

from .sudoku import Sudoku

T = TypeVar('T')


class SudokuPack(Generic[T], UserList, List[T]):
    def __init__(self, initlist=None):
        super().__init__(initlist)

    @classmethod
    def _extract(cls, entry: T) -> Sudoku:
        return entry

    @property
    def f(self) -> Callable[[int], Sudoku]:
        def g(i):
            return self._extract(self.data[i])

        return g

    def interact(self):
        interact(self.f, i=(0, len(self.data) - 1))


def load_pack(path_glob: str, recursive=False) -> SudokuPack[Sudoku]:
    pack = SudokuPack()
    for path in glob.iglob(path_glob, recursive=recursive):
        if path.endswith('.txt.gz'):
            with gzip.open(path, mode='rt') as f:
                for line in f:
                    sudoku = Sudoku.parse(line)
                    if sudoku is not None:
                        pack.append(sudoku)
    return pack
