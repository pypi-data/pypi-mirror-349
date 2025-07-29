"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

.. py:data:: item_marker
   :type: str
   :value: "logging_package_name"

   Name of a pytest marker. Takes one argument, a dotted path logger
   handlers package name
"""

from collections.abc import (
    Callable,
    Sequence,
)

import pytest

item_marker = "logging_package_name"


def _check_out(output: Sequence[str]) -> bool:
    """Separated to be testable and without printing a header line

    :param output: log entries
    :type output: collections.abc.Sequence[str]
    :returns: True has log entries otherwise False
    :rtype: bool
    """
    is_seq = (
        output is not None
        and isinstance(output, Sequence)
        and not isinstance(output, str)
    )
    if is_seq:
        if len(output) == 1 and not bool(output[0]):
            # [""]
            print("Nothing captured")
            ret = False
        else:
            seq_len = len(output)
            for i in range(seq_len):
                print(f"{i}: {output[i]}")
            ret = True
    else:
        ret = False

    return ret


@pytest.fixture()
def has_logging_occurred(caplog: pytest.LogCaptureFixture) -> Callable[[], bool]:
    """Display caplog capture text.

    Usage

    .. code-block: text

       import pytest
       # import your packages underscored name from package's constants module
       g_app_name = "my_package"

       @pytest.mark.logging_package_name(g_app_name)
       def test_something(logging_strict, has_logging_occurred):
           t_two = logging_strict()
           logger, loggers = t_two

           logger.info("Hi there")

           assert has_logging_occurred()

    .. seealso::

       https://github.com/pytest-dev/pytest/discussions/11011
       https://github.com/thebuzzstop/pytest_caplog/tree/master
       `pass params fixture <https://stackoverflow.com/a/44701916>`_

    """

    def _method() -> bool:
        """Check if there is at least one log message. Print log messages.

        :returns: True if logging occurred otherwise False
        :rtype: bool
        """
        output = caplog.text.rstrip("\n").split(sep="\n")
        print("\nCAPLOG:")
        ret = _check_out(output)

        return ret

    return _method
