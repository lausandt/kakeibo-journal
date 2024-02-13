"""
This test suite is not mocked due to the small seize of the database
Instead actions are taken on the database and removed at the end of the module
"""


def test_create_user(client, test_user):
    response = client.post(url='/users/register', json=test_user)
    assert response.status_code == 200


def test_get_users(client):
    response = client.get(url='/users/')
    assert response.status_code == 200


def test_get_user_me(client, user_access_token):
    response = client.get(
        url=f'/users/me',
        headers={'Authorization': f'Bearer {user_access_token}'},
    )
    assert response.status_code == 200


def test_get_user_by_id(client, user_access_token):
    user = client.get(
        url=f'/users/me',
        headers={'Authorization': f'Bearer {user_access_token}'},
    )
    id = user.json()['id']
    response = client.get(
        url=f'users/user by id/{id}',
        headers={'Authorization': f'Bearer {user_access_token}'},
    )
    assert response.status_code == 200

def test_user_by_ne_id(client, user_access_token):
    id = 1_000_000_000
    response = client.get(
        url=f'users/user by id/{id}',
        headers={'Authorization': f'Bearer {user_access_token}'},
    )
    assert response.status_code == 404

def test_update_me(client, user_access_token):
    stub = {
        'full_name': 'King George',
        'password': 'string',
        'username': 'test@user.com',
    }
    response = client.patch(
        url='/users/update me',
        headers={'Authorization': f'Bearer {user_access_token}'},
        json=stub,
    )
    assert response.json()['full_name'] == 'King George'
    assert response.status_code == 200


def test_delete_user(client, user_access_token):
    user = client.get(
        url=f'/users/me',
        headers={'Authorization': f'Bearer {user_access_token}'},
    )
    id = user.json()['id']
    response = client.delete(
        f'/users/remove user/{id}',
        headers={'Authorization': f'Bearer {user_access_token}'},
    )
    assert response.status_code == 200
