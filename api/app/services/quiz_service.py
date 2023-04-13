from flask import make_response, jsonify
import json

def get_quiz(specifications):

    #TODO: add logic for different kinds of quiz data based on specifications
    try:
        # SAMPLE QUIZ DATA
        f = open('data/sample_data.json')
        quiz_data = json.load(f)

        return make_response(jsonify(quiz_data), 200)

    except Exception as e:
        return make_response({'message': str(e)}, 500)
    