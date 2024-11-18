from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# Obtener el token de acceso y asegurarse de que el usuario esté registrado
def get_token():
    # Intento de registro del usuario; si ya existe, se ignora el error
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    
    # Obtener el token para el usuario registrado
    response = client.post("/token", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    return response.json().get("access_token")

# Prueba para endpoint protegido con token válido
def test_protected_endpoint_with_valid_token():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Tienes acceso al contenido protegido"}

# Prueba para endpoint protegido sin token
def test_protected_endpoint_without_token():
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

# Prueba para endpoint protegido con token inválido
def test_protected_endpoint_with_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}




