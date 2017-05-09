'''
   Serves Flask static pages
'''
from flask import (Flask, Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, send_from_directory)
from ..common.helpers import return_json
from ..providers import VkFeatureProvider
import re


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/<path:path>')
def index(path=None):
    print('!!!')
    return render_template('app.html')


@frontend.route('/vk_sentiment', methods=['GET', 'POST'])
def vk_sentiment():
    return render_template('vk_sentiment.html')


@frontend.route('/get_vk_json', methods=['GET', 'POST'])
@return_json
def get_vk_info():
    print('Ok')
    if request.method != 'POST':
        print('Not post')
        return None

    provider = VkFeatureProvider()
    publics = request.form.get('publics', None)
    num_posts = request.form.get('num_posts', None)
    if not publics or not num_posts:
        raise ValueError('Arguments are wrong publics: {}, num_posts: {}'
                         .format(publics, num_posts))

    publics = re.findall(r'[\w.]+', publics)
    print(publics, num_posts)
    res = provider.get_news(publics, int(num_posts))
    print(res)
    return res
