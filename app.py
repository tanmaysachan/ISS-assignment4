from flask import Flask
from views import main
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.secret_key = 'tanmay'

app.register_blueprint(main)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
