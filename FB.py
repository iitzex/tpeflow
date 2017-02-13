# -*- coding: utf-8 -*-
import facebook
# get toke from facebook
token_long = ''


def post(msg):
    graph = get_api(token_long)

    graph.put_wall_post(msg)
#    graph.put_photo(image=open('tower.jpg'), message='Look at this cool photo!')


def post_graph(title, msg):
    graph = get_api(token_long)
    post = graph.put_photo(image=open('tpeflow.png'), message=title)
    pid = post['id']

    publishComment(graph, pid, msg)


def publishComment(graph, post_id, msg):

    comment_id = graph.put_comment(post_id, "\n" + msg)
    return comment_id


def get_api_long(page_access_token):
    graph = facebook.GraphAPI(page_access_token)
    return graph


def get_api(token):
    # Fill in the values noted in previous steps here
    cfg = {
        "page_id": "1649296442008404",  # Step 1
        "access_token": token   # Step 3
    }

    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']

    graph = facebook.GraphAPI(page_access_token)
    return graph


if __name__ == "__main__":
    post("facebook post testing")
