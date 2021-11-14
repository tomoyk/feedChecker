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

クレデンシャルを環境変数へセット

```
export DISCORD_WEBHOOK=xxx
```

実行

```
python main.py
```

## デーモン化

Systemd TimerとCronの2種類の方法を説明する．

### Systemd Timer

/etc/systemd/systemへsystemd/以下のファイルを配置する．

以下のコマンドで有効化する．

```
sudo systemctl daemon-reload
sudo systemctl start feeder.service
sudo systemctl start feeder.timer
sudo systemctl enable feeder.service
sudo systemctl enable feeder.timer
```

### Cron

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
