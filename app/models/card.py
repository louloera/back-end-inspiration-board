from app import db


class Card (db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id'), nullable=True)
    board = db.relationship('Board', back_populates='boards')


    def to_dict(self):
        card_dict = {
            'id': self.id,
            'message': self.message,
            'likes_count': self.likes_count,
            }
        if self.board_id:
            card_dict["board_id"] = self.board_id
    
        return card_dict
    
    @classmethod
    def get_attributes(cls):
        return 'message', 'likes_count'
    
    @classmethod
    def from_dict(cls, request_body):
        card = cls(
                message=request_body['message'],
                likes_count=request_body['likes_count'],
                board_id=request_body.get('board_id', None))
        return card