from flask import Flask, url_for, render_template, request
from sentiment_classifiers import SentimentClassifier, files, binary_dict
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
