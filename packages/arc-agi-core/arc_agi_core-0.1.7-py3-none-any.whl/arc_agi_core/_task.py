from typing import List, Optional, Dict, Literal, Self, Union
from ._pair import Pair
from ._grid import Grid

from pathlib import Path
import json
from ._utils import Layout


class Task:
    """
    Represents an Abstract Reasoning Corpus (ARC) task.

    A Task consists of a set of training and test input-output pairs, and optionally a task ID.
    This class provides methods for loading from and saving to JSON, as well as for converting
    to and from dictionary representations. It also supports censoring and uncensoring of test outputs.

    Attributes:
        train (List[Pair]): List of training input-output pairs.
        test (List[Pair]): List of test input-output pairs.
        task_id (Optional[str]): Unique identifier for the task, if available.

    Methods:
        from_dict(task_dict, task_id): Create a Task from a dictionary.
        to_dict(): Convert the Task to a dictionary.
        from_json(file_path): Load a Task from a JSON file.
        save_as_json(path): Save the Task to a JSON file.
        inputs: List of all input grids (train and test).
        outputs: List of all output grids (train and test), censored outputs will be None.
        censor(): Censor the outputs of the test pairs.
        uncensor(): Uncensor the outputs of the test pairs.
        __repr__(): String representation of the Task.
        __str__(): String representation (same as __repr__).
        _repr_html_(): HTML representation for Jupyter/IPython.
    """

    def __init__(
        self,
        train: List[Pair],
        test: List[Pair],
        task_id: Optional[str] = None,
    ) -> None:
        """
        Initializes a Task.

        Args:
            train (List[Pair]): List of training input-output pairs.
            test (List[Pair]): List of test input-output pairs.
            task_id (Optional[str]): Unique identifier for the task, if available.

        Raises:
            TypeError: If any element in train or test is not a Pair.
        """
        if not all(isinstance(pair, Pair) for pair in train):
            raise TypeError("All elements in 'train' must be Pair objects.")
        if not all(isinstance(pair, Pair) for pair in test):
            raise TypeError("All elements in 'test' must be Pair objects.")

        self.train = train
        self.test = test
        self.task_id = task_id

    @classmethod
    def from_dict(
        cls,
        task_dict: Dict[
            Literal["train", "test"],
            List[Dict[Literal["input", "output"], List[List[int]]]],
        ],
        task_id: Optional[str] = None,
    ) -> Self:
        """
        Creates a Task instance from a dictionary.

        Args:
            task_dict (dict): Dictionary with 'train' and 'test' keys, each mapping to a list of
                dictionaries with 'input' and 'output' keys (2D lists of ints).
            task_id (Optional[str]): Optional task identifier.

        Returns:
            Task: The constructed Task instance.

        Raises:
            ValueError: If the dictionary format is invalid.
        """
        try:
            train_pairs = [
                Pair(pair["input"], pair["output"]) for pair in task_dict["train"]
            ]
            test_pairs = [
                Pair(pair["input"], pair["output"]) for pair in task_dict["test"]
            ]
            return cls(train_pairs, test_pairs, task_id)
        except (TypeError, KeyError) as e:
            raise ValueError(f"Invalid task dictionary format: {e}") from e

    def to_dict(self) -> Dict[str, List[Dict[str, List[List[int]]]]]:
        """
        Converts the Task to a dictionary format.

        Returns:
            dict: Dictionary with 'train' and 'test' keys, each mapping to a list of
                dictionaries with 'input' and 'output' keys.
        """
        return {
            "train": [
                {"input": pair.input.to_list(), "output": pair.output.to_list()}
                for pair in self.train
            ],
            "test": [
                {"input": pair.input.to_list(), "output": pair.output.to_list()}
                for pair in self.test
            ],
        }

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> Self:
        """
        Creates a Task instance from a JSON file.

        Args:
            file_path (str | Path): Path to the JSON file.

        Returns:
            Task: The loaded Task instance.

        Raises:
            ValueError: If loading or parsing fails.
        """
        file_path = Path(file_path)
        task_id = file_path.stem
        try:
            with file_path.open("r") as f:
                task_data = json.load(f)
            return cls.from_dict(task_data, task_id)
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Error loading Task from JSON '{file_path}': {e}") from e

    def save_as_json(self, path: Union[str, Path]) -> None:
        """
        Saves the Task to a JSON file.

        Args:
            path (str | Path): Destination file path.

        Raises:
            IOError: If saving fails.
        """
        path = Path(path)
        try:
            with path.open("w") as f:
                json.dump(self.to_dict(), f, indent=4)
            print(f"Task saved to '{path}'")
        except IOError as e:
            raise IOError(f"Error saving Task to JSON '{path}': {e}") from e

    @property
    def inputs(self) -> List[Grid]:
        """
        Returns a list of all input grids (train and test).

        Returns:
            List[Grid]: All input grids in the task.
        """
        return [pair.input for pair in self.train + self.test]

    @property
    def outputs(self) -> List[Optional[Grid]]:
        """
        Returns a list of all output grids (train and test). Censored outputs will be None.

        Returns:
            List[Optional[Grid]]: All output grids in the task.
        """
        return [pair.output for pair in self.train + self.test]

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the task, including all train and test pairs.

        Returns:
            str: String representation of the Task.
        """
        train_repr = Layout(
            *[
                Layout(
                    Layout(
                        f"INPUT {i}", pair.input, direction="vertical", align="center"
                    ),
                    " -> ",
                    Layout(
                        f"OUTPUT {i}",
                        pair.output if pair.output else "*CENSORED*",
                        direction="vertical",
                        align="center",
                    ),
                )
                for i, pair in enumerate(self.train)
            ],
            direction="vertical",
        )
        test_repr = Layout(
            *[
                Layout(
                    Layout(
                        f"INPUT {i}", pair.input, direction="vertical", align="center"
                    ),
                    " -> ",
                    Layout(
                        f"OUTPUT {i}",
                        pair.output if not pair._is_censored else "*CENSORED*",
                        direction="vertical",
                        align="center",
                    ),
                )
                for i, pair in enumerate(self.test)
            ],
            direction="vertical",
        )
        width = max(train_repr.width, test_repr.width)
        title = f"< Task{' ' + self.task_id if self.task_id else ''} >".center(
            width, "="
        )
        train_title = " Train ".center(width, "-")
        test_title = " Test ".center(width, "-")

        return repr(
            Layout(
                title,
                train_title,
                train_repr,
                test_title,
                test_repr,
                direction="vertical",
            )
        )

    def __str__(self) -> str:
        """
        Returns the same string representation as __repr__.

        Returns:
            str: String representation of the Task.
        """
        return self.__repr__()

    def _repr_html_(self):
        """
        Returns an HTML representation of the task for Jupyter/IPython.

        Returns:
            str: HTML string.
        """
        return (
            '<div style="display: flex; flex-direction: column; align-items: center; width: fit-content; border: solid 2px grey; border-radius: 0.5rem; padding: 0.5rem; margin: auto;">'
            f'<label style="border-bottom: solid 1px grey; width: 100%; text-align: center; ">Task{f" - {self.task_id}" if self.task_id else ""}</label>'
            "<table>"
            + " ".join(
                f'<tr style="background: transparent" ><td style="text-align: center">train[{i}].input</td><td></td><td style="text-align: center">train[{i}].output</td></tr>'
                f'<tr style="background: transparent"><td>{pair.input._repr_html_()}</td><td> → </td><td>{pair.output._repr_html_()}</td></tr>'
                for i, pair in enumerate(self.train)
            )
            + '<tr style="border-bottom: dashed 1px grey; height: 1rem;"></tr>'
            + " ".join(
                f'<tr style="background: transparent"><td style="text-align: center">test[{i}].input</td><td></td><td style="text-align: center">test[{i}].output</td></tr>'
                f'<tr style="background: transparent"><td>{pair.input._repr_html_()}</td>'
                "<td> → </td>"
                f"<td>{pair.output._repr_html_()}</td>"
                if not pair._is_censored
                else '<td style="text-align: center; vertical-align: middle;">?</td>'
                "</tr>"
                for i, pair in enumerate(self.test)
            )
            + "</table>"
            + "</div>"
        )

    def censor(self) -> None:
        """
        Censors the outputs of the testing pairs.
        """
        for pair in self.test:
            pair.censor()

    def uncensor(self) -> None:
        """
        Uncensors the outputs of the testing pairs.
        """
        for pair in self.test:
            pair.uncensor()
