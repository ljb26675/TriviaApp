import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format()
                 for question in selection if question.question]
    current_qs = questions[start:end]

    return current_qs


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # allow * for all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    GET /categories/<int:category_id>
    Handles GET requests
    for all available categories.
    '''
    @app.route('/categories/<int:category_id>', methods=['GET'])
    def get_category(category_id):

        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if category is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'categories': category.format()
            })

    '''
    GET /categories
    Gets a list of all categories.
    curl -X POST http://localhost:5000/categories
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():

        categories = Category.query.all()
        formatted_cat = {cat.id: cat.type for cat in categories}

        if len(formatted_cat) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_cat
        })

    '''
    GET /questions
    Returns a list of questions, 
    number of total questions, categories. 
    curl http://localhost:5000/questions?page=1
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():

        categories = Category.query.all()
        formatted_cat = {cat.id: cat.type for cat in categories}

        questions = [question for question in Question.query.all()
                     if question.question]
        formatted_qs = paginate_questions(request, questions)

        if len(formatted_qs) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_qs,
            'total_questions': len(questions),
            'categories': formatted_cat

        })

    '''
    DELETE /questions/<int:question_id>
    Deletes a question if the given ID exists. Returns the id of the deleted question,
    success value, new question list, and total questions.
    curl -X DELETE http://localhost:5000/questions/24
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = [question for question in Question.query.order_by(
                Question.id).all() if question.question]
            formatted_qs = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': formatted_qs,
                'total_questions': len(questions)
            })

        except:
            abort(422)

    '''
    POST /questions
    This endpoint does one of two things:
      1. Creates a question with the given json values. Returns the
        success value, new question list with added question, and total questions.
        - curl -X POST -H "Content-Type: application/json" -d '{"question":"What's the deal with airline food?", "answer":"idk", "category":"5", "difficulty":"1"}' http://localhost:5000/questions
      2. Queries for a question and returns a list of all questions that contain the serach term.
        Returns the success value, question list, and total questions.
    
    '''
    # curl -X POST -H "Content-Type: application/json" -d '{"question":"What's the deal with airline food?", "answer":"idk", "category":"5", "difficulty":"1"}' http://localhost:5000/questions
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        search = body.get('searchTerm', None)

        try:
            if search:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))).all()
                questions = [
                    question for question in questions if question.question]
                formatted_qs = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'questions': formatted_qs,
                    'total_questions': len(questions)
                })
            else:
                question = Question(question=new_question, answer=new_answer,
                                    category=new_category, difficulty=new_difficulty)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                questions = [
                    question for question in questions if question.question]
                formatted_qs = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': formatted_qs,
                    'total_questions': len(questions)

                })
        except:
            abort(422)

    '''
    GET /categories/<int:category_id>/questions
    Gets questions based on the category. Returns the id of the
    success value, question list, total questions, and current category.
    curl http://localhost:5000/categories/1/questions
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):

        questions = Question.query.filter(
            Question.category == category_id).all()
        questions = [question for question in questions if question.question]

        formatted_qs = paginate_questions(request, questions)

        if len(formatted_qs) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_qs,
            'total_questions': len(questions),
            'current_category': category_id

        })

    '''
    POST /quizzes
    An endpoint for the quizzes tab. It requires json input of previous questions,
    quiz category, questions, and numQ. It returns the success value,
    a quiz question, questions remaining, and number of questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        questions = body.get('questions', None)
        numQ = body.get('numQ', None)

        try:

            if questions is None:

                numQ = 5

                if quiz_category["id"] == -1:
                    questions = Question.query.all()
                else:
                    cat = int(quiz_category["id"])
                    questions = Question.query.filter(
                        Question.category == cat).all()

                formatted_qs = [question.format()
                                for question in questions if question.question]

                if len(formatted_qs) < 5:
                    numQ = len(formatted_qs)

                questions = formatted_qs

            if len(questions) != 0:
                question = random.choice(questions)

                questions.remove(question)
            else:
                question = []

            return jsonify({
                'success': True,
                'question': question,
                'numQ': numQ,
                'questions': questions
            })

        except:
            abort(422)

    '''
    error handlers for all expected errors 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 405

    return app
