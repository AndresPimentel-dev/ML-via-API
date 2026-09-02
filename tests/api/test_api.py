def test_register_login(client):
    response = client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    
    assert response.status_code == 201
    token = response.json()["access_token"]
    assert token is not None

def test_login_login(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    response = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

def test_obtener_contract(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    tokendecode = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {tokendecode}"}
    prediction_response = client.post("/api/v1/predictions/contracts", json={"company_description": "empresa de software"}, headers=headers)
    print(payload.json)
    assert prediction_response.status_code == 201
    assert prediction_response.json() == {"status": "Predicción creada y guardada"}

def test_obtener(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    tokendecode = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {tokendecode}"}
    prediction_response =  client.post("/api/v1/predictions/probability", json={"contract_name": "construccion", "user_budget": "20000"}, headers=headers)
    
    assert prediction_response.status_code == 201
    assert prediction_response.json() == {"status": "Predicción creada y guardada"}

def test_obtener_predicciones(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    token = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/v1/predictions/contracts", json={"company_description": "empresa de software"}, headers=headers)
    response = client.get("/readpredictions", headers=headers)
    
    assert response.status_code == 200
    assert response.json() is not None

def test_borrar_predicciones(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    tokendecode = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {tokendecode}"}

    response = client.delete(f"/delete_prediction/{1}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"status": "tarea borrada"}