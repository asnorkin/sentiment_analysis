'''
   Serves Flask static pages
'''
from flask import (Flask, Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, send_from_directory)
from ..common.helpers import return_json
from ..providers import VkFeatureProvider
from ..providers.sentiment_classifiers import SentimentClassifier, files, binary_dict
import re


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/<path:path>')
def auth(path=None):
    return render_template('app.html')


@frontend.route('/index')
def index():
    return render_template('index.html')


@frontend.route('/vk_sentiment', methods=['GET', 'POST'])
def vk_sentiment():
    return render_template('vk_sentiment.html')


@frontend.route('/get_vk_json', methods=['GET', 'POST'])
@return_json
def get_vk_info():
    if request.method != 'POST':
        return None

    provider = VkFeatureProvider()
    publics = request.form.get('publics', None)
    num_posts = request.form.get('num_posts', None)
    if not publics or not num_posts:
        raise ValueError('Arguments are wrong publics: {}, num_posts: {}'
                         .format(publics, num_posts))

    publics = re.findall(r'[\w.]+', publics)
    return provider.get_news(publics, int(num_posts))


###############################################################################
#                           Classifier pages
###############################################################################
@frontend.route('/movie_binary_sentiment', methods=['GET', 'POST'])
def movie_binary_sentiment():
    classifier = SentimentClassifier(files['binary_movie'], binary_dict)

    text = ''
    prediction_message = ''
    if request.method == 'POST':
        text = request.form['text']
        prediction_message = classifier.get_prediction_message(text)

    return render_template('movie_binary_sentiment.html', text=text, prediction_message=prediction_message)


@frontend.route('/goods_binary_sentiment', methods=['GET', 'POST'])
def goods_binary_sentiment():
    classifier = SentimentClassifier(files['binary_goods'], binary_dict)

    text = ''
    prediction_message = ''
    if request.method == 'POST':
        text = request.form['text']
        prediction_message = classifier.get_prediction_message(text)

    return render_template('goods_binary_sentiment.html', text=text, prediction_message=prediction_message)


###############################################################################
#                             Info pages
###############################################################################
@frontend.route('/algo.html')
def algo():
    return render_template('algo.html')


@frontend.route('/about.html')
def about():
    return render_template('about.html')
