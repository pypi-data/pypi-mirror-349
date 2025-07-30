from abc import ABC, abstractmethod
from typing import Any
import arc_agi_core as arc
import re
from IPython.display import display


class LLM(ABC):
    def __init__(self):
        self.client = self.init_client()

    @abstractmethod
    def init_client(self) -> Any:
        pass

    @abstractmethod
    def ask(self, prompt: str) -> str:
        pass

    @classmethod
    def encode_grid(self, grid: arc.Grid) -> str:
        return str(grid)

    @classmethod
    def decode_grid(self, string_repr: str) -> arc.Grid:
        sanitized_str = re.sub(r"[^\d \n]", "", string_repr).strip()
        return arc.Grid(
            [
                [int(c) for c in row.split(" ") if c != ""]
                for row in sanitized_str.split("\n")
            ]
        )

    @classmethod
    def encode_task(self, task: arc.Task, censor: bool = True) -> str:
        if censor:
            task.censor()

        return (
            "--Training Examples--\n"
            + "\n".join(
                f"Example {i + 1}: \nInput: \n{self.encode_grid(pair.input)}\nOutput: \n{self.encode_grid(pair.output)}\n"
                for i, pair in enumerate(task.train)
            )
            + "\n\n"
            + "--Test--\n"
            + "Input:\n"
            + self.encode_grid(task.test[0].input)
            + "\n"
        )

    def evaluate(self, task: arc.Task, max_retries: int = 3) -> bool:
        task.censor()

        prompt = f"""
You are participating in a puzzle solving competition. You are an expert at solving puzzles. 

Below is a list of input and output pairs with a pattern. Your goal is to identify the pattern or transformation in the training examples that maps the input to the output, then apply that pattern to the test input to give a final output. 

Respond in the format of the training output example grids. 

{self.encode_task(task)}

Output:
        """

        response = self.ask(prompt)
        attempt = 0
        prediction = None
        while attempt < max_retries:
            try:
                prediction = self.decode_grid(response)
                break
            except:
                attempt += 1
                response = self.ask(
                    'Your response cannot be parsed. Finalize your answer to a pure grid in format of the given example grids. Do not include any other formatting or words other than the answer grid itself. Do not include "output: " too. Just pure grid of numbers without formatting. '
                )
                continue

        display(prediction)

        task.uncensor()
        return task.test[0].output == prediction
