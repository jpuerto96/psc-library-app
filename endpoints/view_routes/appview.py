from flask import Blueprint, url_for, render_template, request, current_app
from flask_login import login_required, login_user, logout_user
from flask_mail import Message

app_view_endpoints = Blueprint('app_view_endpoints', __name__)
# Return the home page
@app_view_endpoints.route('/', methods=['GET'])
@login_required
def home():
    return render_template("index.html")
