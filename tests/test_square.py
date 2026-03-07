from app.app import app


def test_index_get_returns_form_page():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Enter a number" in resp.data or b"number" in resp.data


def test_square_valid_positive_integer():
    client = app.test_client()
    resp = client.post("/", data={"number": "7"})
    assert resp.status_code == 200
    assert b"49" in resp.data


def test_square_zero():
    client = app.test_client()
    resp = client.post("/", data={"number": "0"})
    assert resp.status_code == 200
    assert b"0" in resp.data


def test_square_invalid_non_numeric_input():
    client = app.test_client()
    resp = client.post("/", data={"number": "abc"})
    assert resp.status_code == 200
    assert b"Please enter a valid non-negative integer." in resp.data


def test_square_empty_input():
    client = app.test_client()
    resp = client.post("/", data={"number": ""})
    assert resp.status_code == 200
    assert b"Please enter a valid non-negative integer." in resp.data
