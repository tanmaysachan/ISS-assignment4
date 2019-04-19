import unittest
from models import ExperimentResults, db
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from app import app

engine = create_engine('sqlite:///local.db', echo = True)
class DatabaseTest(unittest.TestCase):
    def test_url1(self):
        with app.app_context():
            data = ExperimentResults.query.filter_by(language="english", corpus_size=100000).all()
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0].img_url, "https://i.imgur.com/fTkspx5.jpg")

if __name__ == "__main__":
    unittest.main()
