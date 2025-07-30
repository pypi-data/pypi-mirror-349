import functools

from loguru import logger

from ._base import Callback, TimerRecords


def log_record(
    *,
    depth: int = 1,
    elapsed_threshold: float = 1e-3,
    index: int = -1,
    level: int | str = "DEBUG",
) -> Callback:
    return functools.partial(
        _log_record,
        depth=depth,
        elapsed_threshold=elapsed_threshold,
        index=index,
        level=level,
    )


def log_summary(*, depth: int = 1, level: int | str = "INFO") -> Callback:
    return functools.partial(_log_summary, depth=depth, level=level)


def _log_record(
    timer: TimerRecords,
    *,
    depth: int = 1,
    elapsed_threshold: float = 1e-3,
    index: int = -1,
    level: int | str = "DEBUG",
) -> None:
    if timer.elapsed() < elapsed_threshold:
        return
    logger.opt(depth=depth).log(level, timer.human_record(index=index))


def _log_summary(
    timer: TimerRecords, *, depth: int = 1, level: int | str = "INFO"
) -> None:
    logger.opt(depth=depth).log(level, timer.human_summary())


__all__ = ["log_record", "log_summary"]
