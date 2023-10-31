import datetime

import pytest

from gitgus.utils.secret_store.mac_os import get_macos, set_macos

SERVICE_NAME = "gitgus_test"
KEY_NAME = "test_key"


@pytest.mark.skip(
    reason="In the pre-commit hook, there's some race condition. Find it."
)
def test_it_works():
    value = "test_value_" + str(datetime.datetime.now())

    set_macos(SERVICE_NAME, KEY_NAME, value)
    actual = get_macos(SERVICE_NAME, KEY_NAME)
    assert actual == value
