from flask import Blueprint, request, abort

from . import authentication
from src.provider import inventory

bp = Blueprint("drink", __name__)
auth = authentication.auth

@bp.route("beer/new", methods=['POST'])
@auth.login_required
def new_beer():
    try:
        json_data = request.get_json()
        rowid = inventory().new_beer(json_data)
        return {"rowid":rowid}
    except ValueError:
        return abort(401)


@bp.route("beer/<int:rowid>", methods=['GET'])
@auth.login_required
def retrieve_beer(rowid):
    beer = inventory().retrieve_beer(rowid)
    if beer is None:
        return abort(404)
    return { "data" : beer.write_json() }

@bp.route("beer/<int:rowid>", methods=['POST'])
@auth.login_required
def update_beer(rowid):
    try:
        json_data = request.get_json()
        saved_id = inventory().update_beer(rowid, json_data)
        return {"rowid":saved_id}
    except ValueError:
        return abort(401)