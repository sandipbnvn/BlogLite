from .user import User
from .post import Post
from flask_restful import Api


api = Api(prefix='/api')
api.add_resource(User, '/users', '/users/<string:filt>', '/users/<int:id>', '/users/<string:followunfollow>/<int:to_follow_id>')
 # filt stands for filtering the user list as per parameter provided
api.add_resource(Post, '/posts', '/posts/<string:filt>', '/posts/<int:id>')
