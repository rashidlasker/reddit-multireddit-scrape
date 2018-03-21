from flask import Flask, request
from flask_restful import Resource, Api
import json
import requests
import re
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
api = Api(app)

##################################################### HELPER FUNCTIONS #####################################################
def substringSearch(searchString, text):
        searchString = re.sub(r'\W+', '', searchString.lower())
        text = re.sub(r'\W+', '', text.lower())
        return text.find(searchString)

def updateCache():
    # Set problem parameters
    searchableSubreddits = ['programming', 'webdev', 'coding', 'ReverseEngineering', 'startups', 'Python', 'javascript', 'ruby', 'cpp']
    headers = {'user-agent': 'web:torch-demo-api:v0.0.2 (by /u/RadishSaysHi)'}

    # Get data
    responsePosts = []
    responseComments = []
    for subredditName in searchableSubreddits:
        subredditRequestURL = 'http://www.reddit.com/r/'+ subredditName +'/hot.json'
        subredditResponse = requests.get(subredditRequestURL, headers=headers)
        allPosts = subredditResponse.json()['data']['children']
        for post in allPosts:
            if post['data']['stickied'] == False:
                responsePosts.append({'subreddit' : post['data']['subreddit'], 'title' : post['data']['title'], 'url' : post['data']['url']})
                try:
                    postRequestURL = 'http://www.reddit.com/r/'+ subredditName +'/comments/' + post['data']['id'] +'/.json'
                    postResponse = requests.get(postRequestURL, headers=headers)
                    postLink = 'https://www.reddit.com' + post['data']['permalink']
                    allComments = postResponse.json()[1]['data']['children']
                    for comment in allComments:
                        responseComments.append({'body' : comment['data']['body'], 'post' : postLink})
                except:
                    print('missed comment')
    # Save as cached files
    with open("posts.json", 'w') as outfile:
        json.dump(responsePosts, outfile)
    with open("comments.json", 'w') as outfile:
        json.dump(responseComments, outfile)
    print('updated cache')
    return

sched = BackgroundScheduler(daemon=True)
sched.add_job(updateCache,'interval',minutes=1)
sched.start()


##################################################### API ROUTES #####################################################
class Posts(Resource):
    def get(self):
        queryString = request.args.get('search')
        responsePosts = []
        with open('posts.json') as data_file:    
            data = json.load(data_file)
        for post in data:
            if queryString is None or substringSearch(queryString, post['title'])>0:
                responsePosts.append({'subreddit' : post['subreddit'], 'title' : post['title'], 'url' : post['url']})
        return responsePosts

class Comments(Resource):
    def get(self):
        queryString = request.args.get('search')
        responseComments = []
        with open('comments.json') as data_file:    
            data = json.load(data_file)
        for comment in data:
            if queryString is None or substringSearch(queryString, comment['body'])>0:
                responseComments.append({'body' : comment['body'], 'post' : comment['post']})
        return responseComments


api.add_resource(Posts, '/api/posts/list') # Route_1
api.add_resource(Comments, '/api/comments/search') # Route_2

if __name__ == '__main__':
     app.run(port='5002')