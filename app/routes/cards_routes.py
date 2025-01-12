from flask import Blueprint, request
from app import db
from . import valid
from app.models.card import Card


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')


@cards_bp.route('/<card_id>', methods=['PATCH'])
def update_card(card_id):
    card = valid.validate_id(Card, card_id)
    request_body = request.get_json()
    
    card.likes_count = request_body.get('likes_count', card.likes_count)
    card.board_id = request_body.get('board_id', card.board_id)
    
    db.session.commit()
    
    return card.to_dict(), 201


@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = valid.validate_id(Card, card_id)
    
    card_message= card.message
    
    db.session.delete(card)
    db.session.commit()
    
    return {'details': f'Card {card_id} "{card_message}" successfully deleted'}, 200
