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

  questions = [question.format() for question in selection]
  current_qs = questions[start:end]

  return current_qs

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}}) # allow * for all origins


  '''
  DONE  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''


  '''
  DONE Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''test curl for endpoint we set up
    curl http://localhost:5000'''
  # same route
  @app.route('/')
  #@cross_origin()
  def hello():
    return jsonify({'message': 'HELLO WORLD'})
  
 

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_category(category_id):
    try:

      category = Category.query.filter(Category.id == category_id).one_or_none()

      if category is None:
        abort(404)
      else:
        return jsonify({
          'success': True,
          'categories': category.format()
        })

    except:
      abort(400)

  #post should not be allowed
  # curl -X POST http://localhost:5000/categories
  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      categories = Category.query.all()
      #formatted_cat = [cat.format() for cat in categories]
      #catTypes = [cat.type for cat in formatted_cat]
      formatted_cat = [cat.type for cat in categories]
      # current cat?
      if len(formatted_cat) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'categories': formatted_cat
      })
    except:
      abort(400)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  #http://localhost:5000/questions?page=1
  @app.route('/questions', methods=['GET'])
  def get_questions():
    
    try:
      '''category = request.args.get('category', -1, type=int)

      if category != -1:
        questions = Question.query.filter(Question.category == category).all()
      else:
        questions = Question.query.all()'''

      categories = Category.query.all()
      formatted_cat = [cat.type for cat in categories]
      
    
      questions = Question.query.all()
      #print(questions)
      formatted_qs = paginate_questions(request, questions)

      if len(formatted_qs) == 0:       
        abort(404)
        
      return jsonify({ 
        'success': True,
        'questions': formatted_qs,
        'total_questions': len(questions),
        'categories': formatted_cat,
        'current_category': []
      
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      questions = Question.query.order_by(Question.id).all()
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
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  #curl -X POST -H "Content-Type: application/json" -d '{"question":"What's the deal with airline food?", "answer":"idk", "category":"5", "difficulty":"1"}' http://localhost:5000/questions
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
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
        formatted_qs = paginate_questions(request, questions)
        return jsonify({
        'success': True,
        'questions': formatted_qs,
        'total_questions': len(questions),
        'current_category': []
        })
      else:
    
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()


        questions = Question.query.order_by(Question.id).all()
        formatted_qs = paginate_questions(request, questions)
          
        return jsonify({ # current catergory, categories? 
          'success': True,
          'created': question.id,
          'questions': formatted_qs,
          'total_questions': len(questions)
        
        })
    except:
      abort(422)


  '''
  @TODO: DONE -- SEARCH BREAKS THO
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  

  '''
  @TODO: DONE
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_category_questions(category_id):
    
    try:
      
      questions = Question.query.filter(Question.category == category_id).all()
    
      #questions = Question.query.all()
      formatted_qs = paginate_questions(request, questions)

      if len(formatted_qs) == 0:       
        abort(404)
        
      return jsonify({ # current catergory, categories? 
        'success': True,
        'questions': formatted_qs,
        'total_questions': len(questions),
        'current_category': category_id
      
      })
    except:
      abort(400)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
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

        if quiz_category["id"] == -1: #works
          questions = Question.query.all()
        else:
          cat = int(quiz_category["id"])+1          
          questions = Question.query.filter(Question.category == cat).all()

        formatted_qs = [question.format() for question in questions if question.question]
        

        if len(formatted_qs) < 5:
          numQ = len(formatted_qs)

        questions = formatted_qs

      if len(questions) != 0:
        question = random.choice(questions)
        #question = random.choice(formatted_qs)

        questions.remove(question)
      else:
        question = []
        
      return jsonify({ # current catergory, categories? 
        'success': True,
        'question': question,
        'numQ': numQ,
        'questions': questions
      })

    except:
      abort(422)


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
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
  
  @app.errorhandler(404)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
    }), 400

  
  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
    }), 405
  
  return app

    