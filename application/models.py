from application.database import db

class Users(db.Model):

	__tabelname__ = 'users'
	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	email = db.Column(db.String)
	password = db.Column(db.String)
	


class Decks(db.Model):

	__tabelname__ = 'decks'
	deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	deck_name = db.Column(db.String, nullable=False)
	score = db.Column(db.String)
	last_review = db.Column(db.String)
	num = db.Column(db.Integer)
	owner = db.relationship('Users', secondary='user_decks')



class UserDecks(db.Model):

	__tabelname__ = 'user_decks'
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True, nullable=False)
	deck_id = db.Column(db.Integer, db.ForeignKey('decks.deck_id'), primary_key=True, nullable=False)



class Cards(db.Model):

	__tabelname__ = 'cards'
	card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	card_title = db.Column(db.String, nullable=False)
	card_content = db.Column(db.String, nullable=False)
	deck = db.relationship('Decks', secondary='deck_cards')



class DeckCards(db.Model):

	__tabelname__ = 'deck_cards'
	deck_id = db.Column(db.Integer, db.ForeignKey('decks.deck_id'), primary_key=True, nullable=False)
	card_id = db.Column(db.Integer, db.ForeignKey('cards.card_id'), primary_key=True, nullable=False)
