#!/usr/bin/env python
import datetime
import feedparser
import os
import sys
import urllib.request
import time
from feeder import Feeder

argv=sys.argv
argv.sort()

def has_argv(check_name):
    for a in argv:
        # Has check_param on argv
        if( a==check_name ):
            return True
    return False

def download(uri, file_name):
    urllib.request.urlretrieve(uri, file_name)

def save_log(message):
    current_dir = os.getcwd()
    with open(current_dir + '/console.log', mode='a', encoding='utf-8') as fd:
        now = datetime.datetime.today()
        msg = str(now) + ' ' + str(message) + '\n'
        print(msg, end='')
        fd.write(msg)

def main():
    try:
        if( os.path.exists('feed.xml') ):
            os.remove('feed_old.xml')
            os.rename('feed.xml', 'feed_old.xml')
        download(uri='https://inside.teu.ac.jp/feed/', file_name='feed.xml')
    except Exception as e:
        save_log(message=e)
        sys.exit(1)

    fresh_feed = feedparser.parse(r'feed.xml')
    saved_feed = feedparser.parse(r'feed_old.xml')
    print('[ok] Success to parse feed*.xml')

    if( has_argv(check_name="--offline") ):
        print("[info] Offline mode is enabled. Not downlaod feed from remote.")
        feeder = Feeder()
        feeder.set(parsed_feed=saved_feed)
        feeder.show(items=['title', 'uri'])
        sys.exit(0)

    feeder = {'fresh': Feeder(), 'saved': Feeder()}
    feeder['fresh'].set(parsed_feed=fresh_feed)
    feeder['saved'].set(parsed_feed=saved_feed)
    print('[ok] Success to set parsed_data')

    new_entries = Feeder.fetch_diff(target=feeder['fresh'].get(), base=feeder['saved'].get())
    # debug:: print(str(new_entries))
    if(len(new_entries) < 1):
         save_log('[info] update was not found.')
         sys.exit(0)
    print('[ok] Success to fetch difference between fresh and saved')

    for entry in new_entries:
        body = entry['title'] + ' (' + entry['date'] +  ')\n' + entry['uri'] + '\n'
        Feeder.notify_slack(message=body)
        time.sleep(3)

if __name__ == '__main__':
    main()
