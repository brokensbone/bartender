from flask import Flask, Blueprint, render_template, abort, current_app, g, session, flash, url_for, request, redirect
from werkzeug.exceptions import Forbidden
from . import authentication
import os
import sqlite3
import hashlib
import datetime

ISO8601 = '%Y-%m-%dT%H:%M:%S'

auth = authentication.auth
bp = Blueprint("booze", __name__)

@bp.route("/test", methods=['GET'])
def test():
    return { "result" : "booze!", "score" : 12 }