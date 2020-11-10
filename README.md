# API Reference

## Getting Started 

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

    1. Creates a question with the given json values. Returns the
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

    2. Queries for a question and returns a list of all questions that contain the serach term.
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


