import string
from typing import List, Optional

import numpy as np

# language=css
css = '''
table.sudoku {
    border: 2px solid #555;
}

table.sudoku tr {
    background: #fff !important;
}

table.sudoku tr.b {
    border-bottom: 2px solid #555;
}

table.sudoku td {
    border: 1px solid #bbb;
    width: 2.5em;
    height: 2.5em;
    text-align: center;
}

table.sudoku td.m {
    background: #f4f4f4;
}

table.sudoku td.b {
    border-right: 2px solid #555;
}
'''


def class_attr(classes: List[str]) -> str:
    if classes:
        return f''' class="{' '.join(classes)}"'''
    return ''

class Sudoku:
    def __init__(self, data: List[int], mask: Optional[List[bool]] = None):
        """
        Creates puzzle from raw representation as list of 81
        numbers 1-9 and 0 for empty fields.

        :param data: Raw representation of sudoku puzzle
        :param mask: List of booleans stating if field was empty in original puzzle
        """

        assert len(data) == 81

        self.data = np.array(data, dtype=np.uint8)

        if mask is not None:
            assert len(mask) == 81
        else:
            mask = [i == 0 for i in data]

        self.mask = np.array(mask, dtype=np.bool)

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

    def clone(self) -> 'Sudoku':
        return Sudoku(
            self.data.copy(),
            self.mask.copy(),
        )

    def _repr_html_(self) -> str:
        r = [
            f'<style>{css}</style>'
            '<table class="sudoku">'
        ]

        for i, d in enumerate(self.data):
            if i % 9 == 0:
                row_class = []

                if i == 18 or i == 45:
                    row_class.append('b')

                r.append(f'<tr{class_attr(row_class)}>')

            cell_class = []

            if not self.mask[i]:
                cell_class.append('m')

            if i % 3 == 2 and i % 9 != 8:
                cell_class.append('b')

            cell_value = '' if d == 0 else d

            r.append(f'<td{class_attr(cell_class)}>{cell_value}</td>')

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
