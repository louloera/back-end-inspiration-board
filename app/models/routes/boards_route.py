from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board


boards_bp = Blueprint('boards', __name__)