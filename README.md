# feedChecker
学内サイトのお知らせをスクレイピングするコード

feed.xmlが存在しないとエラーになるので、存在しない場合は `touch feed.xml` などで回避する.

## 使い方

GitHubからダウンロード

```
git clone https://github.com/tomoyk/feedChecker
```

Python3環境のセットアップ

```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

クレデンシャルを取得して，以下にセット

```
 @staticmethod
    def notify_slack(message):
        requests.post('https://hooks.slack.com/services/xxxx', data = json.dumps({
            'text': message, # 投稿するテキスト
            'username': u'feedChecker', # 投稿のユーザー名
            'icon_emoji': u':robot_face:', # 投稿のプロフィール画像に入れる絵文字
            'link_names': 1, # メンションを有効にする
        }))
```

実行

```
python main.py
```

スクリプトを作ってCronに登録

```
#!/bin/bash -xe

cd /home/foo/feedChecker
. env/bin/activate
python main.py
```

```
$ crontab -e
*/5 * * * *  /bin/bash /home/foo/run.sh                                          
```
