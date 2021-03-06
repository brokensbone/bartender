from flask import Flask, Blueprint, render_template, abort, current_app, g, session, flash, url_for, request, redirect
from werkzeug.exceptions import Forbidden
from . import authentication
import os
import sqlite3
import hashlib
import datetime



auth = authentication.auth
bp = Blueprint("booze", __name__)

@bp.route("/test", methods=['GET'])
def test():
    return { "result" : "booze!", "score" : 13 }

@bp.route("/testauth")
@auth.login_required
def test_auth():
    return test()
