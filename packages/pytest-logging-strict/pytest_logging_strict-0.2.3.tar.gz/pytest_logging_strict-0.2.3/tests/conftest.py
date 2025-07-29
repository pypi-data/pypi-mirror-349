"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

Enable plugin pytester

.. py:data:: pytest_plugins
   :type: str
   :value: ["pytester", "logging_strict"]

   pytest plugins to loader

.. seealso::

   `pytest plugins list <https://docs.pytest.org/en/stable/reference/plugin_list.html>`_

   `logassert <https://pypi.org/project/logassert/>`_

   `logot <https://github.com/etianen/logot/blob/main/logot/_pytest.py>`_

"""

import pytest

pytest_plugins = [
    "pytester",
    "logging_strict",
]


def pytest_report_header() -> str:
    """Add package versioning info to pytest header

    ``_version.py`` is not tracked in git. In a clean environment,
    ``_version.py`` will not yet exist.

    To create it, run :code:`python -m build`

    :returns: plugin or plugin dependencies versions
    :rtype: str
    """
    try:
        from logging_strict._version import __version__ as ls_version

        from pytest_logging_strict._version import __version__ as pls_version
    except ImportError:
        ret = ""
    else:
        ret = f"pytest-logging-strict: {pls_version} dependency logging-strict: {ls_version}"

    return ret


@pytest.fixture(
    params=[
        True,  # xdist enabled, active
        False,  # xdist enabled, inactive
        None,  # xdist disabled
    ],
)
def xdist_args(request: pytest.FixtureRequest):
    """Fixture of various states of pytest-xdist. On off or None"""
    if request.param is None:
        return ["-p", "no:xdist"]
    return ["-n", "auto"] if request.param else []
