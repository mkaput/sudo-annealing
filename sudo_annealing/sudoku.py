import glob
import gzip
import string
from typing import List, Optional


def load_pack(path_glob: str, recursive=False) -> List['Sudoku']:
    pack = []
    for path in glob.iglob(path_glob, recursive=recursive):
        if path.endswith('.txt.gz'):
            with gzip.open(path, mode='rt') as f:
                for line in f:
                    sudoku = Sudoku.parse(line)
                    if sudoku is not None:
                        pack.append(sudoku)
    return pack


class Sudoku:
    def __init__(self, data: List[int]):
        """
        Creates puzzle from raw representation as list of 81
        numbers 1-9 and 0 for empty fields.

        :param data: Raw representation of sudoku puzzle
        """

        self.data = data
        self.mask = [i == 0 for i in data]

    @classmethod
    def parse(cls, s: str) -> Optional['Sudoku']:
        """

        :param s:
        :return: parsed sudoku puzzle or `None`
        """

        data = [int(c) for c in s if c in string.digits]
        if len(data) != 81:
            return None
        return cls(data)

    def _repr_html_(self) -> str:
        r = ['<table style="border: 2px solid #555">']

        for i, d in enumerate(self.data):
            if i % 9 == 0:
                row_style = 'background: #fff;'

                if i == 18 or i == 45:
                    row_style += 'border-bottom: 2px solid #555;'

                r.append(f'<tr style="{row_style}">')

            cell_style = 'border: 1px solid #bbb;width:2.5em;height:2.5em;text-align:center;'

            if not self.mask[i]:
                cell_style += 'background: #f4f4f4;'

            if i % 3 == 2 and i % 9 != 8:
                cell_style += 'border-right: 2px solid #555;'

            cell_value = '' if d == 0 else d

            r.append(f'<td style="{cell_style}">{cell_value}</td>')

            if i % 9 == 8:
                r.append('</tr>')

        r.append('</table>')

        return ''.join(r)

    def __str__(self) -> str:
        r = []
        for i, d in enumerate(self.data):
            r.append(str(' ' if d == 0 else d))
            if i % 9 == 8:
                r.append('\n')
        return ''.join(r)
