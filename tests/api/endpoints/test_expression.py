from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_simple_derivative():
    response = client.post("/expression", json={"expr": "2*x", "diff_var": "x"})
    assert response.status_code == 200
    assert response.json() == {"derivative": "2"}


def test_complex_derivartive():
    response = client.post("/expression", json={"expr": "(ln(x) ^ 2) * sin(x)", "diff_var": "x"})
    assert response.status_code == 200
    assert response.json() == {"derivative": "(x*log(x)*cos(x) + 2*sin(x))*log(x)/x"}


def test_invalid_derivative():
    response = client.post(
        "/expression", json={"expr": "((ln(x) ^ 2) * sin(x)", "diff_var": "x"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid parenthesis in position 0"}


def test_nonexistent_route():
    response = client.post(
        "/test", json={"expr": "((ln(x) ^ 2) * sin(x)", "diff_var": "x"}
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

