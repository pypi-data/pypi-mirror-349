from collections.abc import (
    Callable,
    Sequence,
)

import pytest

item_marker: str

def _check_out(output: Sequence[str]) -> bool: ...
@pytest.fixture()
def has_logging_occurred(caplog: pytest.LogCaptureFixture) -> Callable[[], bool]: ...
