# app.py

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')

app.config.from_pyfile('config.py')  # Carrega as configurações do arquivo config.py
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from controllers.api_controller import *
from controllers.home_controller import *
from models.caixa import Caixa

if __name__ == '__main__':
    app.run(debug=True)
