from flask import Blueprint

bp = Blueprint('api', __name__)

#import app.common.argparse

from . import user
