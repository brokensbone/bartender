#!/bin/bash

source env/bin/activate

coverage run -m pytest
coverage report
coverage html

export FLASK_APP="src.launch:application_factory()"
export FLASK_ENV=development
export APPLICATION_DATA=/home/$USER/.config/bartender
flask run --host=127.0.0.1 --port=5005
