
# Reddit Multireddit Scraper
This project was a coding challenge for Torch Technologies. The task was to create an API that aggregates the posts and comments from a list of selected programming subreddits and make them searchable. In particular, the API included the following two endpoints.

### API Description

    GET /api/posts/list?search=<text>

Lists all posts from the front page of each subreddit. The response includes, for each post:

 - The subreddit from which the post was taken
 - The title of the post 
 - The link to the post itself

An optional search query parameter can be used to filter the posts returned in response. 

    GET /api/comments/search?search=<text>

Return comments to the posts from the front page of each subreddit. For simplification, only the root comment in each thread is retrieved. Each comment includes:

 - The comment text 
 - A link to the post with which the comment is associated.

As before, the search parameter can be used for filtering the comments based on the text.

### Local Caching

In this example, the data is stored in a local JSON file to improve API performance. An asynchronous background scheduler processes reddit data and updates the local cache every minute. 

### Next Steps

Given more time on the project, I would implement a database instead of local files. The database would allow for more efficient caching and retrieving, and would greatly improve the scalability of the project.

# Setup

For this project, Python must be installed. In your command line, you'll need to run the following commands in the project repo:

    pip install -r requirements.txt
    set FLASK_APP=server.py
    flask run

# Usage

Once you run the app, you should be able to visit http://127.0.0.1:5000/api/posts/list and see the data!