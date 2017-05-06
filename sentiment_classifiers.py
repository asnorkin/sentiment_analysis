from sklearn.externals import joblib

files = {
    'binary_movie' : 'binary_movie_clf.pkl',
    'bank' : 'bank_clf.pkl',
    'binary_goods' : 'binary_goods_clf.pkl'
}

binary_dict = {
    -1 : 'prediction error',
     0 : 'negative',
     1 : 'positive'
}


class SentimentClassifier():
    
    def __init__(self, model_file, classes_dict):
        self.model = joblib.load(model_file)
        self.classes_dict = classes_dict

    def get_probability_words(self, probability):
        if probability < 0.55:
            return "neutral or uncertain"
        if probability < 0.7:
            return "probably"
        if probability > 0.95:
            return "certain"
        else:
            return ""

    def predict_text(self, text):
        try:
            pred = self.model.predict([text])[0]
            have_predict_proba = getattr(self.model, 'predict_proba', None)
            prob = 0.95 if not have_predict_proba else self.model.predict_proba([text])[0].max()
            return pred, prob
        except Exception as e:
            print("Prediction error: {}".format(e))
            return -1, 0.8

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + " " + self.classes_dict[class_prediction]

