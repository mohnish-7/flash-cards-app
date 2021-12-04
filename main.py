from flask import Flask, render_template
import os
from application.config import DevelopmentConfig
from application.database import db
from application.models import Users, Decks
app = None

def create_app():

	app = Flask(__name__, template_folder='templates') # Initializing
	env = os.getenv('ENV','development') # Getting the environment
	
	# Checking whether the environment is set up for development
	if env == 'production':

		print('Currently no production config is setup.')

	else:

		print('Starting local development environment...')
		app.config.from_object(DevelopmentConfig) # Configuring the app
	db.init_app(app)
	app.app_context().push()
	return app

app = create_app()
from application.controllers import * # Importing all the controllers


if __name__ == '__main__':

	# Running the Flask app
	app.run(debug=True)
