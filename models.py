from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Feedback(db.Model):
    """
    Feedback model

    consists of id, name, email and feedback
    """
    __tablename__ = 'feedback'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20))
    email = db.Column('email', db.String(50))
    feedback = db.Column('feedback', db.Unicode)

    def __repr__(self):
        return str(self.id) + ":" + self.email

class Question(db.Model):
    """
    Question model
    (to be used by the quiz page)

    consists of id, question and answer
    """
    __tablename__ = 'question'

    id = db.Column('id', db.Integer, primary_key=True)
    question = db.Column('question', db.String(100))
    answer = db.Column('answer', db.String(100))

    def __repr__(self):
        return str(self.id) + ":" + self.question

class ExperimentResults(db.Model):
    """
    ExperimentResults model
    (to be used the experiments page)

    consists of id, language, corpus_size and img_url
    """
    __tablename__ = 'experimentresults'

    id = db.Column('id', db.Integer, primary_key=True)
    language = db.Column('language', db.String(50))
    corpus_size = db.Column('corpus_size', db.Integer)
    img_url = db.Column('img_url', db.String(1000))

    def __repr__(self):
        return str(self.id) + ":" + self.language + ":" + str(self.corpus_size)
