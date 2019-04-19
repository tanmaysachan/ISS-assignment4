from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Feedback, Question, ExperimentResults

import json
import random

# to be used the quiz method
last_set_of_questions = []
reset = False

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/intro')
@main.route('/introduction')
def intro():
    """
    introduction page
    """
    return render_template('Introduction.html') 

@main.route('/theory')
def theory():
    """
    theory page
    """
    return render_template('Theory.html') 

@main.route('/objective')
def objective():
    """
    objective page
    """
    return render_template('Objective.html') 

@main.route('/experiment', methods=['GET', 'POST'])
def experiment():
    """
    experiment page

    Asks the user to select language, and corpus size.
    Displays the relevant experiment by querying the database.

    Images hosted on Imgur.
    """
    languages = []
    corpus_sizes = []
    img_url = "not_found"
    for it in ExperimentResults.query.all():
        if it.language not in languages:
            languages.append(it.language)
        if it.corpus_size not in corpus_sizes:
            corpus_sizes.append(it.corpus_size)
    if request.method == 'POST':
        print(request.form['language'], request.form['corpus_size'])
        img_url = ExperimentResults.query.filter_by(language=request.form['language'],
                corpus_size=request.form['corpus_size']).all()
        assert(len(img_url) == 1)
        img_url = img_url[0].img_url
        print(img_url)
    return render_template('Experiment.html', languages=languages,
            corpus_sizes=corpus_sizes, img_url=img_url)

@main.route('/add_experiment', methods=['GET', 'POST'])
def add_experiment():
    """
    add_experiment page

    Asks the user inputs for an experiment.
    Adds the corresponding experiment to the database,
    which can then be used on the experiment page.
    """
    if request.method == 'POST':
        if not request.form['language'] or not request.form['corpus_size'] or not request.form['img_url']:
            flash("*fill all fields", "error")
            return redirect(url_for('main.add_experiment'))
        if len(ExperimentResults.query.filter_by(language=request.form['language'].lower(),
                corpus_size=request.form['corpus_size']).all()):
            flash("*experiment already exists", "error")
            return redirect(url_for('main.add_experiment'))
        er = ExperimentResults(language=request.form['language'].lower(),
        corpus_size=request.form['corpus_size'], img_url=request.form['img_url'])
        db.create_all()
        db.session.add(er)
        db.session.commit()
        flash("experiment added!", "success")
        return redirect(url_for('main.add_experiment'))
    return render_template('add_experiment.html')

@main.route('/show_experiments')
def show_experiments():
    """
    show_experiments page

    Displays all existing experiments in the database.
    """
    return render_template('show_experiments.html', exps=ExperimentResults.query.all())

@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    quiz page

    Selects 5 random questions from the database,
    and displays them.
    Clicking on the submit button evaluates them.
    The user is made aware of the questions they attempted wrong.
    """
    global last_set_of_questions
    global reset
    question_db_size = len(Question.query.all())
    print(question_db_size)
    ids = random.sample(range(1, question_db_size+1), 5);
    questions_chosen = []
    for i in ids:
        questions_chosen.append(Question.query.get(i))
    if reset:
        questions_chosen = last_set_of_questions
        reset = False
    if request.method != 'POST':
        last_set_of_questions = questions_chosen
    if request.method == 'POST':
        wrong_questions = []
        cnt = 1
        for question in last_set_of_questions:
            answer = request.form[str(question.id)]
            if question.answer.lower() != answer.lower():
                wrong_questions.append(cnt)
            cnt += 1
        format_string = "Some questions were wrong. List of wrong questions: "
        for i in wrong_questions:
            format_string += str(i) + ","
        if len(wrong_questions) == 0:
            flash("All correct! Well Done!", "success")
        else:
            format_string = format_string[:-1]
            flash(format_string, "wrong")
            reset = True
        return redirect(url_for('main.quiz'))
    return render_template('Quizzes.html', questions=questions_chosen) 

@main.route('/procedure')
def procedure():
    """
    procedure page
    """
    return render_template('Procedure.html') 
   
@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """
    feedback page

    User can enter their feedback.
    """
    if request.method == 'POST':
        fb = Feedback(name=request.form['name'], email=request.form['email'],
                feedback=request.form['feedback'])
        print(fb)
        db.create_all()
        db.session.add(fb)
        db.session.commit()
    return render_template('Feedback.html') 

@main.route('/check_feedbacks')
def check_feedbacks():
    """
    check_feedback page

    Displays all the feedbacks so far.
    """
    return render_template('check_feedback.html', fbs=Feedback.query.all())

@main.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """
    add_question page

    User can add a question to the database, which can be used
    by the quiz.
    Quiz must be supplied with a corresponding answer.
    """
    if request.method == 'POST':
        if not request.form['question'] or not request.form['answer']:
            flash('question not added, invalid question/answer', 'error')
            return redirect(url_for('main.add_question'))
        q = Question(question=request.form['question'], answer=request.form['answer'])
        db.create_all()
        db.session.add(q)
        db.session.commit()
    return render_template('add_ques.html')

@main.route('/get_all_questions')
def get_all_questions():
    """
    get_all_questions page

    User can check on all existing questions.
    This page does not reveal the answers however.
    """
    print(len(Question.query.all()))
    return render_template('get_all_questions.html',  questions=Question.query.all())
