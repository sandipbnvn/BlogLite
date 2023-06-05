from flask import current_app
from flask_login import current_user
from flask_restful import Resource, marshal_with, fields, reqparse
from werkzeug.exceptions import Conflict
from sqlalchemy.exc import IntegrityError
from application.models import db
from application.utils.security import user_datastore
from flask_security import auth_required, hash_password
from werkzeug.exceptions import (
    NotFound, Conflict, BadRequest)
from ..models.users import User as users_model, db
from sqlalchemy.orm import aliased
from .post import post_field
from ..cache import cache

user_req = reqparse.RequestParser()
user_req.add_argument('email', required=True, help="email required")
user_req.add_argument('username', required=True, help="username required")
user_req.add_argument('password', required=True, help="password required")
user_req.add_argument('aboutme', required=False)

user_res_fields = {
    'id':fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'aboutme': fields.String,
    'posts': fields.List(fields.Nested(post_field)),
}

user_res_fields2 = {
    'id':fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'aboutme': fields.String,
    'followed_size': fields.Integer,
    'followers_size': fields.Integer,
    'posts_size': fields.Integer,
    'user_following': fields.Boolean,
    'following_user': fields.Boolean
}
user_res_fields3 = {
    'id':fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'aboutme': fields.String,
    'user_following': fields.Boolean,
    'following_user': fields.Boolean
}


class User(Resource):

    @marshal_with(user_res_fields)
    def post(self, filt=None):
        '''It lets the user crate an account;
        if the same email-id alredy in use; raised conflict
        '''
        if filt:
            raise BadRequest('Id not required')
        current_app.logger.info('started parsing the request')
        data = user_req.parse_args()
        current_app.logger.info('request parsed')
        if user_datastore.find_user(email=data['email']):
            raise Conflict("the email is already in use")
        try:
            current_app.logger.info('started createing user in database')
            user = user_datastore.create_user(username=data['username'], aboutme=data['aboutme'], email=data['email'],
                password=hash_password(data['password']))
            db.session.commit()
            current_app.logger.info('inserted the data in database')
            return user
        except IntegrityError:
            raise Conflict

    @auth_required('token')
    @marshal_with(user_res_fields)
    def get(self, filt=None, id=None):
        if id:
            user = users_model.query.get(id)
            if not user:
                raise BadRequest("user not found")
            else:
                return user
        if filt=="self":
            return current_user
        elif filt=="all":
            current_app.logger.info('assesing all users')
            data = users_model.query.all()
            current_app.logger.info('returning all users')
            return data
        elif filt=="followed":
            # current_app.logger.info('assesing all users')
            # data = users_model.query.filter_by(user_id=current_user.id).all()
            # current_app.logger.info('returning all users')
            # return data
            return current_user.followed
        elif filt=="followers":
            return current_user.followers
        else:
            raise BadRequest("Proper parameter is required. Please provide amongst these options: self, all, followed, followers")

    @auth_required('token')
    def put(self, followunfollow=None, to_follow_id=None):
        if not to_follow_id or not followunfollow:
            current_app.logger.info('id/follow_unfollow directive not provided')
            raise BadRequest('id/follow_unfollow directive not provided')
        if to_follow_id==current_user.id:
            current_app.logger.info('user trying to follow himself/herself, raising BadRequest')
            raise BadRequest("You can't follow yourself!")
        try:
            current_app.logger.info('finding the user to be followed')
            to_follow_user = users_model.query.get(to_follow_id)
            if to_follow_user:
                if followunfollow=="follow":
                    current_user.follow(to_follow_user)
                elif followunfollow=="unfollow":
                    current_user.unfollow(to_follow_user)
                current_app.logger.info('modified the followed list')
                db.session.commit()
            else:
                raise NotFound("user does not exist! Please provide a valid user id")
        except IntegrityError:
            raise Conflict
        return "", 200
