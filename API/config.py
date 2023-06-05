# import os
# from dotenv import load_dotenv
# load_dotenv()


class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../databases/development.db'
    SECRET_KEY = "thisissecter"
    SECURITY_PASSWORD_SALT = "thisissaltt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    UPLOAD_FOLDER = '../UX/blogfront/src/assets/uploded_images/'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 1000
    CACHE_KEY_PREFIX = 'bloglite_api'
    CACHE_REDIS_URL = 'redis://localhost:6379/1'
    CELERY_BROKER_URL = 'redis://localhost:6379/2'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USERNAME = '21f1002787@ds.study.iitm.ac.in'
    # MAIL_PASSWORD = 'tata@2111'
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_SERVER = 'smtp.mail.yahoo.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = 'sandip_53@yahoo.co.in'
    # MAIL_PASSWORD = 'tata@123'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False


class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DB")
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     SECURITY_PASSWORD_SALT = os.getenv("SECRET_SALT")
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../databases/test.db'
