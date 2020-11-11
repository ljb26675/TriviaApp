import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:dawg2020', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who wrote the song Love Story?',
            'answer': 'Taylor Swift',
            'category': 5,
            'difficulty': 1
        }

        self.search = {
            'searchTerm': 'hank'
        }

        self.quiz = {
            'previous_questions': [],
            'quiz_category': 0,
            'questions': None,
            'numQ': 5
        }

        self.quiz2 = {
            'previous_questions': [],
            'quiz_category': 1,
            'questions': None,
            'numQ': 3
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    '''
    GET /categories test
    '''
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    '''
    GET /categories/{category_id} test
    '''
    def test_get_categories_id(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    '''
    Test error 
    '''
    def test_404_for_categories(self):
        res = self.client().get('/categories/7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    GET /questions tests
    '''
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    '''
    Test error
    '''
    def test_get_questions_error(self):
        res = self.client().get('/questions?page=20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    GET /categories/num/questions tests
    '''
    def test_get_questions_by_cat(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    '''
    Test error
    '''
    def test_get_questions_by_cat_error(self):
        res = self.client().get('/categories/7/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Test POST /questions for adding
    '''
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(question)

    '''
    Test POST /questions for search
    '''
    def test_search_for_question(self):
        res = self.client().post('/questions', json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    

    '''
    Test DELETE
    '''
    def test_delete_question(self): # only works on freshdb, need to restore everytime to run
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(question, None)

    '''
    Test error
    '''
    def test_delete_error(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    '''
    Test POST /quizzes for ALL quiz (category = 0)
    '''
    def test_create_quizzes(self):
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)

        questions = Question.query.filter(Question.category == self.quiz["quiz_category"]).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['numQ'], len(questions))

    '''
    Test POST /quizzes for science quiz (category = 1)
    '''
    def test_create_quizzes(self):
        res = self.client().post('/quizzes', json=self.quiz2)
        data = json.loads(res.data)

        questions = Question.query.filter(Question.category == self.quiz2["quiz_category"]).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['numQ'], len(questions)) 
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()