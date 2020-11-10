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
GET /categories/<int:category_id>
    *General:
        *Returns the id and type of that category object and a success value.
    *Sample: `curl http://localhost:5000/categories/5`
    ```
    {
        categories: {
            id: 5,
            type: "Entertainment"
        },
        success: true
    }
    ```