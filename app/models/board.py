from app import db

class Board (db.Model):
    __tablename__ = 'boards'
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', back_populates='board', lazy=True)
    
    def to_dict(self):
        return {
                'id': self.id,
                'title': self.title,
                'owner': self.owner
        }

    @classmethod
    def get_attributes(cls):
        return 'title', 'owner'
    
    @classmethod
    def from_dict(cls, request_body):
        board = cls(
                    title=request_body['title'],
                    owner=request_body['owner']
                    )
        return board
