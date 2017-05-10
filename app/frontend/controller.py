'''
   Serves Flask static pages
'''
from flask import Blueprint, render_template


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/<path:path>')
def auth(path=None):
    return render_template('app.html')


@frontend.route('/index')
def index():
    return render_template('index.html')


###############################################################################
#                           Classifier pages
###############################################################################
@frontend.route('/vk_sentiment')
def vk_sentiment():
    return render_template('vk_sentiment.html')


@frontend.route('/movie_binary_sentiment')
def movie_binary_sentiment():
    return render_template('movie_binary_sentiment.html')


@frontend.route('/goods_binary_sentiment')
def goods_binary_sentiment():
    return render_template('goods_binary_sentiment.html')


###############################################################################
#                             Info pages
###############################################################################
@frontend.route('/algo.html')
def algo():
    return render_template('algo.html')


@frontend.route('/about.html')
def about():
    return render_template('about.html')
