# -------------------------------------------------------------------------------------------------------------------------------------- #
#															Controllers
# -------------------------------------------------------------------------------------------------------------------------------------- #

from flask import current_app as app 
from flask import render_template, request, redirect
from application.models import Users,Decks,Cards
from random import shuffle
from application.misc import *

# -------------------------------------------------- Initializing Global Variables ----------------------------------------------------- #

u_name = None
current_deck_id = None
n = 0
card_no = 0

print('\n\n','Page refreshed.........','\n\n')

# --------------------------------------------------------------- Login ---------------------------------------------------------------- #

@app.route('/',methods=['GET','POST'])
def login():
		
	try:
		
		global u_name
		
		if request.method == 'GET':
		
			u_name = None
			
			return render_template('login_page.html')
		
		else:
			# This POST request comes from register.html
			new_username = request.form['username']
			new_name = request.form['name']
			new_email = request.form['email']
			new_password = request.form['password']
			status = create_new_user(new_username,new_name,new_email,new_password)
		
			if status:
		
				return render_template('success.html',success='New user created successfully. Please Login to continue...',code='newusercreated')
		
			else:
		
				return render_template('failure.html',failure='Username already exists. Try a different Username or login.',code='usernameexists')

	except:

		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ------------------------------------------------------------- Registration ----------------------------------------------------------- #

@app.route('/register',methods=['GET','POST'])
def register():
	try:
		return render_template('register.html')
	except:
		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# --------------------------------------------------------------- Dashboard ------------------------------------------------------------ #

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
	
	global u_name,n,card_no
	n = 0
	card_no = 0
	
	try:

		# POST Request is generated from the Login page
		if request.method == 'POST':
			
			u_name = request.form['username']
			pwd = request.form['password']
			exists = user_exists(u_name,pwd)
			
			if exists == True:
				
				usr = Users.query.filter(Users.username == u_name).one()
				grps = Decks.query.filter(Decks.owner.any(username=u_name))
				n_decks = num_of_decks(u_name)
				
				if n_decks == 0:
					
					return render_template('dashboard.html',decks=grps,usr_name=usr.name,n_decks=n_decks,flag=1)
				
				else:
					
					return render_template('dashboard.html',decks=grps,usr_name=usr.name)
			


			elif exists == 'wrongpassword':

				return render_template('failure.html',failure='Wrong Password',code='wpwd')



			else:
				
				return render_template('failure.html',failure='Username not found.',code='usernotfound')
		
		# GET request will be generated from any page while going back to dashboard
		else:
			
			if u_name == None:
				return render_template('logout.html')
			
			usr = Users.query.filter(Users.username == u_name).one()
			grps = Decks.query.filter(Decks.owner.any(username=u_name))
			n_decks = num_of_decks(u_name)
			
			if n_decks == 0:
				
				return render_template('dashboard.html',decks=grps,usr_name=usr.name,n_decks=n_decks,flag=1)
			
			else:
				
				return render_template('dashboard.html',decks=grps,usr_name=usr.name)

	except:
	
		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')			



# ------------------------------------------------------ Searching for a Deck ---------------------------------------------------------- #

@app.route('/deck_search',methods=['GET','POST'])
def deck_search():

	try:

		global u_name

		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('deck_search.html')

		else:

			d_name = request.form['deck_name']

			if deck_exists(u_name,d_name):

				search_decks = search(u_name,d_name)
				
				return render_template('search_items.html', decks=search_decks)

			else:

				return render_template('failure.html',failure='Deck not found.',code='nodeckexists3')

	except:

		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')


# ------------------------------------------------------ Creating a New Deck ----------------------------------------------------------- #

@app.route('/new_deck',methods=['GET','POST'])
def new_deck():
	
	try:

		global u_name
		
		if request.method == 'GET':

			if u_name == None:
				return render_template('logout.html')

			return render_template('new_deck.html')
		
		else:

			new_deck = request.form['deck_name']
			status = create_new_deck(new_deck,user_name=u_name)

			if status:

				grps = Decks.query.filter(Decks.owner.any(username=u_name))

				return redirect('/dashboard')

	except:

		 return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')
		


# ------------------------------------------------------- Displaying a Card ------------------------------------------------------------ #

@app.route('/cards/<d_id>',methods=['GET','POST'])
def cards(d_id):
	
	try:
		
		global current_deck_id,card_no
		current_deck_id = d_id
		
		if u_name == None:
			return render_template('logout.html')

		d = Decks.query.filter(Decks.deck_id == d_id).one()
		flashcards = flash_cards(d_id)
		#shuffle(flashcards)
		num_of_cards = len(flashcards)
		
		if card_no == num_of_cards and num_of_cards != 0:
			
			return redirect('/results')

		elif num_of_cards == 0:
			
			return render_template('cards.html',card=None,dn=d.deck_name,n_cards=num_of_cards,flag=1)

		else:
			
			return render_template('cards.html', card=flashcards[card_no], dn=d.deck_name, d_id=d.deck_id,flag=0)


	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ------------------------------------------------------ Displaying all Card ----------------------------------------------------------- #

