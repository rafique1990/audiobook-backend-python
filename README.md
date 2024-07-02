# Audiobook App

This is an Audiobook application built with FastAPI. The application allows users to manage audiobooks, authors, narrators, subscriptions, bookmarks, listening history, reviews, and ratings.

## Features

- User management 
- Subscription management 
- Author management 
- Narrator management 
- Audiobook management 
- Chapter management 
- Category management 
- Listening history management 
- Bookmark management 
- Review management 
- Rating management 
- Purchase management 

**1. Clone the repository:**

```bash
git clone git@github.com:rafique1990/audiobook-backend-python.git
cd audiobook-app
```
**2. Creating Virtual Environment**

```
python -m venv .venv
```
on Linux 
```
source venv/bin/activate
```
on Windows use:
```
.venv\Scripts\activate
```

**3. Install the dependencies:**

```
pip install -r requirements.txt
```


**4 (Optional). Populate/Insert some test data in the database:**

```
python populate_db.py
```

## Running the Application
Start the FastAPI server using Uvicorn:
```
uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000.

## API Documentation

The API documentation is available at http://127.0.0.1:8000/docs.





## Running Application
run app module
```
uvicorn carsharing:app --reload  

OR

fastapi dev carsharing.py
```

Application runs at  http://127.0.0.1:8000 

## Running Tests
Run the following command to execute the tests:
```
pytest
```
Auo generated documentation for the API an be accessed at: http://127.0.0.1:8000/docs

## Debugging the Application
In the main.py add following two lines:
```
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

This `README.md` file provides a comprehensive overview of the audiobook app, including installation instructions, project structure, and details on how to run the application and tests. Adjust the repository URL and other specifics as needed for your project.
