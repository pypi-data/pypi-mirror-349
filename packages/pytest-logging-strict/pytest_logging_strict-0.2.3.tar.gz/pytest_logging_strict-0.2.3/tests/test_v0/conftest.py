"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

implementation v0 fixtures

"""

import pytest


@pytest.fixture(scope="session")
def impl_version_no() -> str:
    """Plugin implementation version_no

    :returns: version no
    :rtype: str
    """
    return "0"
