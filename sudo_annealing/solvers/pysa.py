from sudo_annealing import Sudoku
from sudo_annealing.solvers.abstract import AbstractSolver, SudokuSolution
from random import randint, random
from math import exp


class PySA(AbstractSolver):
    @classmethod
    def full_name(cls) -> str:
        return "Simulated Annealing, Python"

    @classmethod
    def solve(cls, sudoku: Sudoku) -> SudokuSolution:
        s = SudokuSolution()
        s.append((0, sudoku.clone()))
        result = cls.do_solve(0, 1e20, 1.5, sudoku, s)
        if not result:
            raise Exception("sudoku not solvable!")
        return s

    @classmethod
    def do_solve(cls, it: int, temp: float, step: float, sudoku: Sudoku,
                 sol: SudokuSolution) -> bool:

        # setup
        cls.fill_board(sudoku)
        mark = cls.assess_board(sudoku)

        # iteration purposes (display)
        delta_temp = temp / 1e4
        check_temp = temp - delta_temp
        sol.append((it, sudoku.clone()))
        it += 1

        while temp > 1e-2 or mark != 0:
            old, new = cls.candidates_for_shuffle()

            if sudoku.masked(old) and sudoku.masked(new):
                temp /= step

                delta = cls.make_change(sudoku, old, new)

                if delta < 0:
                    mark += delta
                elif random() < exp((-delta) / temp):
                    mark += delta
                else:
                    cls.unmake_change(sudoku, old, new)

                # for displaying purposes
                if check_temp > temp:
                    it += 1
                    sol.append((it, sudoku.clone()))
                    check_temp = temp - delta_temp

        if mark == 0:
            sol.append((it + 1, sudoku.clone()))
            return True
        return False

    @classmethod
    def fill_board(cls, sudoku: Sudoku):
        [cls.fill_box(sudoku, 3 * i, 3 * j)
         for i in range(3) for j in range(3)]

    @classmethod
    def fill_box(cls, s: Sudoku, x: int, y: int):
        nums = [i for i in range(1, 10)]
        for i in range(3):
            for j in range(3):
                if not s.masked((x + i, y + j)):
                    nums.remove(s.data[Sudoku.conv2t1((x + i, y + j))])

        for i in range(3):
            for j in range(3):
                if s.masked((x + i, y + j)):
                    s.data[Sudoku.conv2t1((x + i, y + j))] = nums.pop()

    # 162 - starting mark ; -1 for each distinct entry in row/column;
    # 0 - accepting mark
    @classmethod
    def assess_board(cls, sudoku: Sudoku) -> int:
        mark = 162
        for i in range(0, 81, 10):
            mark += cls.assess_row(sudoku.get_row(i))
            mark += cls.assess_row(sudoku.get_col(i))
        return mark

    @classmethod
    def assess_change(cls, old_rows: tuple, new_rows: tuple) -> int:
        old_score = sum([cls.assess_row(row) for row in old_rows])
        new_score = sum([cls.assess_row(row) for row in new_rows])

        return new_score - old_score

    @classmethod
    def assess_row(cls, row: tuple) -> int:
        repeats = {}
        for value in row:
            repeats[value] = repeats[value] + 1 if value in repeats else 1

        return sum([-1 for value in row if repeats[value] == 1])

    # makes shuffle and returns delta of sudoku mark
    @classmethod
    def make_change(cls, sudoku: Sudoku, old: int, new: int) -> int:
        old_rows = (sudoku.get_row(old), sudoku.get_col(old),
                    sudoku.get_row(new), sudoku.get_col(new))

        sudoku.data[old], sudoku.data[new] = sudoku.data[new], sudoku.data[old]

        new_rows = (sudoku.get_row(new), sudoku.get_col(new),
                    sudoku.get_row(old), sudoku.get_col(old))

        return cls.assess_change(old_rows, new_rows)

    @classmethod
    def unmake_change(cls, sudoku: Sudoku, old: int, new: int):
        sudoku.data[old], sudoku.data[new] = sudoku.data[new], \
                                             sudoku.data[old]

    @classmethod
    def candidates_for_shuffle(cls) -> tuple:
        x_base = 3 * randint(0, 2)
        y_base = 3 * randint(0, 2)

        x = Sudoku.conv2t1(
            (x_base + randint(0, 2), y_base + randint(0, 2)))
        y = Sudoku.conv2t1(
            (x_base + randint(0, 2), y_base + randint(0, 2)))

        return x, y
