import os
import textwrap

import dotenv
import twitter


USER = "michael_nielsen"


def fetch_tweets():
    dotenv.load_dotenv()
    api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                      consumer_secret=os.getenv('CONSUMER_SECRET'),
                      access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
                      access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                      tweet_mode='extended')
    return api.GetUserTimeline(screen_name=USER, count=200)


def print_messages(base_ids, messages):
    for base_id in base_ids[::-1]:
        current_id = base_id

        if 'next_id' in messages[current_id]:
            print('+' + '-'*70 + '+')
        
        while 'next_id' in messages[current_id]:
            text = '\n'.join(textwrap.wrap(messages[current_id]['text'], width=70))
            if current_id != base_id:
                print('+' + ' '*70 + '+')
            print(text)
            current_id = messages[current_id]['next_id']


if __name__ == '__main__':
    tweets = fetch_tweets()

    messages = {tweet.id: {'text': tweet.full_text} for tweet in tweets}
    base_ids = [tweet.id for tweet in tweets if tweet.in_reply_to_status_id is None]

    for tweet in tweets:
        reply_id = tweet.in_reply_to_status_id 
        if reply_id in messages:
            messages[reply_id]['next_id'] = tweet.id

    print_messages(base_ids, messages)
