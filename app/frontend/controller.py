'''
   Serves Flask static pages
'''
from flask import (Flask, Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, send_from_directory)
from flask_login import login_required
from ..common.helpers import return_json
from ..providers import VkFeatureProvider
import re


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/<path:path>')
def index(path=None):
    return render_template('app.html')


@login_required
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
