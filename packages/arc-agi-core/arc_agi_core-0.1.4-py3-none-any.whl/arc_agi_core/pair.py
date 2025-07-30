from typing import Union, List, Optional, Dict
from .grid import Grid
from .utils import Layout

import warnings
from hashlib import sha256


class Pair:
    """
    Represents a single input-output pair for an ARC task.

    A Pair consists of an input grid and an output grid, and supports optional censoring
    of the output (for use in test sets where the output is hidden).

    Attributes:
        input (Grid): The input grid for the pair.
        output (Optional[Grid]): The output grid for the pair, or None if censored.

    Methods:
        censor(): Censor the output grid (hide it).
        uncensor(): Uncensor the output grid (reveal it).
        to_dict(): Convert the pair to a dictionary format.
        __hash__(): Compute a hash of the pair.
        __eq__(other): Check equality with another pair.
        __repr__(): Return a string representation.
        _repr_html_(): Return an HTML representation for Jupyter/IPython.
    """

    def __init__(
        self,
        input: Union[Grid, List[List[int]]],
        output: Union[Grid, List[List[int]]],
        censor: bool = False,
    ) -> None:
        """
        Initialize a Pair instance.

        Args:
            input (Grid | List[List[int]]): The input grid or nested list.
            output (Grid | List[List[int]]): The output grid or nested list.
            censor (bool): Whether to censor the output initially.
        """
        self.input = input if isinstance(input, Grid) else Grid(input)
        self.output = output if isinstance(output, Grid) else Grid(output)
        self._is_censored = censor

    @property
    def output(self) -> Optional[Grid]:
        """
        Get the output grid, or None if censored.

        Returns:
            Optional[Grid]: The output grid, or None if censored.

        Warns:
            UserWarning: If the output is censored.
        """
        if self._is_censored:
            warnings.warn(
                "`output` is censored. Call `.uncensor()` to gain access.",
                UserWarning,
                stacklevel=2,
            )
            return None
        return self._output

    @output.setter
    def output(self, grid: Union[Grid, List[List[int]]], censor: bool = False) -> None:
        """
        Set the output grid.

        Args:
            grid (Grid | List[List[int]]): The output grid or nested list.
            censor (bool): Whether to censor the output after setting.
        """
        self._output = grid if isinstance(grid, Grid) else Grid(grid)
        if censor:
            self.censor()

    def censor(self) -> None:
        """
        Censor the output grid (hide it).
        """
        self._is_censored = True

    def uncensor(self) -> None:
        """
        Uncensor the output grid (reveal it).
        """
        self._is_censored = False

    def _repr_html_(self) -> str:
        """
        Return an HTML representation of the pair for Jupyter/IPython.

        Returns:
            str: HTML string.
        """
        return (
            '<div class="pair" style="display: flex; align-items: center; gap: 1rem; margin: auto;">'
            f"<div>{self.input._repr_html_()}</div>"
            "<div> → </div>"
            f"<div>{self.output._repr_html_()}</div>"
            "</div>"
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the pair, showing input and output.

        Returns:
            str: String representation.
        """
        return repr(
            Layout(
                Layout(
                    "INPUT",
                    repr(self.input),
                    direction="vertical",
                    align="center",
                ),
                "->",
                Layout(
                    "OUTPUT",
                    repr(self.output) if self.output else "*CENSORED*",
                    direction="vertical",
                    align="center",
                ),
                align="center",
            )
        )

    def to_dict(self) -> Dict[str, List[List[int]]]:
        """
        Convert the pair to a dictionary format.

        Returns:
            Dict[str, List[List[int]]]: Dictionary with 'input' and 'output' keys.
        """
        return {"input": self.input.to_list(), "output": self.output.to_list()}

    def __hash__(self) -> int:
        """
        Compute a hash of the pair based on input and output.

        Returns:
            int: Hash value.
        """
        h = sha256()
        h.update(str(hash(self.input)).encode())
        h.update(str(hash(self.output)).encode())
        return int(h.hexdigest(), 16)

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Pair.

        Args:
            other (object): Another Pair instance.

        Returns:
            bool: True if input and output grids are equal.

        Raises:
            NotImplementedError: If other is not a Pair.
        """
        if not isinstance(other, Pair):
            raise NotImplementedError
        return (self.input == other.input) and (self.output == other.output)
