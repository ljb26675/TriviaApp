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

## Endpoints
**GET /categories/<int:category_id>**
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

**GET /categories**
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

**GET /questions**
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
  "total_questions": 101
}

```
