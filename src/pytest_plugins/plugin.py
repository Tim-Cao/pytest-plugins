from datetime import datetime

import pytest

from pytest_plugins import smtp

data = {
    "failed": 0,
    "passed": 0,
}


def pytest_addoption(parser):
    parser.addini("when_to_send", help="When to send test results")

    parser.addini("sender_email", help="The smtp sender email address")

    parser.addini("sender_auth_code", help="The smtp sender auth code")

    parser.addini("receiver_email", help="The receiver email address")


def pytest_collection_finish(session: pytest.Session):
    data["total"] = len(session.items)


def pytest_configure(config: pytest.Config):
    data["start_time"] = datetime.now()

    data["when_to_send"] = config.getini("when_to_send")
    data["sender_email"] = config.getini("sender_email")
    data["sender_auth_code"] = config.getini("sender_auth_code")
    data["receiver_email"] = config.getini("receiver_email")


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_unconfigure():
    data["end_time"] = datetime.now()

    data["duration"] = data["end_time"] - data["start_time"]

    data["passed_ratio"] = data["passed"] / data["total"] * 100

    data["passed_ratio"] = f'{data["passed_ratio"]:.2f}%'

    send_result()


def send_result():
    if data["when_to_send"] == "on_fail" and data["failed"] == 0:
        return

    if (
        not data["sender_email"]
        or not data["sender_auth_code"]
        or not data["receiver_email"]
    ):
        return

    content = f"""
<html>
<head>
</head>
<body>
    <p>Total Tests: {data["total"]}</p>
    <p>Testing Duration: {data["duration"]}s</p>
    <p>Passed Number: <span style="color: green;">{data["passed"]}</span></p>
    <p>Failed Number: <span style="color: red;">{data["failed"]}</span></p>
    <p>Passed Ratio: {data["passed_ratio"]}s</p>
</body>
</html>
    """

    subject = f'Test Results - {data["start_time"]}'

    smtp.send_email(
        content,
        data["sender_auth_code"],
        data["sender_email"],
        subject,
        data["receiver_email"],
    )

    data["sent"] = 1
