#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Start our application."""

from flask import g
from flask_babel import Babel
from api.src.config.create_app import create_app


app = create_app()
babel = Babel(app)
app.run(**app.config.get_namespace('RUN_'))


@babel.timezoneselector
def get_timezone():
    """Set the user timezone on babel."""
    user = g.get('user', None)
    if user is not None:
        return user.timezone
