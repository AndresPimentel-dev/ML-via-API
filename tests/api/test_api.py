def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    
    assert response.status_code == 201
    token = response.json()["access_token"]
    assert token is not None

def test_login(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    response = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

def test_invalid_credentials(client):

    response = client.post("/api/v1/predictions/contracts", json={"company_description": "empresa de software"})

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_create_prediction(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    tokendecode = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {tokendecode}"}
    prediction_response = client.post("/api/v1/predictions/contracts", json={"company_description": "empresa de software"}, headers=headers)
    assert prediction_response.status_code == 201
    assert prediction_response.json() == {"status": "Predicción creada y guardada"}

def test_get_predictions(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    tokendecode = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {tokendecode}"}
    prediction_response =  client.post("/api/v1/predictions/probability", json={"contract_name": "construccion", "user_budget": "20000"}, headers=headers)
    
    assert prediction_response.status_code == 201
    assert prediction_response.json() == {"status": "Predicción creada y guardada"}

def test_get_contracs(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    token = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/v1/predictions/contracts", json={"company_description": "empresa de software"}, headers=headers)
    response = client.get("/api/v1/predictions", headers=headers)
    
    assert response.status_code == 200
    assert response.json() is not None

def test_delete_own_prediction(client):
    client.post("/api/v1/auth/register", json={"username": "tesiuiouotuser", "email": "email@gmiuuiooail.com", "password": "pasuiowword"})
    payload = client.post("/api/v1/auth/login", data={"username": "tesiuiouotuser", "password": "pasuiowword"})
    tokendecode = payload.json()["access_token"]
    headers = {"Authorization": f"Bearer {tokendecode}"}

    response = client.delete(f"/api/v1/predictions/{1}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"status": "tarea borrada"}