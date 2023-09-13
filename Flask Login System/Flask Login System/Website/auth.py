from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route("hello")
def hello():
    pass