from flask import Flask, render_template, request, jsonify
from sentiment_classifiers import SentimentClassifier, files, binary_dict
from vk_parser import VkFeatureProvider
import functools

app = Flask(__name__)

def return_json(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return inner

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_vk_json')
@return_json
def get_vk_info():
    provider = VkFeatureProvider()
    publics, num_posts = [], 0

    if request.method == 'POST':
        pass

    return provider.get_news(publics, num_posts)

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

if __name__ == "__main__":
    app.run()
