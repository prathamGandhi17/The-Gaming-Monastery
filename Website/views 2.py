from flask import Blueprint, render_template

#urls
views = Blueprint('views', __name__)

#root
@views.route('/')
def home():
    return render_template("home.html")
