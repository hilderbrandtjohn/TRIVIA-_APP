
## Trivia Game App
The application allows you to:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


### Backend
## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

- [psycopg2](https://www.psycopg.org/docs/install.html) Psycopg is a PostgreSQL adapter for the Python programming language.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Frontend

## Setting up the Frontend

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

## API Documentation
---
### Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
-Error :
```json
{
  "success": false, 
  "error": 404,
  "message": "resource not found"
}
```
---
`GET '/questions'`
- Fetches a paginated set of questions, total number of questions, all categories and current category string
- Request Arguments: 'page' - integer
- Returns an object with 10 paginated questions, total questions, all categories and current category

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "difficulty": 2,
      "category": 5
    }
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Science"
}
```
-Error :
```json
{
  "success": false, 
  "error": 404,
  "message": "resource not found"
}
```
---
`GET '/categories/id/questions'`

- Fetch questions for a category specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "difficulty": 2,
      "category": 5
    }
  ],
  "total_questions": 20,
  "current_category": "Entertainment"
}
```
-Error :
```json
{
  "success": false, 
  "error": 404,
  "message": "resource not found"
}
```
---
`POST '/questions'`

- Sends a post request to add a new question to the database
- Request Body:

```json
{
  "question": "Who let the dogs out?",
  "answer": "who who who who",
  "difficulty": 5,
  "category": 5
}
```
- Returns: Does not return any new data
-Error example:
```json
{
  "success": false, 
  "error": 422,
  "message": "unprocessable"
}
```
---
`POST '/question'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "Who let the"
}
```

- Returns: any array of questions, a number of totalQuestions that match the search term and the current category string

```json
{
  "questions": [
    {
      "id": 21,
      "question": "Who let the dogs out?",
      "answer": "who who who who",
      "difficulty": 5,
      "category": 5
    }
  ],
  "total_questions": 10,
  "current_category": "Entertainment"
}
```
-Error :
```json
{
  "success": false, 
  "error": 422,
  "message": "unprocessable"
}
```
`DELETE '/questions/id'`

- Deletes a question using the specified id
- Request Arguments: `id` - integer
- Returns: Does not need to return any data.


-Error :
```json
{
  "success": false, 
  "error": 404,
  "message": "resource not found"
}
```
---
---
`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    "previous_questions": [4, 2, 9],
    "quiz_category": {
        "id": 1,
        "type": "science"
    }
 }
```
- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

-Error :
```json
{
  "success": false, 
  "error": 404,
  "message": "resource not found"
}
```
---


## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```