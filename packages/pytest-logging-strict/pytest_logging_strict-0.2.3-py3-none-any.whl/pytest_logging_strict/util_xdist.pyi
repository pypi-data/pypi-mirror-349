from typing import Any

import pytest

# https://github.com/pytest-dev/pytest-xdist/issues/1121
from xdist.workermanage import WorkerController  # type: ignore

__all__ = (
    "is_xdist",
    "xdist_worker",
    "xdist_workerinput",
)

def is_xdist(config: pytest.Config) -> Any | None: ...
def xdist_worker(config: pytest.Config) -> dict[str, Any]: ...
def xdist_workerinput(node: WorkerController | pytest.Config) -> Any: ...
