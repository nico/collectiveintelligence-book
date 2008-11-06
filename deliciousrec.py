from pydelicious import get_popular, get_userposts, get_urlposts

import time

def initializeUserDict(tag, count=5):
  """Grabs the user ids of active del.icio.us users."""
  user_dict = {}
  # get top `count` popular posts...
  for p1 in get_popular(tag=tag)[0:count]:
    # ...and add all users who posted them
    for p2 in get_urlposts(p1['href']):
      user = p2['user']
      user_dict[user] = {}
  return user_dict

def fillItems(user_dict):
  all_items = {}
  # Find links posted by all users
  for user in user_dict:
    for i in range(3):
      try:
        print 'getting userposts for', user
        posts = get_userposts(user)
        break
      except:
        print 'Failed user %s, retrying' % user
        time.sleep(4)
    for post in posts:
      url = post['href']
      user_dict[user][url] = 1.0
      all_items[url] = 1

  # If a user does not have an item, add it with rating 0
  for ratings in user_dict.values():
    for item in all_items:
      if item not in ratings:
        ratings[item] = 0.0

if __name__ == '__main__':
  # stupid little demo
  import recommendations

  print 'getting users...'
  users = initializeUserDict('programming')
  users['thakis'] = {}
  users['ytamshg'] = {}
  users['tubanator'] = {}

  print 'getting their posts (takes a while) ...'
  fillItems(users)

  print 'Distances:'
  print recommendations.sim_distance(users, 'thakis', 'ytamshg')
  print recommendations.sim_distance(users, 'thakis', 'tubanator')
  print recommendations.sim_distance(users, 'tubanator', 'ytamshg')

  print 'Pearsons:'
  print recommendations.sim_pearson(users, 'thakis', 'ytamshg')
  print recommendations.sim_pearson(users, 'thakis', 'tubanator')
  print recommendations.sim_pearson(users, 'tubanator', 'ytamshg')

  print 'Recommendations:'
  print recommendations.getRecommendations(users, 'thakis')[0:10]
  print recommendations.getRecommendations(users, 'ytamshg')[0:10]
  print recommendations.getRecommendations(users, 'tubanator')[0:10]
