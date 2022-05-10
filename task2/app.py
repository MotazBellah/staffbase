import os
from flask import jsonify, request, Flask
from passlib.hash import pbkdf2_sha256

from models import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///staffbase.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/register", methods=['POST'])
def register():
    try:
        args = request.get_json()
        username = args['username']
        password = args['password']
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    
    # use passlib.hash to hash the password
    hashed_pswd = pbkdf2_sha256.hash(password)
    try:
        # Add username & hashed password to DB
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        db.session.remove()
    except Exception as e:
        print(e)
        return jsonify({"error": "User already exsits"}), 409
    

    return jsonify({"message": "Registered successfully"}), 201



@app.route('/', methods=['GET'])
def show_questions():
    questions = Question.query.all()
    return jsonify(questions=[i.serialize for i in questions])



@app.route('/answers', methods=['GET'])
def show_answers():
    answers = Answer.query.all()
    return jsonify(answers=[i.serialize for i in answers])


@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        args = request.get_json()
        username = args['username']
        question = args['question']
    except KeyError:
        return jsonify({ "message": "Bad Request" }), 404

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({ "message": "Unauthenticated." }), 403

    q = Question(question=question, user_id=user.id)
    db.session.add(q)
    db.session.commit()
    db.session.remove()
    
    questions = Question.query.filter_by(user_id=user.id).all()
    
    return jsonify(questions=[i.serialize for i in questions])


@app.route('/answer_question', methods=['POST'])
def answer_question():
    try:
        args = request.get_json()
        username = args['username']
        question_id = args['question_id']
        answer = args['answer']
    except KeyError:
        return jsonify({ "message": "Bad Request" }), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({ "message": "Unauthenticated." }), 403

    user_answer = Answer(answer=answer, user_id=user.id, question_id=question_id)
    db.session.add(user_answer)
    db.session.commit()
    db.session.remove()
    
    answers = Answer.query.filter_by(user_id=user.id).all()
    
    return jsonify(answers=[i.serialize for i in answers])


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=PORT)
