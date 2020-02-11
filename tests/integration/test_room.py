import json
from app.models.room import Room

def test_get_user_room(test_client, init_db, token):
    response = test_client.get('/rooms/', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    
    assert type(data['room']) is dict
    assert data['room']['code'] == 'test1'

def test_leave_room_as_host(test_client, init_db, token):
    response = test_client.delete('/rooms/test1', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['room']['status'] == 'inactive'

def test_join_unexisting_room(test_client, init_db, token):
    response = test_client.post('/rooms/four2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Room not found'

def test_join_room(test_client, init_db, token):
    response = test_client.post('/rooms/test2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['room']['data']['id'] == 2
    assert len(data['room']['users']) == 2

def test_join_another_room(test_client, init_db, token):
    response = test_client.post('/rooms/test3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403
    assert data['message'] == 'User already belongs to a room'

def test_leave_room(test_client, init_db, token):
    response = test_client.delete('/rooms/test2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['room']['status'] == 'active'

def test_leave_room_not_allowed(test_client, init_db, token):
    response = test_client.delete('/rooms/test2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 422

    assert data['message'] == 'User is not in this room'

def test_leave_unexisting_room(test_client, init_db, token):
    response = test_client.delete('/rooms/four2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Room not found'

def test_create_existing_room(test_client, init_db, token):
    response = test_client.post('/rooms/', json=dict(code='test2'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403
    assert data['message'] == "Room 'test2' is already in use"

def test_create_room(test_client, init_db, token):
    response = test_client.post('/rooms/', json=dict(code='abcde'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert type(data['room']) == dict

def test_create_another_room(test_client, init_db, token):
    response = test_client.post('/rooms/', json=dict(code='abcdf'), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403
    assert data['message'] == 'User already belongs to a room'

def test_search_room(test_client, init_db, token):
    response = test_client.get('/rooms/test3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['room']['data']['code'] == 'test3'

def test_search_unexisting_room(test_client, init_db, token):
    response = test_client.get('/rooms/random', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Room not found'
    
def test_get_unexisting_room_players(test_client, init_db, token):
    response = test_client.get('/rooms/four2', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Room not found'