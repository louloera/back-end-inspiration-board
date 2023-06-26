from flask import Blueprint, request, jsonify, make_response
from app import db
from app import valid
from app.models.card import Card
from app.models.board import Board


cards_bp = Blueprint('cards', __name__, url_prefix='cards')

@cards_bp.route('/<board_id>', methods=['DELETE'])
def delete_task(board_id):
    board = valid.validate_id(Board, board_id)
    
    board_title = board.title
    
    db.session.delete(board)
    db.session.commit()
    return {'details': f'Board {board_id} "{board_title}" successfully deleted'}, 200
