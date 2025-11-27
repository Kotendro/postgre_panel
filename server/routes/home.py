from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config

core = Blueprint("home", __name__)
config = load_config()

logger = getLogger()

@core.route("/")
def index():
    return render_template("home.html")

