from . import db
from flask_security import UserMixin, RoleMixin
from .post import Post

 

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))
 

follower_followed = db.Table("follower_followed",
    db.Model.metadata,
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), index=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
) 

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False, nullable=False)
    aboutme = db.Column(db.Text)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    followed = db.relationship(
        "User",
        secondary=follower_followed,
        primaryjoin = id == follower_followed.c.follower_id,
        secondaryjoin = id == follower_followed.c.followed_id,
    )
    followers = db.relationship(
        "User",
        secondary=follower_followed,
        primaryjoin = id == follower_followed.c.followed_id,
        secondaryjoin = id == follower_followed.c.follower_id,
        overlaps="followed"
    )
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

 

    def follow(self, friend):
        if friend not in self.followed:
            self.followed.append(friend) 

    def unfollow(self, friend):
        if friend in self.followed:
            self.followed.remove(friend)
 

    def is_following(self, user_id):
        return len([followed_user for followed_user in self.followed if followed_user.id==user_id])>0
 

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

 