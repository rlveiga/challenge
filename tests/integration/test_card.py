import json

def test_get_card_info(test_client, init_db, token):
    response = test_client.get('/cards/3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['card']['name'] == 'Deletable card'
    assert len(data['collections']) == 1
    
# Creates card, adding it to a collection (plus the default collection) if necessary
def test_create_card(test_client, init_db, token):
    response = test_client.post('/cards/', json=dict(card_type='black', name='Something clever', collection_id=3), headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card created'
    assert type(data['card']) == dict
    assert data['card']['card_type'] == 'black'
    assert data['card']['name'] == 'Something clever'
    assert data['card']['created_by'] == 1
    assert type(data['card']['collections']) == list
    assert data['card']['collections'][0]['name'] == 'My cards'
    assert data['card']['collections'][1]['name'] == 'Test collection'
    assert data['card']['collections'][0]['created_by'] == 1

def test_delete_card(test_client, init_db, token):
    response = test_client.delete('/cards/3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card deleted'
    assert data['card'] == {}

def test_delete_unexisting_card(test_client, init_db, token):
    response = test_client.delete('/cards/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card not found'

def test_delete_unauthorized_card(test_client, init_db, token):
    response = test_client.delete('/cards/4', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this card'

# Add to collection tests
def test_add_to_collection(test_client, init_db, token):
    response = test_client.post('/cards/1/add_collection/6', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card added to collection'

def test_add_to_collection_again(test_client, init_db, token):
    response = test_client.post('/cards/1/add_collection/6', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 409

    assert data['message'] == 'Card already belongs to this collection'

def test_add_to_unexisting_collection(test_client, init_db, token):
    response = test_client.post('/cards/1/add_collection/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'

def test_add_unexisting_card_to_collection(test_client, init_db, token):
    response = test_client.post('/cards/42/add_collection/3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card not found'

def test_add_unauthorized_card_to_collection(test_client, init_db, token):
    response = test_client.post('/cards/2/add_collection/3', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this card'

def test_add_to_unauthorized_collection(test_client, init_db, token):
    response = test_client.post('/cards/1/add_collection/4', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this collection'

# Remove from collection tests
def test_remove_from_collection(test_client, init_db, token):
    response = test_client.delete('/cards/1/remove_collection/6', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 200

    assert data['message'] == 'Card removed from collection'

def test_remove_from_collection_again(test_client, init_db, token):
    response = test_client.delete('/cards/1/remove_collection/6', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card does not belong to this collection'

def test_remove_from_unexisting_collection(test_client, init_db, token):
    response = test_client.delete('/cards/1/remove_collection/42', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Collection not found'

def test_remove_unexisting_card_from_collection(test_client, init_db, token):
    response = test_client.delete('/cards/42/remove_collection/6', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 404

    assert data['message'] == 'Card not found'

def test_remove_unauthorized_card_from_collection(test_client, init_db, token):
    response = test_client.delete('/cards/2/remove_collection/6', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this card'

def test_remove_from_unauthorized_collection(test_client, init_db, token):
    response = test_client.delete('/cards/1/remove_collection/4', headers={'access-token': token})

    data = json.loads(response.data)

    assert response.status_code == 403

    assert data['message'] == 'You do not own this collection'