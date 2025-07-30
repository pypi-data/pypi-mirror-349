from rich.console import Console, RenderableType
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    Task,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Column
from rich.text import Text

from liblaf.grapes import human as _human
from liblaf.grapes import pretty


class RateColumn(ProgressColumn):
    """RateColumn is a subclass of ProgressColumn that represents the rate of progress for a given task."""

    unit: str = "it"
    """The unit of measurement for the progress bar."""

    def __init__(self, unit: str = "it", table_column: Column | None = None) -> None:
        """.

        Args:
            unit: The unit of measurement for the progress bar.
            table_column: The table column associated with the progress bar.
        """
        super().__init__(table_column)
        self.unit = unit

    def render(self, task: Task) -> RenderableType:
        """Render the progress speed of a given task.

        Args:
            task: The task for which the speed is to be rendered.

        Returns:
            A text object representing the speed of the task.
        """
        if not task.speed:
            return Text(f"?{self.unit}/s", style="progress.data.speed")
        human: str = _human.human_throughout(task.speed, self.unit)
        return Text(human, style="progress.data.speed")


def progress(
    *columns: str | ProgressColumn,
    console: Console | None = None,
    total_is_unknown: bool = False,
) -> Progress:
    if not columns:
        columns: list[ProgressColumn] = [
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
        ]
        if total_is_unknown:
            columns += [
                MofNCompleteColumn(),
                "[",
                TimeElapsedColumn(),
                ",",
                RateColumn(),
                "]",
            ]
        else:
            columns += [
                TaskProgressColumn(),
                "[",
                TimeElapsedColumn(),
                "<",
                TimeRemainingColumn(),
                ",",
                RateColumn(),
                "]",
            ]
    console = console or pretty.get_console("stderr")
    progress = Progress(*columns, console=console)
    return progress
