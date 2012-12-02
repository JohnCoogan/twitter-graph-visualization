# -*- coding: utf-8 -*-

import tweepy, json, collections, functools, operator

#  Set these global varaibles to customize your analysis.
#  Register and create tokens at http://dev.twitter.com
configs = json.loads(open('oauth.json','r').read())

# Create a twitter API connection w/ OAuth.
auth = tweepy.OAuthHandler(configs['consumer_key'], configs['consumer_secret'])
auth.set_access_token(configs['access_token'], configs['access_token_secret'])
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
    print "You are Follwing: %s" % len(my_friends)
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

def get_user_objects(user_list):
    top_users = []
    for user in user_list:
        full_user = api.get_user(id=user)
        user_dict = {}
        user_dict['screen_name'] = full_user.screen_name
        user_dict['friends_count'] = full_user.friends_count
        user_dict['followers_count'] = full_user.followers_count
        user_dict['name'] = full_user.name
        user_dict['profile_image_url'] = full_user.profile_image_url
        user_dict['id'] = full_user.id
        user_dict['following'] = full_user.following
        top_users.append(user_dict)

    f = open('temp/topusers.json', 'w')
    f.seek(0)
    friends_json = json.dumps(top_users, sort_keys=True, indent=4)
    f.write(friends_json)
    f.truncate()
    f.close()

def load_graph():
    mygraph = json.loads(open('temp/small_graph.json', 'r').read())
    for node in mygraph['nodes']:
        full_user = api.get_user(id=node['id'])
        node['screen_name'] = full_user.screen_name
        node['friends_count'] = full_user.friends_count
        node['followers_count'] = full_user.followers_count
        node['name'] = full_user.name
        node['profile_image_url'] = full_user.profile_image_url
        node['following'] = full_user.following

    f = open('temp/fullgraph.json', 'w')
    f.seek(0)
    graph_json = json.dumps(mygraph, sort_keys=True, indent=4)
    f.write(graph_json)
    f.truncate()
    f.close()

def print_configs():
    for key in configs.keys():
        print "%s: %s" % (key, configs[key])
