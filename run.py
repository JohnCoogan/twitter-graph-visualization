from twitter_scrape import get_edgelist, fill_out_graph
from analysis_functions import run_analysis
import tweepy, json

def main():
    get_edgelist()
    run_analysis()
    fill_out_graph()    

def get_info():
    settings = {}
    settings['screen_name'] = raw_input('Who do you want to run this for?: ')
    settings['size'] = int(raw_input('How many nodes?: '))
    oauth = json.loads(open('oauth.json','r').read())

    # Create a twitter API connection w/ OAuth.
    auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
    auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
    api = tweepy.API(auth)
    user_info = api.get_user(screen_name=settings['screen_name'])
    settings['user_id'] = int(user_info.id)

    f = open('user_info.json', 'w')
    f.seek(0)
    settings_json = json.dumps(settings, sort_keys=True, indent=4)
    f.write(settings_json)
    f.truncate()
    f.close()

    main()

if __name__ == '__main__':
    get_info()