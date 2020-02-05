from flask import jsonify, request

from app import db
from app.models.card import Card, CardAssociation
from app.models.collection import Collection
from app.models.schemas import card_share_schema, cards_share_schema, collection_share_schema, collections_share_schema, user_share_schema, users_share_schema, room_share_schema

from . import card
from app.wrappers import token_required
from functools import wraps

@card.route('/<card_id>', methods=['GET'])
@token_required
def get_card_info(user, card_id):
  card = Card.query.filter_by(id=card_id).first()

  if card is None:
    return jsonify({'message': 'Card does not exist'}), 404

  res = {
    'card': card_share_schema.dump(card),
    'collections': collections_share_schema.dump(card.collections)
  } 

  return jsonify(res)

@card.route('/', methods=['POST'])
@token_required
def create_card(user):
    body = request.get_json()

    if(body['name'] and body['card_type']):
        new_card = Card(name=body['name'], card_type=body['card_type'], created_by=user.id)

        db.session.add(new_card)
        db.session.commit()

        new_association = CardAssociation(
            card_id=new_card.id,
            collection_id=Collection.query.filter_by(created_by=user.id, name='My cards').first().id
            )

        db.session.add(new_association)
        db.session.commit()

        card_response = card_share_schema.dump(new_card)
        card_response['collections'] = collections_share_schema.dump(new_card.collections)
        
        res = {
            'message': 'Card created',
            'card': card_response
        }

        return jsonify(res)

    else:
        res = {
            'message': 'Missing attributes'
        }

        return jsonify(res), 422

@card.route('/', methods=['GET'])
@token_required
def get_user_cards(user):
    cards = Card.query.filter_by(created_by=user.id).all()

    cards_res = []

    for card in cards:
        cards_res.append({
            'data': card_share_schema.dump(card),
            'collections': collections_share_schema.dump(card.collections)
        })

    res = {
        'cards': cards_res
    }

    return jsonify(res)

@card.route('/<card_id>', methods=['DELETE'])
@token_required
def delete_card(user, card_id):
    card = Card.query.filter_by(id=card_id).first()

    if card is None:
        res = {
            'message': 'Card not found'
        }

        return jsonify(res), 404

    else:
        if card.created_by != user.id:
            res = {
                'message': 'You do not own this card'
            }

            return jsonify(res), 403

        else:
            CardAssociation.query.filter_by(card_id=card.id).delete()
            db.session.delete(card)
            db.session.commit()

            res = {
                'message': 'Card deleted',
                'card': card_share_schema.dump(Card.query.filter_by(id=card_id).first())
            }

            return jsonify(res)

@card.route('/<card_id>/add_collections', methods=['POST'])
@token_required
def add_card_to_collection(user, card_id):
    card = Card.query.filter_by(id=card_id).first()

    if card is None:
        res = {
            'message': 'Card not found'
        }

        return jsonify(res), 404

    if card.created_by != user.id:
        res = {
            'message': 'You do not own this card'
        }

        return jsonify(res), 403   

    body = request.get_json()

    for element in body['collections']:
        collection = Collection.query.filter_by(id=element['id']).first()
        existing_association = CardAssociation.query.filter_by(card_id=card_id, collection_id=element['id']).first()

        if collection is None:
            res = {
                'message': 'Collection not found'
            }

            return jsonify(res), 404

        elif existing_association is not None:
            res = {
                'message': 'Card already belongs to this collection'
            }

            return jsonify(res), 409

        elif collection.created_by != user.id:
            res = {
                'message': 'You do not own this collection'
            }

            return jsonify(res), 403

        else:
            new_association = CardAssociation(card_id=card.id, collection_id=element['id'])

            db.session.add(new_association)

    db.session.commit()

    card_response = card_share_schema.dump(card)
    card_response['collections'] = collections_share_schema.dump(card.collections)

    res = {
        'message': 'Card added to collections',
        'card': card_response
    }

    return jsonify(res)

@card.route('/<card_id>/remove_collections', methods=['DELETE'])
@token_required
def remove_card_from_collection(user, card_id):
    card = Card.query.filter_by(id=card_id).first()

    if card is None:
        res = {
            'message': 'Card not found'
        }

        return jsonify(res), 404

    elif card.created_by != user.id:
        res = {
            'message': 'You do not own this card'
        }

        return jsonify(res), 403

    body = request.get_json()

    for element in body['collections']:
        collection = Collection.query.filter_by(id=element['id']).first()
        existing_association = CardAssociation.query.filter_by(card_id=card_id, collection_id=element['id']).first()

        if collection is None:
            res = {
                'message': 'Collection not found'
            }

            return jsonify(res), 404

        elif collection.created_by != user.id:
            res = {
                'message': 'You do not own this collection'
            }

            return jsonify(res), 403

        elif existing_association is None:
            res = {
                'message': 'Card does not belong to this collection'
            }

            return jsonify(res), 404

        else:
            CardAssociation.query.filter_by(card_id=card.id, collection_id=element['id']).delete()

    db.session.commit()

    card_response = card_share_schema.dump(card)
    card_response['collections'] = collections_share_schema.dump(card.collections)

    res = {
        'message': 'Card removed from collections',
        'card': card_response
    }

    return jsonify(res)