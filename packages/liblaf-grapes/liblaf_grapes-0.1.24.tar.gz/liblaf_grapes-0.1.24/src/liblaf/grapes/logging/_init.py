from collections.abc import Sequence
from typing import Unpack

import loguru

from ._icecream import init_icecream
from ._init_loguru import init_loguru


def init_logging(
    *,
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
    **kwargs: Unpack["loguru.BasicHandlerConfig"],
) -> None:
    init_loguru(handlers=handlers, levels=levels, **kwargs)
    init_icecream()
