import string
from typing import List, Optional, Tuple, Union

import numpy as np

Coords = Union[int, Tuple[int, int]]
Row = Tuple[int, int, int, int, int, int, int, int, int]

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

    @classmethod
    def conv2t1(cls, c2d: Tuple[int, int]) -> int:
        """
        Converts 2D cell coords to 1D
        """
        x, y = c2d
        assert 0 <= x < 9 and 0 <= y < 9
        return y * 9 + x

    @classmethod
    def conv1t2(cls, c1d: int) -> Tuple[int, int]:
        """
        Converts 1D cell coords to 2D
        """
        x, y = c1d % 9, c1d // 9
        assert 0 <= x < 9 and 0 <= y < 9
        return x, y

    @classmethod
    def unify_coords(cls, coords: Coords) -> int:
        if isinstance(coords, tuple):
            coords = cls.conv2t1(coords)
        assert 0 <= coords < 81
        return coords

    def __getitem__(self, coords: Coords) -> int:
        return self.data[self.unify_coords(coords)]

    def get_row(self, coords: Coords) -> Row:
        offset = (self.unify_coords(coords) // 9) * 9
        return tuple(self.data[offset:offset + 9])

    def get_col(self, coords: Coords) -> Row:
        offset = self.unify_coords(coords) % 9
        return tuple(self.data[offset::9])

    def get_box(self, coords: Coords) -> Row:
        x, y = self.conv1t2(self.unify_coords(coords))
        x, y = (x // 3) * 3, (y // 3) * 3
        p = []
        for i in range(3):
            for j in range(3):
                p.append(self.conv2t1((x + j, y + i)))
        # noinspection PyTypeChecker
        return tuple(self.data[i] for i in p)

    def masked(self, coords: Coords) -> bool:
        return self.mask[self.unify_coords(coords)]

    def is_safe_to_put(self, value: int, coords: Coords) -> bool:
        assert 1 <= value <= 9
        return value not in self.get_row(coords) and \
               value not in self.get_col(coords) and \
               value not in self.get_box(coords)

    def clone(self) -> 'Sudoku':
        return Sudoku(
            self.data.copy(),
            self.mask.copy(),
        )

    def bitmask(self) -> np.ndarray:
        """
        Returns mask represented as 128bit bitmap, where 1 means field is empty.
        The bitmap is represented as 2-vector of 64-bit unsigned integers,
        little endian, least significant bit contains mask for first cell.

        So value layout looks like this:
        ```
        [63, ..., 1, 0] [(unused, zeros)..., 81, ..., 65, 64]
        ```

        To index it one can use following formula:
        ```
        bitmask(i) = bitmask[i // 64] & (1 << (i % 64))
        ```
        """
        bit = np.array([0, 0], dtype=np.uint64)
        for i, v in enumerate(self.mask):
            if v:
                bit[i // 64] |= np.uint64(1 << (i % 64))
        return bit

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
