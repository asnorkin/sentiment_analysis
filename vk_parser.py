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
        #return json.dumps(result)
        return result

    # NOTE: the completely other feature, very usefull personally for me
    def friends_intersect(self, uid_list):
        result = None
        try:
            result = set(self._vk_api.friends.get(user_id=uid_list[0]))
            self._vk_grace()
        except:
            pass
        for i, uid in enumerate(uid_list[1:]):
            try:
                tmp = set(self._vk_api.friends.get(user_id=uid))
                self._vk_grace()
            except:
                continue
            if result is not None:
                result = result.intersection(tmp)
            else:
                result = tmp
        return result

    def get_user_info(self, entry_uid, fname=None, lname=None):
        try:
            friend_list = self._vk_api.friends.get(user_id=entry_uid, fields='personal', name_case='nom')
            self._vk_grace()
        except:
            return []

        return [x for x in friend_list
                if (not fname or fname in x['first_name']) and (not lname or lname in x['last_name'])]

    def get_uid_set_info(self, uid_set):
        result = []
        for friend_uid in uid_set:
            try:
                friend = self._vk_api.users.get(user_id=friend_uid, fields='sex,personal', name_case='nom')
                self._vk_grace()
            except:
                continue
            result.append(friend)

        return result

if __name__ == '__main__':
    provider = VkFeatureProvider()
    res = provider.get_news(['scientific.american'], 5)
    print(res)
