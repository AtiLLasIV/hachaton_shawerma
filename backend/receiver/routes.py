from flask import Blueprint, request, jsonify
from handler.insert import insert_vacancy
from handler.get import get_vacancies
from handler.aggregate import get_aggregates

bp = Blueprint('receiver', __name__)

@bp.route("/vacancy", methods=["POST"])
def add_vacancy():
    data = request.json
    result = insert_vacancy(data)
    return jsonify(result)

@bp.route("/vacancies", methods=["GET"])
def list_vacancies():
    filters = request.args.to_dict()
    result = get_vacancies(filters)
    return jsonify(result)

# @bp.route("/vacancies/aggregate", methods=["GET"])
# def aggregate_vacancies():
#     filters = request.args.to_dict()
#     result = get_aggregates(filters)
#     return jsonify(result) 

# @bp.route("/mock_vacancies", methods=["GET"])
# def mock_vacancies():
#     data = [
#         {
#             "company": "РоссияАвто",
#             "position": "Курьер",
#             "salary": 41000,
#             "city": "Москва",
#             "experience_years": 0,
#             "currency": "RUB",
#             "posted_at": "2024-06-10T10:00:00Z",
#         },
#         {
#             "company": "Самокат",
#             "position": "Курьер на велосипеде",
#             "salary": 193000,
#             "city": "Москва",
#             "experience_years": 0,
#             "currency": "RUB",
#             "posted_at": "2024-06-09T09:00:00Z",
#         },
#         {
#             "company": "Яндекс Еда",
#             "position": "Курьер",
#             "salary": 70000,
#             "city": "Санкт-Петербург",
#             "experience_years": 0,
#             "currency": "RUB",
#             "posted_at": "2024-06-08T12:00:00Z",
#         },
#         {
#             "company": "Самокат",
#             "position": "Курьер на авто",
#             "salary": 100000,
#             "city": "Москва",
#             "experience_years": 0,
#             "currency": "RUB",
#             "posted_at": "2024-06-06T11:00:00Z",
#         },
#     ]
    return jsonify(data)