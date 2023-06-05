from flask_login import current_user
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_security import auth_required
from werkzeug.exceptions import (
    NotFound, Conflict, BadRequest)
# from ..models.task import Task as task_model, db
from ..models.post import Post as post_model, db
from ..models.users import User as user_model
from sqlalchemy.exc import IntegrityError
from flask import current_app
from datetime import datetime, date, timedelta
from flask import request, jsonify
import os
import secrets
from ..cache import cache

post_req_data = reqparse.RequestParser()
post_req_data.add_argument('title', required=True, help="title required")
post_req_data.add_argument('description', required=True, help="description required")
post_req_data.add_argument('imageURL')
post_req_data.add_argument('image', type=object)


post_field = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'imageURL': fields.String,
    'creation_date': fields.DateTime,
    'user_id': fields.Integer
}

post_field2 = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'imageURL': fields.String,
    'creation_date': fields.DateTime,
    'user_id': fields.Integer,
    'email': fields.String,
    'username': fields.String
}

class Post(Resource):

    method_decorators = {
        'get': [marshal_with(post_field), auth_required('token')],
        'post': [marshal_with(post_field), auth_required('token')],
        'put': [marshal_with(post_field), auth_required('token')],
        'delete': [auth_required('token')]
    }

    def post(self, id=None, filt=None):
        """Post a post data in the data base

        Raises:
            BadRequest: Id provided by the user
            Conflict: Data already Exist (Data Type integrity will be
            handled by err)
            err: Request Parsing Error

        Returns:
            json: Newly created post
        """
        if id:
            raise BadRequest('Id not required')
        current_app.logger.info('started parsing request')
        imageURL = ""
        if 'image' in request.files:
            image=request.files['image']
            current_app.logger.info("image found")
            filename2 = secrets.token_hex(16)
            extn = image.filename.split(".")[-1]
            complete_filename = filename2 + "." + extn
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], complete_filename))
            current_app.logger.info('created path successfully')
            imageURL= "../assets/uploded_images/"+complete_filename
        else:           
            current_app.logger.info('image key not present')
        title = request.form["title"]
        description = request.form["description"]
        try:
            current_app.logger.info('Starting to add data in data base')
            current_local_time = datetime.utcnow()
            if imageURL != "":
                post = post_model(title=title,description = description, imageURL=complete_filename, user_id=current_user.id, creation_date=current_local_time)
            else:
                post = post_model(title=title,description = description, user_id=current_user.id, creation_date=current_local_time)
            current_user.posts.append(post)
            db.session.add(post)
            db.session.commit()
            current_app.logger.info(f'post added to the database at {current_local_time}')
            return post, 201
        except IntegrityError:
            current_app.logger.warning(
                'Could not add data to database because of conflict')
            db.session.rollback()
            raise Conflict

    def get(self, id=None, filt=None):
        """Get the task data

        Raises:
            NotFound: Task with the id not found

        Returns:
            json: If id provided returns task with that id, else all tasks
        """

        if id:
            '''this will return taking id as post id'''
            # current_app.logger.info(f'Started fetching data with id: {id}')
            # data = post_model.query.filter_by(
            #     id=id, user_id=current_user.id).first()
            # if not data:
            #     current_app.logger.error(f'post with {id} not found')
            #     raise NotFound("Requested Post in not available")
            # current_app.logger.info(f'returning the post with id: {id}')
            # return data

            '''this will return data taking id as user id'''
            current_app.logger.info(f'Started fetching data with user id: {id}')
            user_data = user_model.query.filter_by(id=id).first()
            if not user_data:
                current_app.logger.error(f'user with {id} not found')
                raise NotFound("Requested user in not available")
            current_app.logger.info(f'returning the post with id: {id}')
            data = post_model.query.filter_by(user_id=id).all()
            return data
        if filt=="self":
            current_app.logger.info('assesing all posts by user')
            data = post_model.query.filter_by(user_id=current_user.id).all()
            return data
            current_app.logger.info('returning all posts by user')
            return data
        elif filt=="all":
            current_app.logger.info("returning all posts by all users")
            data = post_model.query.order_by(post_model.creation_date.asc()).all()
            return data
        elif filt=="followed":
            current_app.logger.info("returning posts by users that the curent user follow")
            data = post_model.query.order_by(post_model.creation_date.asc()).all()
            data_filtered = [post for post in data if current_user.is_following(post.user_id)]
            return data_filtered

    def put(self, id=None):
        """_summary_

        Args:
            id (int, optional): Id if the post to update. Defaults to None.

        Raises:
            BadRequest: Id was not provided.
            NotFound: post with id not found.
            Conflict: Duplicate the task

        Returns:
            json: Updated post
        """
        if not id:
            raise BadRequest("Please provide the id of the Post")
        current_app.logger.info('Started fetching the post data')
        post = post_model.query.filter_by(id=id, user_id=current_user.id).first()
        if not post:
            current_app.logger.info(f'No post with id {id}')
            raise NotFound("Data not found")

        current_app.logger.info(
            f'Started updating the post with id {id}')
    

        #     post.update(
        #         post_req_data.parse_args())
        #     db.session.commit()
        # except IntegrityError:
        #     raise Conflict
        # current_app.logger.info(
        #     f'updated the post with id {id}')

        # return post.first(), 200

        imageURL = ""
        if 'image' in request.files:
            image=request.files['image']
            current_app.logger.info("image found")
            filename2 = secrets.token_hex(16)
            extn = image.filename.split(".")[-1]
            complete_filename = filename2 + "." + extn
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], complete_filename))
            current_app.logger.info('created path successfully')
            imageURL= "../assets/uploded_images/"+complete_filename
        else:           
            current_app.logger.info('image key not present')
        title = request.form["title"]
        description = request.form["description"]
        try:
            current_app.logger.info('Starting to add edited data in data base')
            current_app.logger.info(f'edit post title: {title}')
            current_app.logger.info(f'edit post description: {description}')
            # current_local_time = datetime.utcnow()
            if imageURL == "":
                current_app.logger.info('inside imageURL equals null')
                # post.update(title=title,description = description, imageURL=complete_filename, user_id=current_user.id)
                post.title=title
                post.description=description
                post.user_id=current_user.id

            else:
                current_app.logger.info('inside imageURL not equals null')
                # post.update(title=title,description = description, user_id=current_user.id)
                post.title=title
                post.description=description
                post.user_id=current_user.id
                post.imageURL=complete_filename
            db.session.add(post)
            db.session.commit()
            current_app.logger.info('updated the post in the database')
        except IntegrityError:
            current_app.logger.info('found IntegrityError in updating the post')
            raise Conflict
        current_app.logger.info(
            f'updated the post with id {id}')

        return post, 200

    def delete(self, id=None):
        """Delete the post resource

        Args:
            id (int, optional): Id of the post to be deleted. Defaults to None.

        Raises:
            BadRequest: Id not given
            NotFound: post with the id not found

        Returns:
            string: empty string
        """
        if not id:
            raise BadRequest
        current_app.logger.info(f'Checking if task with id {id} exist')
        data = post_model.query.filter_by(
                id=id, user_id=current_user.id).first()
        current_app.logger.info(
            f'found record is {data}')
        if not data:
            raise NotFound("data not found")

        current_app.logger.info(
            f'post with id {id} found, deleting the data')
        db.session.delete(data)
        db.session.commit()
        current_app.logger.info(
            f'post with id {id} deleted successfuly')
        return "", 200
