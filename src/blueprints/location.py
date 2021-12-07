from flask import Blueprint, request, abort

from src.provider import location_manager
from . import authentication

auth = authentication.auth

bp = Blueprint("location", __name__)

@bp.route("new", methods=['POST'])
@auth.login_required
def api_new_location():
    venue_json = request.get_json()
    success = location_manager().new_location_json(venue_json)
    return {"success" : success }

@bp.route("<int:rowid>", methods=["GET"])
@auth.login_required
def api_get_location(rowid):
    v = location_manager().retrieve_location(rowid)
    if v is None:
        return abort(404)
    return {"data" : v.as_dict() }

@bp.route("<int:rowid>", methods=["POST"])
@auth.login_required
def api_update_location(rowid):
    venue_json = request.get_json()
    lm = location_manager()
    v = lm.retrieve_location(rowid)
    if v is None:
        return abort(404)
    v.set_from_json(venue_json)
    lm.update_location(v)
    return {"result" : True}

@bp.route("search", methods=["GET"])
@auth.login_required
def api_search_location():
    longitude = request.args.get('longitude', type = float)
    latitude = request.args.get('latitude', type = float)
    nearness = request.args.get('nearness', default=0.1, type = float)
    vs = location_manager().get_venues_near(longitude, latitude, nearness=nearness)
    return {"data" : [ v.as_dict() for v in vs ]}



