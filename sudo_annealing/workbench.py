import random
from typing import List

from IPython.display import clear_output, display
from ipywidgets import BoundedIntText, Dropdown, VBox, Button, HBox, Output, interact, SelectionSlider, Label

from sudo_annealing.puzzle_pack import SudokuPack
from sudo_annealing.solvers.abstract import AbstractSolver, NonSteppingSolver


class workbench(VBox):
    def __init__(self, algorithms: List[AbstractSolver], puzzle_pack: SudokuPack):
        super().__init__()

        self.algorithms = algorithms
        self.puzzle_pack = puzzle_pack

        self.algorithm_dropdown = Dropdown(
            options={a.display_name(): a for a in algorithms},
            description='Algorithm:',
        )

        self.puzzle_id_input = BoundedIntText(
            value=random.randrange(0, len(puzzle_pack)),
            min=0,
            max=len(puzzle_pack) - 1,
            description='Puzzle:',
        )

        self.random_btn = Button(description='Random')
        self.random_btn.on_click(self.random_puzzle)

        self.run_btn = Button(description='Run')
        self.run_btn.on_click(self.run)

        self.out = Output()
        self.result = None

        self.children = [
            self.algorithm_dropdown,
            HBox([self.puzzle_id_input, self.random_btn]),
            self.run_btn,
            self.out,
        ]

    def random_puzzle(self, *args):
        self.puzzle_id_input.value = random.randint(
            self.puzzle_id_input.min, self.puzzle_id_input.max)

    def run(self, *args):
        self.run_btn.disabled = True
        try:
            with self.out:
                clear_output(wait=True)
                algorithm = self.algorithm_dropdown.get_interact_value()
                puzzle_id = self.puzzle_id_input.get_interact_value()
                puzzle = self.puzzle_pack[puzzle_id]
                self.result = algorithm.solve(puzzle.clone())
                self.display_result()
        finally:
            self.run_btn.disabled = False

    def display_result(self):
        if len(self.result) == 2:
            orig = self.result[0][1]
            solv = self.result[1][1]
            display(Label('Problem:'))
            display(orig)
            display(Label('Solution:'))
            display(solv)
        else:
            interact(
                self.result.f,
                i=SelectionSlider(
                    options={iteration: i for i, (iteration, _) in enumerate(self.result.data)},
                    description='Iteration',
                ),
            )
