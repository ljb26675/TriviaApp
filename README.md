# Trivia App
This project is the Trivia App project for the Udacity Fullstack nanodegree course. Users should be
able to add, delete, and search questions within the app. They should also be able to play the quiz
with questions within the database.

## Getting Started
### Pre-requisites and Local Development
Make sure you have have Python3, pip and node installed on your local machines.

#### Backend
- From the backend folder, create your virtual env:
`python -m virtualenv env`
- Source that virtual env:
`source env/Scripts/activate` (Windows)
`source env/bin/activate` (Mac)
- Install the requirements:
`pip install -r requirements.txt`
- Restore the database from the psql file:
`psql trivia < trivia.psql`

You will need to edit the models.py file to reflect your own local database. To do this, 
edit the `database_path` var.

- To run the app:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://localhost:5000/ by default and is a proxy in the frontend configuration.

### Frontend
From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on http://localhost:3000/

## Tests
In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend
    app is hosted at the default, `http://localhost:5000/`, which is set as a proxy in the frontend config.
- Authentication: This application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON ojects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
    
}
```
The api will return 4 error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method Not Allowed

## Endpoints Glossary
1. [GET /categories/{category_id}](#get-categoriescategory_id "Goto get-categoriescategory_id")
2. [GET /categories](#get-categories "Goto get-categories")
3. [GET /questions](#get-questions "Goto get-questions")
4. [DELETE /questions/{question_id}](#delete-questionsquestion_id "Goto delete-questionsquestion_id")
5. [POST /questions](#post-questions "Goto post-questions")
6. [GET /categories/{category_id}/questions](#get-categoriescategory_idquestions "Goto get-categoriescategory_idquestions")
7. [POST /quizzes](#post-quizzes "Goto post-quizzes")

## Endpoints
### GET /categories/{category_id}
- General:
    - Returns the id and type of that category object and a success value.
- Sample: `curl http://localhost:5000/categories/5`

    ```
    {
        categories: {
            id: 5,
            type: "Entertainment"
        },
        success: true
    }
    ```

### GET /categories
- General:
    - Returns a list of all types of categories and a success value.
- Sample: `curl http://localhost:5000/categories`
    
    ```
    {
        categories: [
            "Science",
            "Art",
            "Geography",
            "History",
            "Entertainment",
            "Sports"
        ],
        success: true
    }
    ```

### GET /questions
- General:
    - Gets a list of all questions with pagination. Returns a list of questions, number of total questions, current category, categories, and a success value.
- Sample: `curl http://localhost:5000/questions?page=2`

```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "current_category": [],
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "idk",
      "category": 5,
      "difficulty": 1,
      "id": 24,
      "question": "Whats the deal with airline food?"
    }
  ],
  "success": true,
  "total_questions": 20
}

```

### DELETE /questions/{question_id}
- General:
    - Deletes a question if the given ID exists. Returns the id of the deleted question,
    success value, new question list, and total questions.
- Sample: `curl -X DELETE http://localhost:5000/questions/24`
```
{
  "deleted": 24,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### POST /questions
- General, This POST call does one of two things, CREATES or SEARCHES:

    1. **Creates** a question with the given json values. Returns the
    success value, new question list with added question, and total questions.
    The json must specify the question and answer text, category, and difficulty score.
    - Sample Creation: `curl -X POST -H "Content-Type: application/json" -d '{"question":"Whats the deal with airline food?", "answer":"idk", "category":"5", "difficulty":"1"}' http://localhost:5000/questions`

        ```
        {
        "created": 110,
        "questions": [
            {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
            },
            {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
            },
            {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
            },
            {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
            }
        ],
        "success": true,
        "total_questions": 20
        }
        ```

    2. **Searches** for a question and returns a list of all questions that contain the serach term.
    Returns the success value, question list, and total questions.
    The json must specify the search term for this to occur. 
    - Sample Creation: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"hank"}' http://localhost:5000/questions`
        
        ```
        {
            "current_category": [],
            "questions": [
                {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                }
            ],
            "success": true,
            "total_questions": 1
        }
        ```

### GET /categories/{category_id}/questions
- General:
    - Gets questions based on the category. Returns the id of the
    success value, question list, total questions, and current category.
- Sample: `curl http://localhost:5000/categories/1/questions`

```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### POST /quizzes
- General:
    - An endpoint for the quizzes tab. It requires json input of previous questions,
  quiz category, questions, and numQ. It returns the success value,
  a quiz question, questions remaining, and number of questions.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{id: "0", type: "Science"}, "questions":null, "numQ":5}' http://localhost:5000/quizzes`
`

