# -------------------------------------------------------------------------------------------------------------------------------------- #

#														Miscallaneous Functions

# -------------------------------------------------------------------------------------------------------------------------------------- #

from application.database import db
from application.models import Users,Decks,Cards,UserDecks,DeckCards
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_DIR = os.path.join(basedir,'../db_directory')

engine = create_engine('sqlite:///'+os.path.join(SQLITE_DB_DIR,'flashcards.sqlite3'))



# ------------------------------------------------- To Check if User Account exists -----------------------------------------------------#

def user_exists(u_name,pwd):

	with Session(engine, autoflush=False) as session:

		session.begin()

		try:
			
			c = session.query(Users).filter(Users.username == u_name).one()
			u_id = c.user_id

		except:

			c = None

		if c == None:
			return False
		
		else:
			if c.password == pwd:
				return True
			else:
				return 'wrongpassword'



# --------------------------------------------------- To Check if Decks exists ----------------------------------------------------------#

def deck_exists(u_name,d_name):

	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:
				
				user = ssn.query(Users).filter(Users.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).all()

				for d in deck_list:
					
					try:
						
						obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.user_id).filter(UserDecks.deck_id == d.deck_id).one()
						
						if obj != None:
							return True

					except:
						continue		

				return False			 

			except:

				print('Something went wrong.')
				
				return False



# ----------------------------------------------------- To Check if Card exists ---------------------------------------------------------#

def card_exists(c_name,d_id):

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:
				
				card_list = session.query(Cards).filter(Cards.card_title == c_name).all()
				
				for c in card_list:
					
					try:
						
						obj = session.query(DeckCards).filter(DeckCards.deck_id == d_id).filter(DeckCards.card_id == c.card_id).one()
						
						if obj != None:
							return True

					except:
						continue

				return False
					

			except:

				print('Something went wrong.')
				
				return False



# --------------------------------------------------------- To Create a new User --------------------------------------------------------#

def create_new_user(new_username,new_name,new_email,new_password):
	
	with Session(engine, autoflush=False) as session:

		session.begin()

		try:

			if session.query(Users).filter(Users.username == new_username).count() > 0:

				return False

			else:

				new_user = Users(username=new_username,name=new_name,email=new_email,password=new_password)
				session.add(new_user)

		except:

			print('Something went wrong.')
			
			return False

		else:

			print('Commit successful.')
			session.commit()

			return True



# -------------------------------------------------------- To create a new Deck ---------------------------------------------------------#

def create_new_deck(new_deck,user_name):

		with Session(engine, autoflush=False) as session:

			session.begin()

			try:
				
				user = session.query(Users).filter(Users.username == user_name).one()
				new = Decks(deck_name=new_deck,score=0,last_review='NA',num=0)
				new.owner.append(user)
				session.add(new)

			except:

				print('Something went wrong.')
				
				return False

			else:

				print('Commit successful.')
				session.commit()
				return True



# ---------------------------------------------------------- To create a new Card -------------------------------------------------------#

def create_new_card(new_card_title,new_card_content,d_id):

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:
				
				deck_obj = session.query(Decks).filter(Decks.deck_id == d_id).one()
				new = Cards(card_title=new_card_title, card_content=new_card_content)
				new.deck.append(deck_obj)
				session.add(new)

			except:

				print('Something went wrong.')
				
				return False

			else:

				print('Commit successful.')
				session.commit()
				return True	



# --------------------------------------------------------- To delete a Card ------------------------------------------------------------#

def delete_card(c_name,d_id):
	
	with Session(engine, autoflush=False) as session:

			session.begin()

			try:
				card_list = session.query(Cards).filter(Cards.card_title == c_name).all()
				
				for c in card_list:
					
					try:

						del_obj = session.query(DeckCards).filter(DeckCards.deck_id == d_id).filter(DeckCards.card_id == c.card_id).one()
					
					except:
					
						continue
					
					session.delete(del_obj)
				
				for c in card_list:
				
					try:

						del_obj = session.query(Cards).filter(Cards.card_id == c.card_id).filter(Cards.deck.any(deck_id=d_id)).one()
				
					except:
				
						continue
				
					session.delete(del_obj)

			except:

				print('Something went wrong.')
				
				return False

			else:

				print('Commit successful.')
				session.commit()

				return True	



