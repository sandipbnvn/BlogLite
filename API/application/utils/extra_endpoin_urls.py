# import sys
# sys.path.append("..") # Adds higher directory to python modules path.

from flask import make_response, url_for, jsonify
import json
from ..models import db
from ..models.post import Post
from ..models.users import User
from flask_restful import marshal_with
from flask_security import auth_required
from flask import current_app
from flask_login import current_user
from ..resources.post import post_field2
from ..resources.user import user_res_fields2, user_res_fields3
from ..cache import cache
from datetime import datetime, timedelta
import pandas as pd
# from application import celery



def get_followed_list():
    followed_ids = []
    for user in current_user.followed:
        followed_ids.append(user.id)
    return followed_ids

def get_followers_list():
    followers_ids = []
    for user in current_user.followers:
        followers_ids.append(user.id)
    return followers_ids

@auth_required('token')
@marshal_with(post_field2)
def all_post_short(filter_id):
    results = db.session.query(Post, User).join(Post).all()
    resp = []
    for post, user in results:
        post_body = dict()
        post_body['id'] = post.id
        post_body['title'] = post.title
        post_body['description'] = post.description
        post_body['imageURL'] = post.imageURL
        post_body['creation_date'] = post.creation_date
        post_body['user_id'] = user.id
        post_body['email'] = user.email
        post_body['username'] = user.username
        resp.append(post_body)
    if filter_id != 0:
        filtered_resp = []
        for post in resp:
            if post['user_id']==filter_id:
                filtered_resp.append(post)
        final_resp = filtered_resp[::-1]
        return final_resp
    else:
        filtered_resp = []
        followed_ids = get_followed_list()
        current_app.logger.info(f'{followed_ids}')
        for post in resp:
            if post['user_id'] in followed_ids:
                filtered_resp.append(post)
        final_resp = filtered_resp[::-1]
        return final_resp

@auth_required('token')
@marshal_with(user_res_fields2)
# @cache.memoize(50) #comment out to cache this for a particular user
def user_info_short(user_id=0):
    if user_id!=0:
        user = User.query.get(user_id)
    else:
        user = current_user
    posts = Post.query.filter_by(user_id=user.id).all()
    followed_len = len(user.followed)
    followers_len = len(user.followers)
    current_app.logger.info(f'user retrieved successfully from database')
    current_app.logger.info(f'users posts are: {posts}')
    followed_list = get_followed_list()
    followers_list = get_followers_list()
    
    user_info = dict()
    user_info['id']=user.id
    user_info['email']=user.email
    user_info['username']=user.username
    user_info['aboutme']=user.aboutme
    user_info['followed_size']=followed_len
    user_info['followers_size']=followers_len
    user_info['posts_size']=len(posts)
    user_info['user_following']=user.id in followed_list
    user_info['following_user']=user.id in followers_list
    current_app.logger.info(f'fresh response sent at {datetime.utcnow()+timedelta(hours=5, minutes=30)}')
    return user_info

@auth_required('token')
@marshal_with(user_res_fields3)
@cache.cached(timeout=50)
def all_user_info_short():
    users = User.query.all()
    followed_list = get_followed_list()
    followers_list = get_followers_list()
    users_info = []
    for user in users:        
        ind_user_info = dict()
        ind_user_info['id']=user.id
        ind_user_info['email']=user.email
        ind_user_info['username']=user.username
        ind_user_info['aboutme']=user.aboutme
        ind_user_info['user_following']=user.id in followed_list
        ind_user_info['following_user']=user.id in followers_list
        users_info.append(ind_user_info)
    current_app.logger.info(f"fresh result fetched from database at {datetime.utcnow()+timedelta(hours=5, minutes=30)}")
    return users_info
  
@auth_required('token')
@marshal_with(user_res_fields3)
def all_user_info_short_follow(id, list):
    quaried_user = User.query.get(id)
    followed_list = get_followed_list()
    followers_list = get_followers_list()
    users_info = []
    if list=="follows":
        for user in quaried_user.followed:        
            ind_user_info = dict()
            ind_user_info['id']=user.id
            ind_user_info['email']=user.email
            ind_user_info['username']=user.username
            ind_user_info['aboutme']=user.aboutme
            ind_user_info['user_following']=user.id in followed_list
            ind_user_info['following_user']=user.id in followers_list
            users_info.append(ind_user_info)
        return users_info

    elif list=="is followed by":
        for user in quaried_user.followers:        
            ind_user_info = dict()
            ind_user_info['id']=user.id
            ind_user_info['email']=user.email
            ind_user_info['username']=user.username
            ind_user_info['aboutme']=user.aboutme
            ind_user_info['user_following']=user.id in followed_list
            ind_user_info['following_user']=user.id in followers_list
            users_info.append(ind_user_info)
        return users_info


@auth_required('token')
def remove_post_image(id):
    post = Post.query.get(id)
    post.imageURL = None
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "image deleted"}), 200

@auth_required('token')
def export_posts():
    posts = Post.query.filter_by(user_id = current_user.id).all()
    for post in posts:
        post.creation_date = post.creation_date + timedelta(hours=5, minutes = 30)
        post.creation_date = post.creation_date.strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([post.__dict__ for post in posts])
    # df = pd.DataFrame([post for post in posts])
    df.drop(['_sa_instance_state'], axis=1, inplace=True)
    df.drop(['imageURL'], axis=1, inplace=True)
    df.drop(['id'], axis=1, inplace=True)
    df.drop(['user_id'], axis=1, inplace=True)

    response = make_response(df.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=posts.csv"
    response.headers["Content-type"] = "text/csv"
    return response





