from flask import Blueprint

app = Blueprint('normal_xss',
    __name__,
    template_folder='templates',
    static_folder='static')

from . import views