@app.route('/all_cards/<d_id>',methods=['GET','POST'])
def all_cards(d_id):
		
	try:

		global current_deck_id
		current_deck_id = d_id
		
		if u_name == None:
			return render_template('logout.html')
		
		d = Decks.query.filter(Decks.deck_id == d_id).one()
		cards = flash_cards(d_id)
		num_of_cards = len(cards)
		flashcards = Cards.query.filter(Cards.deck.any(deck_id=d_id))

		return render_template('all_cards.html', cards=flashcards, dn=d.deck_name,n_cards=num_of_cards)

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# -------------------------------------------------------- Creating a new Card --------------------------------------------------------- #

@app.route('/new_card',methods=['GET','POST'])
def new_card():

	try:
		
		global current_deck_id
		
		if request.method == 'GET':
		
			if u_name == None:
					return render_template('logout.html')
		
			return render_template('new_card.html')

		else:

			new_card_title = request.form['card_title']
			new_card_content = request.form['card_content']
			deck_id = current_deck_id
			status = create_new_card(new_card_title,new_card_content,deck_id)
			
			if status:
			
				return render_template('success.html',success='New card created.',code='newcarddel')
	
	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ------------------------------------------------------ Deleting a Card --------------------------------------------------------------- #

@app.route('/delete_card',methods=['GET','POST'])
def del_card():
		
	try:
	
		global current_deck_id
	
		if request.method == 'GET':
	
			if u_name == None:
				return render_template('logout.html')
	
			return render_template('delete_card.html')

		else:
			c_name = request.form['card_name']

			if card_exists(c_name,current_deck_id):

				status = delete_card(c_name,current_deck_id)
				
				if status:
					
					return render_template('success.html',success='Card deleted.',code='newcarddel')

			else:

				return render_template('failure.html',failure='Card not found.',code='nocardexists')
	
	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ---------------------------------------------------------- Deleting a Deck ----------------------------------------------------------- #

@app.route('/delete_deck',methods=['GET','POST'])
def del_deck():
	
	try:

		global u_name

		if request.method == 'GET':

			if u_name == None:

				return render_template('logout.html')

			return render_template('delete_deck.html')

		else:

			d_name = request.form['deck_name']
			
			if deck_exists(u_name,d_name):

				status = delete_deck(d_name,u_name)
				
				if status:
					
					return redirect('/dashboard')

			else:

				return render_template('failure.html',failure='Deck not found.',code='nodeckexists1')

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ---------------------------------------------------------- Editing a Deck ------------------------------------------------------------ #

@app.route('/change_deck_name',methods=['GET','POST'])
def change_deck_name():

	try:

		global u_name

		if request.method == 'GET':
			
			if u_name == None:
				return render_template('logout.html')
			
			return render_template('edit_deck.html')
		
		else:
		
			d_name = request.form['deck_name']
			new_d_name = request.form['new_deck_name']

			if deck_exists(u_name,d_name):

				status = edit_deck(d_name,u_name,new_d_name)
		
				if status:
		
					return redirect('/dashboard')
		
			else:

				return render_template('failure.html',failure='Deck not found.',code='nodeckexists2')

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# -------------------------------------------------------- Score Calculation ----------------------------------------------------------- #

@app.route('/score/<p>',methods=['GET','POST'])
def score_calc(p):

	try:
		
		global n,current_deck_id,card_no
		
		if request.method == 'GET':
		
			if u_name == None:
				return render_template('logout.html')

		else:
			n += 1
			card_no += 1
			status = update_score(current_deck_id,p,n)
		
			if status:
		
				return redirect('/cards/'+str(current_deck_id))

	except:

		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')



# ---------------------------------------------------------- Displaying Results -------------------------------------------------------- #

@app.route('/results',methods=['GET','POST'])
def results():

	try:
		
		global current_deck_id
		d_id = current_deck_id
		d = Decks.query.filter(Decks.deck_id == d_id).one()
		
		return render_template('results.html',score=d.score)

	except:
		
		return render_template('failure.html',failure='Something went wrong. Logout and Try Again.',code='sww')


@app.route('/logout',methods=['GET','POST'])
def logout():
	
	global u_name
	u_name = None
	
	return render_template('logout.html')



# ------------------------------------------------------------ X_____x_____X ----------------------------------------------------------- #