# --------------------------------------------------------- To delete a Deck ------------------------------------------------------------#

def delete_deck(d_name,u_name):

	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:

				user = ssn.query(Users).filter(Users.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).all()
				
				for d in deck_list:
				
					try:
						
						del_obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.user_id).filter(UserDecks.deck_id == d.deck_id).one()
				
					except:
				
						continue
				
					ssn.delete(del_obj) 
				
				for d in deck_list:
				
					try:
						
						cd_list = ssn.query(DeckCards).filter(DeckCards.deck_id == d.deck_id).all()

						for cd in cd_list:
				
							card_list = ssn.query(Cards).filter(Cards.card_id == cd.card_id).all()
							ssn.delete(cd)

						for c in card_list:
						
							delete_card(c.card_title,d.deck_id)
						
						del_obj = ssn.query(Decks).filter(Decks.deck_id == d.deck_id).filter(Decks.owner.any(user_id = user.user_id)).one()
					
					except:

						continue
					
					ssn.delete(del_obj)

			except:

				print('Something went wrong.')
				
				return False

			else:

				print('Commit successful.')
				ssn.commit()

				return True	



# ----------------------------------------------------------- To edit a Deck ------------------------------------------------------------#

def edit_deck(d_name,u_name,new_d_name):
	
	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:
				
				user = ssn.query(Users).filter(Users.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).filter().all()
				
				for d in deck_list:
				
					try:
				
						obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.user_id).filter(UserDecks.deck_id == d.deck_id).one()
				
					except:
				
						continue
				
					if obj != None:
				
						edit_obj = ssn.query(Decks).filter(Decks.deck_id == obj.deck_id).one()
					
					edit_obj.deck_name = new_d_name

			except:

				print('Something went wrong.')
				
				return False

			else:

				print('Commit successful.')
				ssn.commit()

				return True	



# --------------------------------------------------------- To search for a Deck --------------------------------------------------------#

def search(u_name,d_name):

	
	with Session(engine, autoflush=False) as ssn:

			ssn.begin()

			try:
				
				all_decks = []
				user = ssn.query(Users).filter(Users.username == u_name).one()
				deck_list = ssn.query(Decks).filter(Decks.deck_name == d_name).filter().all()
				
				for d in deck_list:
				
					try:
				
						obj = ssn.query(UserDecks).filter(UserDecks.user_id == user.user_id).filter(UserDecks.deck_id == d.deck_id).one()
				
					except:
				
						continue
					
					if obj != None:
						
						dk = ssn.query(Decks).filter(Decks.deck_id == obj.deck_id).one()
						all_decks.append(dk)

				return all_decks
					
				
			except:

				print('Something went wrong.')

				return False



# ------------------------------------------------------- To update a Deck score --------------------------------------------------------#

def update_score(d_id,points,n):

	from datetime import datetime
	import pytz

	with Session(engine, autoflush=False) as session:

			session.begin()

			try:
				
				points = float(points)
				deck = session.query(Decks).filter(Decks.deck_id == d_id).one()
		
				if n == 1:
					
					old_score = 0
				
				else:
				
					old_score = float(deck.score)

				new_score = (old_score + points)
				deck.score = str(new_score)

				ct = str(datetime.now(pytz.timezone('Asia/Kolkata')))
				ct = ct[:-16]
				deck.last_review = ct[:10]+' ,'+ct[10:]
				
				deck.num = n

			except:

				print('Something went wrong.')
				
				return False

			else:

				print('Commit successful.')
				session.commit()

				return True



# ------------------------------------------------- To retrieve all Cards as a list -----------------------------------------------------#

def flash_cards(d_id):

	with Session(engine, autoflush=False) as session:

		session.begin()

		card_list = session.query(Cards).filter(Cards.deck.any(deck_id=d_id)).all()
		
		return card_list



# ---------------------------------------------------- To get the number of Decks -------------------------------------------------------#

def num_of_decks(u_name):

	with Session(engine, autoflush=False) as session:

		session.begin()

		user = session.query(Users).filter(Users.username == u_name).one()
		deck_list = session.query(UserDecks).filter(UserDecks.user_id == user.user_id).all()
	
		return len(deck_list)



# ------------------------------------------------------------- X____X____X -------------------------------------------------------------#
