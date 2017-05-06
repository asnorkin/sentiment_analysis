import functools
import re
import os

from flask import Flask, render_template, request, jsonify
from extensions import db, login_manager, csrf
import config

from sentiment_classifiers import SentimentClassifier, files, binary_dict
from vk_parser import VkFeatureProvider

app = Flask(__name__)
###############################################################################
#                           App managing function
###############################################################################
def create_app(cfg=None, app_name=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = config.DefaultConfig.PROJECT

    app = Flask(app_name) # TODO: check params
    configure_app(app, cfg)
    configure_extensions(app)

    return app

def configure_app(app, cfg=None):
    if not cfg:
        cfg = config.DefaultConfig

    app.config.from_object(cfg)

    application_mode = os.getenv('APPLICATION_MODE', 'LOCAL')
    app.config.from_object(config.get_config(application_mode))

def configure_extensions(app):
    db.init_app(app)

    login_manager.login_view = 'frontend.login'
    login_manager.refresh_view = 'frontend.login'

    @login_manager
    def load_user(id):
        pass # TODO: make it works
        #return user.query.get(id)

    login_manager.setup_app(app)
    csrf.init_app(app)

###############################################################################
#
###############################################################################
def return_json(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return inner

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_vk_json', methods=['GET', 'POST'])
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
#                               Models
###############################################################################
@app.route('/vk_sentiment', methods=['GET', 'POST'])
def vk_sentiment():
    return render_template('vk_sentiment.html')

@app.route('/bank_sentiment', methods=['GET', 'POST'])
def bank_sentiment():
    #classifier = SentimentClassifier(files[')

    text = ''
    prediction_message = ''
    if request.method == 'POST':
        text = request.form['text']

    return render_template('bank_sentiment.html', text=text, prediction_message=prediction_message)

@app.route('/movie_binary_sentiment', methods=['GET', 'POST'])
def movie_binary_sentiment():
    classifier = SentimentClassifier(files['binary_movie'], binary_dict)

    text = ''
    prediction_message = ''
    if request.method == 'POST':
        text = request.form['text']
        prediction_message = classifier.get_prediction_message(text)

    return render_template('movie_binary_sentiment.html', text=text, prediction_message=prediction_message)

@app.route('/goods_binary_sentiment', methods=['GET', 'POST'])
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
@app.route('/algo.html')
def algo():
    return render_template('algo.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.debug = True
    app.run()
