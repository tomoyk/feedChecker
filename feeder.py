import datetime
import os
import requests
import json

class Feeder:
    def __init__(self):
        self.entries = []

    def set(self, parsed_feed):
        for entry in parsed_feed['entries']:
            tmp = {}

            # Convert "Tue, 06 Mar 2018 05:20:30 +0000" => Type(Date)
            entry_date_raw = entry['published']
            entry_date = datetime.datetime.strptime(entry_date_raw, '%a, %d %b %Y %H:%M:%S %z')
            tmp['date'] = str(entry_date.strftime('%Y/%m/%d'))

            # Convert from internal-uri to external-uri
            entry_uri = entry['links'][0]['href']
            tmp['uri'] = entry_uri.replace("//inside.teu.ac.jp/", "//service.cloud.teu.ac.jp/inside2/")

            tmp['title'] = entry['title']
            tmp['author'] = entry['author']
            tmp['content'] = entry['content'][0]['value']
            self.entries.append(tmp)

    def get(self):
        return self.entries

    def show(self, items=[]):
        for entry in self.entries:
            for key in items:
                print(entry[key])
            print("--------------------")

    # Fetch new pattern [added:: target - base]
    @staticmethod
    def fetch_diff(target, base):
        added_entry = []
        for t in target:
            for b in base:
                if(t==b):
                    break
            else:
                # debug:: print("New Content: \n\t" + str(t))
                added_entry.append(t)
        return added_entry
     
    @staticmethod
    def notify_slack(message):
        requests.post('https://hooks.slack.com/services/', data = json.dumps({
            'text': message, # 投稿するテキスト
            'username': u'feedChecker', # 投稿のユーザー名
            'icon_emoji': u':robot_face:', # 投稿のプロフィール画像に入れる絵文字
            'link_names': 1, # メンションを有効にする
        }))

    @staticmethod
    def notify_discord(message):
        DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK', 'EMPTY')
        assert DISCORD_WEBHOOK != 'EMPTY'
        r_body = requests.post(DISCORD_WEBHOOK, {
            'username': 'SiteUpdateNotice',
            'content': message
        })
        r_body.raise_for_status()
