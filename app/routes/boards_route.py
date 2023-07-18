from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app import db
from app.models.card import Card
from app.models.board import Board
from . import valid
import requests
import os


boards_bp = Blueprint('boards', __name__, url_prefix='/boards')


@boards_bp.route('', methods=['POST'])
@cross_origin()
def create_board():
    request_body = request.get_json()
    valid_request = valid.validate_entry(Board, request_body)

    new_board = Board.from_dict(valid_request)
    
    db.session.add(new_board)
    db.session.commit()
    return jsonify(new_board.to_dict()), 201


@boards_bp.route('', methods=['GET'])
def get_boards():
    title_query = request.args.get('title')
    
    if title_query:
        boards = Board.query.filter(Board.title.ilike('%'+title_query.strip()+'%'))
    else:
        boards = Board.query.all()
    
    board_response = [board.to_dict() for board in boards]
    return jsonify(board_response), 200


@boards_bp.route('/<board_id>', methods=['GET'])
def get_board_by_id(board_id):
    board = valid.validate_id(Board, board_id)
    
    return (board.to_dict()), 200


@boards_bp.route('/<board_id>', methods=['DELETE'])
def delete_board(board_id):
    board = valid.validate_id(Board, board_id)
    
    board_title = board.title
    
    db.session.delete(board)
    db.session.commit()
    return {'details': f'Board {board_id} "{board_title}" successfully deleted'}, 200


@boards_bp.route('/<board_id>/cards', methods=['POST'])
@cross_origin()
def post_card_ids_to_board(board_id):

    board =valid.validate_id(Board, board_id)
    request_body = request.get_json()
    
    valid_request = valid.validate_entry(Card, request_body)
    new_card = Card.from_dict(valid_request)
    new_card.board_id = board_id
    
    db.session.add(new_card)
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_BOT_TOKEN")
    data ={ 
        "channel": "nerdjal2",
        "text":f"Someone just added a card {new_card.message} to the {board.title} board",
        "token": token
    }
    response = requests.post(url, data=data)

    return (new_card.to_dict()), 200


@boards_bp.route('', methods=['DELETE'])
def delete_all_boards():

    boards = Board.query.all()
    # db.session.delete(boards)

    cards = Card.query.all()
    # db.session.delete(cards)
    
    for board in boards: 
        db.session.delete(board)
    for card in cards:
        db.session.delete(card)

    db.session.commit()
    return jsonify("Deleted all boards"), 201

@boards_bp.route('/<board_id>/cards', methods=['GET'])

def get_one_board_cards(board_id):
    board = valid.validate_id(Board, board_id)
    cards = Card.query.filter_by(board_id=board_id).order_by(Card.likes_count.desc()).order_by(Card.message.asc())

    return ({'cards': [card.to_dict() for card in cards]}), 200
    