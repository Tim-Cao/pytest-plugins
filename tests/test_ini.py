from pathlib import Path

import pytest

from pytest_plugins import plugin

pytest_plugins = "pytester"


@pytest.fixture(autouse=True)
def mock():
    back_up = plugin.data
    plugin.data = {
        "failed": 0,
        "passed": 0,
    }

    yield

    plugin.data = back_up


@pytest.mark.parametrize("when_to_send", ["every_time", "on_fail"])
def test_when_to_send(when_to_send, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")

    config_path.write_text(
        f"""
[pytest]
when_to_send = {when_to_send}

sender_email = example@qq.com

sender_auth_code = test

receiver_email = example@qq.com
"""
    )

    config = pytester.parseconfig(config_path)

    assert config.getini("when_to_send") == when_to_send

    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )

    pytester.runpytest("-c", str(config_path))

    if when_to_send == "every_time":
        assert plugin.data["sent"] == 1
    else:
        assert plugin.data.get("sent") is None


@pytest.mark.parametrize("sender_email", ["example@qq.com", ""])
def test_sender_email(sender_email, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")

    config_path.write_text(
        f"""
[pytest]
when_to_send = every_time

sender_email = {sender_email}

sender_auth_code = test

receiver_email = example@qq.com
    """
    )

    config = pytester.parseconfig(config_path)

    assert config.getini("sender_email") == sender_email

    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )

    pytester.runpytest("-c", str(config_path))

    if sender_email:
        assert plugin.data["sent"] == 1
    else:
        assert plugin.data.get("sent") is None
