import vk
import json
from sentiment_classifiers import SentimentClassifier, binary_dict, files

class VkFeatureProvider(object):
    def __init__(self):
        self._vk_api = vk.API(vk.Session())
        self._vk_delay = 0.3
        self._clf = SentimentClassifier(files['binary_goods'], binary_dict)

    def _vk_grace(self):
        import time
        time.sleep(self._vk_delay)

    def get_news(self, sources, amount=10):
        # entry for Alex Anlysis tool
        result = []

        for source in sources:
            try:
                data = self._vk_api.wall.get(domain=source, count=amount, extended=1, fields='name')
                self._vk_grace()
                print(data)
            except:
                return {}

            news = []
            for node in data['wall'][1:]:
                try:
                    if node['post_type'] != 'post':
                        continue
                    text = node['text']
                    #print('{}'.format(text.encode('utf-8')))
                    rate = self._clf.predict_text(text)[0]
                    news.append({'text' : '{}'.format(text.encode('utf-8')), 'rate' : rate})
                except Exception as e:
                    print('Exception: {}'.format(e))

            result.append({'source': data['groups'][0]['name'], 'news': news})

        return {'data': result}
