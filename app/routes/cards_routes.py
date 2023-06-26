from flask import Blueprint, request, jsonify, make_response
from app import db
from . import valid
from app.models.card import Card


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = valid.validate_id(Card, card_id)
    
    card_title = card.title
    
    db.session.delete(card)
    db.session.commit()
    return {'details': f'Card {card_id} "{card_title}" successfully deleted'}, 200
