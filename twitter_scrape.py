# -*- coding: utf-8 -*-

import tweepy, json, collections, functools, operator

#  Set these global varaibles to customize your analysis.
#  Register and create tokens at http://dev.twitter.com
def load_configs():
    configs = json.loads(open('user_info.json','r').read())
    oauth = json.loads(open('oauth.json','r').read())

    # Create a twitter API connection w/ OAuth.
    auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
    auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
    api = tweepy.API(auth)

def get_first_friends():
    my_friends = []
    friend_cursors = tweepy.Cursor(api.friends, id = configs['screen_name'])
    for friend_cursor in friend_cursors.items():
        friend = {}
        friend['screen_name'] = friend_cursor.screen_name
        friend['friends_count'] = friend_cursor.friends_count
        friend['followers_count'] = friend_cursor.followers_count
        friend['name'] = friend_cursor.name
        friend['profile_image_url'] = friend_cursor.profile_image_url
        friend['id'] = friend_cursor.id
        friend['following'] = friend_cursor.following
        my_friends.append(friend)

    f = open('temp/myfriends.json', 'w')
    f.seek(0)
    friends_json = json.dumps(my_friends, sort_keys=True, indent=4)
    f.write(friends_json)
    f.truncate()
    f.close()

    totals = functools.reduce(operator.add, map(collections.Counter, my_friends))
    print "%s is follwing: %s" % (configs['screen_name'], len(my_friends))
    print "They follow a total of: %s" % totals['friends_count']
    print "And have a following of: %s" % totals['followers_count']

# Weird that I wasn't getting rate limited on this...
def get_second_friends():
    f = open('temp/myfriends.json','r').read()
    friends = json.loads(f)
    friend_ids = [f['id'] for f in friends]
    for friend_id in friend_ids:
        print "Getting followers for %s" % friend_id
        id_list = api.friends_ids(user_id=friend_id)
        for second_id in id_list:
            write_edgelist(friend_id, second_id)

def write_edgelist(follower, followed):
    f = open('temp/data.edgelist', 'a')
    f.write("%s %s\n" % (follower, followed))
    f.close()

def fill_out_graph():
    load_configs()
    mygraph = json.loads(open('temp/small_graph.json', 'r').read())
    for node in mygraph['nodes']:
        full_user = api.get_user(id=node['id'])
        node['screen_name'] = full_user.screen_name
        node['friends_count'] = full_user.friends_count
        node['followers_count'] = full_user.followers_count
        node['name'] = full_user.name
        node['profile_image_url'] = full_user.profile_image_url
        node['following'] = full_user.following
        print "Saved data for: %s" % full_user.screen_name

    f = open('static/graph.json', 'w')
    f.seek(0)
    graph_json = json.dumps(mygraph, sort_keys=True, indent=4)
    f.write(graph_json)
    f.truncate()
    f.close()

def print_configs():
    for key in configs.keys():
        print "%s: %s" % (key, configs[key])

def get_edgelist():
    load_configs()
    # Create edgelist
    get_first_friends()
    get_second_friends()    

if __name__ == '__main__':
    print "Nothing to do night now. Use run.py"