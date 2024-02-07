from datetime import datetime, timedelta

data = {}


def test_start_time():
    data["start_time"] = datetime.now()

    assert data["start_time"]


def test_end_time():
    data["start_time"] = datetime.now()

    data["end_time"] = datetime.now()

    assert data["end_time"] > data["start_time"]


def test_duration():
    data["start_time"] = datetime.now()

    data["end_time"] = datetime.now()

    data["duration"] = data["end_time"] - data["start_time"]

    assert data["duration"] > timedelta(seconds=0)
