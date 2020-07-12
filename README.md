# feedChecker
学内サイトのお知らせをスクレイピングするコード

feed.xmlが存在しないとエラーになるので、存在しない場合は `touch feed.xml` などで回避する.

## 使い方

Githubから落とす。
```
git clone https://github.com/tomoyk/feedChecker
```

以下からクレデンシャルを取得する。

https://tomoyk.slack.com/apps/new/A0F7XDUAZ--incoming-webhook-

以下のソースの `https://hooks.slack.com/services/` を取得したIncoming WebhookのURLに修正する。

```
 @staticmethod
    def notify_slack(message):
        requests.post('https://hooks.slack.com/services/', data = json.dumps({
            'text': message, # 投稿するテキスト
            'username': u'feedChecker', # 投稿のユーザー名
            'icon_emoji': u':robot_face:', # 投稿のプロフィール画像に入れる絵文字
            'link_names': 1, # メンションを有効にする
        }))
```

動かす。

```
$ python3 main.py
```

スクリプトを作ってCronに登録する。

```
#!/bin/bash -xe

cd /home/foo/feedChecker
/usr/bin/python3 main.py
```

```
$ crontab -e
*/5 * * * *  /bin/bash /home/foo/run.sh                                          
```
