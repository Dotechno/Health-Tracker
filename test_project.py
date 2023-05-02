

def test_index_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_response(client):
    response = client.get('/')
    assert b"Dotechno" in response.data


def test_register_200(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_register_response(client):
    response = client.get('/register')
    assert b"Register" in response.data

    # post
    response = client.post('/register', data=dict(
        username='test',
        password='test',
        roles='admin'
    ), follow_redirects=True)
    assert response.status_code == 200
    # check if redirects to login
    assert b"Login" in response.data


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


if __name__ == '__main__':
    unittest.main()
