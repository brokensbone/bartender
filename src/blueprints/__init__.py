from . import api, authentication, location, drink

def register(flapp):
    flapp.register_blueprint(api.bp, url_prefix="/api")
    flapp.register_blueprint(authentication.bp, url_prefix="/auth")
    flapp.register_blueprint(location.bp, url_prefix="/location")
    flapp.register_blueprint(drink.bp, url_prefix="/drink")