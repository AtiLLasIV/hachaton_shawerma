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

@bp.route("/vacancies/aggregate", methods=["GET"])
def aggregate_vacancies():
    filters = request.args.to_dict()
    result = get_aggregates(filters)
    return jsonify(result) 