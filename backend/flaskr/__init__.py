import os
from ssl import Options
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,questions):
    page=request.args.get('page',1, type=int)
    start =(start-1) * QUESTIONS_PER_PAGE
    end= start + QUESTIONS_PER_PAGE

    formated_questions=[questions.format() for question in questions]
    parginated_questions=formated_questions[start:end]

    return parginated_questions
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors=CORS(app, resources={r"/*":{"origins":"*"}})

     #CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authentication,True')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def categories():
        all_categories = Category.query.all()
        all_categories = {category.id: category.type for category in all_categories}

        return jsonify(
            {
                "success": True,
                "categories": all_categories
            }
        )


    #endpoint to handle GET requests for questions,including pagination (every 10 questions).
    @app.route('/questions')
    def get_questions():

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.order_by(Category.id).all()
        current_categories = [category.format() for category in categories]
        
        final_categories = {}
        for x in current_categories:
            final_categories.update({x['id']: x['type']})

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions':len(formatted_questions),
            'categories': final_categories,
            'current_category': 1

            })
    
    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question:
            try:
                question.delete()
            except:
                abort(500)
            else:
                return jsonify({
                    "success": True,
                    "question_id": question_id
                }), 200
        else:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({
               'success': True,
            })

        except:
            abort(422)

    @app.route("/question", methods=["POST"])
    def search_questions():
        body = request.get_json()

        search_term = body.get("searchTerm", None)

        search_result = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()
        current_search = paginate_questions(request, search_result)
        current_category = Category.query.get(1)
        current_category = current_category.format()["type"]

        return jsonify({
            "success": True,
            "questions": current_search,
            "total_questions": len(search_result),
            "current_category": current_category
        })

    @app.route('/categories/<int:category_id>/questions')
    def retreive_category_questions(category_id):
        page = request.args.get('page',1,type=int)

        current_category = Category.query.get(category_id)
        if current_category is None:
            abort(404)

        categories = Category.query.all()
        categories = [category.format() for category in categories]

        questions = Question.query.filter(Question.category == category_id).all()

        start = (page - 1) * QUESTIONS_PER_PAGE
        if(start > len(questions)):
            abort(404)
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format() for question in questions[start:end]]
        return jsonify({
        'success':True,
        'questions':formatted_questions,
        'total_questions': len(questions),
        'current_category': current_category.format(),
        'categories': categories
    })

    @app.route("/quizzes", methods=["POST"])
    def get_quiz():
        data = request.get_json()
        previous_question = data.get("previous_questions")
        quiz_category = data.get("quiz_category")

        if quiz_category["id"] == 0:  
            # for all the categories
            all_questions = Question.query.all()
        else:
            # for the other categories
            all_questions = Question.query.filter_by(
                category=quiz_category["id"]).all()

            if not all_questions:

                abort(404)

        question_list = [q.format() for q in all_questions
                         if q.id not in previous_question]

        if question_list == []:
            return jsonify({
                "success": True
            })

        else:

            question = random.choice(question_list)

            return jsonify({
                "success": True,
                "question": question
            })

    #errir handlers
    @app.errorhandler(404)
    def not_found_404(error):
        return jsonify({
            'success':False,
            'message':"Resource Not Found",
            'error':404
         }),404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success":False,
            "message": "Method Not Alowed",
            "error": 405
        }),405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error_500(error):
        return jsonify({
            'success':False,
            'message':"server error",
            'error':500
        }),500

    return app

