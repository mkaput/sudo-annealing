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
        result = cls.do_solve(0, 0, sudoku, s)
        if not result:
            raise Exception("sudoku not solvable!")
        return s

    @classmethod
    def do_solve(cls, it: int, c: int, sudoku: Sudoku,
                 sol: SudokuSolution) -> bool:
        cls.fill_board(sudoku)
        sol.append((it, sudoku.clone()))
        it += 1

        mark = cls.assess_board(sudoku)
        print(mark)
        temp = 1e20

        while temp > 1e-2 or mark != 0:

            x_base = 3 * randint(0, 2)
            y_base = 3 * randint(0, 2)

            old = Sudoku.conv2t1((x_base + randint(0, 2), y_base + randint(0, 2)))
            new = Sudoku.conv2t1((x_base + randint(0, 2), y_base + randint(0, 2)))

            if sudoku.masked(old) and sudoku.masked(new):
                temp /= 1.5
                sudoku.data[old], sudoku.data[new] = sudoku.data[new], \
                                                     sudoku.data[old]
                delta = cls.assess_board(sudoku) - mark

                if delta < 0:
                    mark += delta
                    it += 1
                    sol.append((it, sudoku.clone()))
                elif random() < exp( (-delta) / temp):
                    mark += delta
                else:
                    sudoku.data[old], sudoku.data[new] = sudoku.data[new], \
                                                         sudoku.data[old]


        if mark == 0:
            sol.append((it + 1, sudoku.clone()))
            return True
        return False

    @classmethod
    def fill_board(cls, sudoku: Sudoku):
        [cls.fill_box(sudoku, 3*i, 3*j)
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

    @classmethod
    def assess_board(cls, sudoku: Sudoku) -> int:
        mark = 162

        for i in range(81):
            if sudoku.get_row(i).count(sudoku.data[i]) == 1:
                mark -= 1
            if sudoku.get_col(i).count(sudoku.data[i]) == 1:
                mark -= 1
        return mark

    # @classmethod
    # def assess_change(cls, sudoku: Sudoku, x: int, y: int) -> int:
    #     delta = 0
    #     xrows = [sudoku.get_row(x), sudoku.get_col(x)]
    #     yrows = [sudoku.get_row(y), sudoku.get_col(y)]
    #
    #     xval = sudoku.data[x]
    #     yval = sudoku.data[y]
    #
    #     for row in xrows:
    #         if row.count(xval) == 1 and row.count(yval) != 0:
    #             delta -=1
    #         elif row.count(xval) != 1 and row.count(yval) == 0:
    #             delta +=1
    #
    #     for row in yrows:
    #         if row.count(yval) == 1 and row.count(xval) != 0:
    #             delta -=1
    #         elif row.count(yval) != 1 and row.count(xval) == 0:
    #             delta +=1
    #
    #     return delta
