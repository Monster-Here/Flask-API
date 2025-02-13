from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure PostgreSQL Database for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:bikash123@localhost/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the database models
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)


class UserAnswer(db.Model):
    user_answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    submitted_answer = db.Column(db.String(200), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()

# API Endpoints

# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"user_id": user.user_id, "username": user.username} for user in users])


# Add a new user
@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"}), 201


# Get all questions
@app.route("/api/questions", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    return jsonify([
        {"question_id": q.question_id, "question": q.question, "subject": q.subject, "correct_answer": q.correct_answer}
        for q in questions
    ])


# Add a new question
@app.route('/api/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    new_question = Question(
        question=data['question'], 
        subject=data['subject'], 
        correct_answer=data['correct_answer']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'question_id': new_question.question_id, 'question': new_question.question}), 201


# Get all user answers
@app.route("/api/user_answers", methods=["GET"])
def get_user_answers():
    user_answers = UserAnswer.query.all()
    return jsonify([
        {"user_answer_id": ua.user_answer_id, "user_id": ua.user_id, "question_id": ua.question_id, "submitted_answer": ua.submitted_answer}
        for ua in user_answers
    ])


# Add a new user answer
@app.route("/api/user_answers", methods=["POST"])
def add_user_answer():
    data = request.get_json()
    new_user_answer = UserAnswer(
        user_id=data["user_id"], 
        question_id=data["question_id"], 
        submitted_answer=data["submitted_answer"]
    )
    db.session.add(new_user_answer)
    db.session.commit()
    return jsonify({"user_answer_id": new_user_answer.user_answer_id, "user_id": new_user_answer.user_id}), 201


if __name__ == "__main__":
    app.run(debug=True)
