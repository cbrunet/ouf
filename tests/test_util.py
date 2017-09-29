import pytest
from ouf.util import humanize


TEST_CASES = [
    (0, "0 bytes"),
    (1000, "1000 bytes"),
    (1023, "1023 bytes"),
    (1024, "1K"),
    (1024000, "1000K"),
    (1048576, "1M"),
]


@pytest.fixture(scope='function', params=TEST_CASES)
def numbers(request):
    return request.param


def test_humanize(numbers):
    s = humanize(numbers[0])
    assert s == numbers[1]
