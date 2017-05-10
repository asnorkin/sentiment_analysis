import re
from flask import Blueprint, request
from ..common.helpers import return_json
from ..providers.sentiment_classifiers import SentimentClassifier, files, binary_dict
from ..providers.vk_provider import VkFeatureProvider


analysis = Blueprint('analysis', __name__, url_prefix='/api/analysis')


@analysis.route('/goods_analyzer', methods=['POST'])
@return_json
def goods_analyzer():
    classifier = SentimentClassifier(files['binary_goods'], binary_dict)
    text = request.form['text']
    prediction_message = classifier.get_prediction_message(text)
    return {'text': text, 'pred_msg': prediction_message}


@analysis.route('/movies_analyzer', methods=['POST'])
@return_json
def movies_analyzer():
    classifier = SentimentClassifier(files['binary_movie'], binary_dict)
    text = request.form['text']
    prediction_message = classifier.get_prediction_message(text)
    return {'text': text, 'pred_msg': prediction_message}


@analysis.route('/vk', methods=['POST'])
@return_json
def get_vk_info():
    provider = VkFeatureProvider()
    publics = request.form.get('publics', None)
    num_posts = request.form.get('num_posts', None)
    if not publics or not num_posts:
        raise ValueError('Arguments are wrong publics: {}, num_posts: {}'
                         .format(publics, num_posts))

    publics = re.findall(r'[\w.]+', publics)
    res = {}
    try:
        res = provider.get_news(publics, int(num_posts))
    except Exception as e:
        pass
    return res
